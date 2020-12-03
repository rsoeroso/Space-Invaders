import socket

host = "127.0.0.1"
port = 65432
mySocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
mySocket.bind((host, port))

print("UDP server listening on port {0}.\n".format(port))

while True:
  data, addr = mySocket.recvfrom(1024) # receive 1024 bytes
  data = data.decode("utf-8")
  print("Message: " + data)

mySocket.close()