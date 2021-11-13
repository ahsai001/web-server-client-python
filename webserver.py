from socket import *
import sys
from _thread import *
import threading


def threaded_client(connection_socket):
    try:
        message = connection_socket.recv(1024)
        filename = message.split()[1]
        f = open(filename[1:])
        outputdata = f.read()

        print('File ', filename, 'has been sent on', threading.currentThread().getName())

        # Send one HTTP header line into socket
        connection_socket.send("HTTP/1.1 200 OK\r\n".encode('UTF-8'))
        connection_socket.send("Connection: keep-alive\r\n".encode('UTF-8'))
        connection_socket.send("Content-type: text/html; charset: utf-8;\r\n".encode('UTF-8'))
        connection_socket.send("\r\n".encode('UTF-8'))
        # Send the content of the requested file to the client
        for i in range(0, len(outputdata)):
            connection_socket.send(outputdata[i].encode('UTF-8'))
        connection_socket.send("\r\n".encode('UTF-8'))
    except FileNotFoundError:
        # Send response message for file not found
        connection_socket.send('HTTP/1.1 404 Not Found\r\n'.encode('UTF-8'))
        # Close client socket
    connection_socket.close()


serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
serverSocket.bind(('', 8000))
serverSocket.listen(5)
threadCount = 0

while True:
    # Establish the connection
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    start_new_thread(threaded_client, (connectionSocket,))
    threadCount += 1
    print('Thread Number: ' + str(threadCount))

serverSocket.close()
sys.exit()  # Terminate the program after sending the corresponding data
