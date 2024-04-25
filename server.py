import socket
import sys
import os

# Create client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specify max amount of bytes to be sent in each packet
max = 1024

# Will count the amount of packets that were sent from client to server
packetCount = 0

# Open file for string
txtfile = open("untitled.txt", "r")
filename = sys.argv[1]

print("Opening " + filename)

txtdata = txtfile.read()

# Check if data is string and get size in bytes
stringcheck = isinstance(txtdata, str)
stringsize = os.path.getsize("untitled.txt")


# Close socket
clientSocket.close()
