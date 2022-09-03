import time
import zmq
import sys
import struct

filename = "files/{}".format(sys.argv[1])

context = zmq.Context()

# Socket to talk to server
# print("Connecting to hello world server...")
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

print("Sending a request ...")
socket.send_string(filename)
info = socket.recv().decode()
print(info)
r, w = info.split("/")
print("Servers info: read size {}, write size {}".format(r, w))

start = time.time()

# reply
chunk = 1
while True:
    socket.send_string("OK")
    data = socket.recv()
    print("Data preview: {}".format(data[:20]))
    if data ==  b"Done":
        print("Done!")
        break
    # print("Received data: {}".format(struct.unpack("iiiii", data[:20])))
    print("Received data chunk {}".format(chunk))
    chunk += 1

# servermsg = socket.recv()
# print(servermsg)

elapsed = time.time() - start
print("Elapsed time: {}".format(elapsed))

logfile = sys.argv[1]
RESULT = "results/{}.csv".format(logfile[:-4])
with open(RESULT, "a") as f:
    f.write(logfile + "," + r + "," + w + "," + str(elapsed) + "\n")