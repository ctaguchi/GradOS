import time
import zmq
import struct
import sys

args = sys.argv
FileReadSize = int(args[1])
SocketWriteSize = int(args[2])

context = zmq.Context() # They create a ZeroMQ context to work with, 
socket = context.socket(zmq.REP) # and a socket.
socket.bind("tcp://*:5555") # The server binds its REP (reply) socket to port 5555

while True:
    # Wait for next request from client
    message = socket.recv().decode()
    print(f"Received request: {message}")
    print("File to read: {}".format(message))
    socket.send_string(str(FileReadSize) + "/" + str(SocketWriteSize))
    # socket.send_string("Request received by the server.")

    # Send reply back to client
    file = message
    # Read the file
    with open(file, "rb") as f:
        byteread = 0
        data = b""
        while True:
            dataread = f.read(FileReadSize)
            if dataread == b"": # When no more data to read
                break
            else:
                data += f.read(FileReadSize) # reading by chunks
                byteread += FileReadSize
                f.seek(byteread)
    # Send the file
    bytesent = 0
    chunk = 1
    while True:
        msg = socket.recv()
        print(msg)
        upper = bytesent + SocketWriteSize
        datasent = data[bytesent:upper]
        print("Sending Chunk {} ...".format(chunk))
        print("Chunk preview: {}".format(datasent[:20]))
        # print(datasent[:5])
        if datasent == b"":
            print("Done!")
            socket.send_string("Done")
            break
        socket.send(datasent)
        print("Sent file preview: {}".format(struct.unpack("iiiii", datasent[:20])))
        bytesent += SocketWriteSize
        chunk += 1
    
        print("Data type: {}".format(type(data)))
    
    # socket.send_string("File sent")
    # break

    # socket.send_string("Server sent the file.")

