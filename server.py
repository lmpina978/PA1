import socket
import os

# Create socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

max_bytes = 1024

# Listens for incoming connections, 1 can be changed as the value, keep it that for now
serverSocket.listen(1)

# Indicator that message has been received
print("Message received!")

# Print Message from client

# Close socket
.close()
