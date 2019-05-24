# UDP_PingS.py

from socket import *
import sys
argv = sys.argv
serverIPaddress = argv[1]

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket, use port 12000
serverSocket.bind((serverIPaddress, 12000))

while True:
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    # Capitalize the message from the client
    message = message.upper()
    serverSocket.sendto(message, address)
