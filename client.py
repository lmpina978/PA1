import socket 

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specify max amount of bytes to be sent
max = 1024 

str = open("untitled.txt", "r")

# Close socket
clientSocket.close()
