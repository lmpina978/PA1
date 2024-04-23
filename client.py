import socket 
import os

# Create client socket
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Specify max amount of bytes to be sent
max = 1024 

# Open file for string
txtfile = open("untitled.txt", "r")
txtdata = txtfile.read()

# Check if data is string 
stringcheck = isinstance(txtdata, str)

if stringcheck and txtdata.length() <= max:
  
# Get byte amount of file and see if it exceeds max


# Close socket
clientSocket.close()
