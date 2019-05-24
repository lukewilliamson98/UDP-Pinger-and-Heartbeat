# UDP_HbS.py
# Luke Williamson

from socket import *
import sys                  # for CLAs
argv = sys.argv
serverIPaddress = argv[1]   # get command line argument (server IP)

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket, use port 12000
serverSocket.bind((serverIPaddress, 12000))

maxTimeOuts = 50        # holds maximum number of time outs
consecTimeOuts = 0      # initialize consecutive number of time outs
previous = 0            # holds previous sequence number, initialized to 0
while True:
    try:
        serverSocket.settimeout(1)                      # 1 sec time out
        # Receive the client packet along with the address it is coming from
        message, address = serverSocket.recvfrom(1024)  
        message = int(message,base=10)                  # convert sequence num to int
        diff = message - previous                       # store difference between seq nums
        if diff > 1:                                    # if packet(s) are skipped
            print "Lost " + str(diff - 1) + " messages" # print num of lost messages
            print "Server received msg " + str(message) # print current sequence num
            previous = message                          # assign current seq num to previous
            consecTimeOuts = 0                          # 0 consecutive time outs
        else:                                           # otherwise
            print "Server received msg " + str(message) # print current sequence num
            previous = message                          # assign current seq num to previous
            consecTimeOuts = 0                          # 0 consecutive time outs
        message = str(message)                          # convert sequence num to string
        serverSocket.sendto(message, address)           # send data back to client    
    except timeout:
        print "Server timed out"                        # print time out msg
        consecTimeOuts = consecTimeOuts + 1             # increase consecTimeOuts by 1
        if consecTimeOuts >= maxTimeOuts:               # if 50 or more consecTimeOuts
            break                                       #  assume client application has stopped, break out of loop, and end script
