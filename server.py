import socket

# Find port to listen to 


# Create socket
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Implement limit of bytes that can be received
max_bytes = 1024

# Listens for incoming connections, 1 can be changed as the value, keep it that for now
serverSocket.listen(1)

print("Server ready to receive.")




# Indicator that message has been received
print("Message received!")

# Print Message from client

# Close socket
serverSocket.close()
