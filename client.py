from socket import *
import sys


clientSocket = socket(AF_INET, SOCK_STREAM)
try:
    clientSocket.connect((sys.argv[1], int(sys.argv[2])))
except error:
    print(str(error))

clientSocket.send(f"GET /{sys.argv[2]}.html HTTP/1.0\r\n".encode())
clientSocket.send("\r\n".encode())

while True:
    data = clientSocket.recv(1024)
    if not data:
        break
    print(data.decode())

clientSocket.close()
