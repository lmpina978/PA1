import socket

serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Indicator that message has been received
print("Message received!")



# Close socket
.close()
