import socket
import ipaddress
import threading
import time
import contextlib
import errno

maxPacketSize = 1024
defaultPort = 5500 # TODO: Change this to your expected port
localServerIP = '127.0.0.1'
serverIP = '***.***.***.***' #TODO: Change this to your instance IP

tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
try:
    tcpPort = int(input("Please enter the TCP port of the host..."));
except:
    tcpPort = 0;
if tcpPort == 0:
    tcpPort = defaultPort;
if serverIP.find("*") != -1:
    tcpSocket.connect((localServerIP, tcpPort));
    print("using local ip...")
else:
    tcpSocket.connect((serverIP, tcpPort));
    print("using server ip of :",serverIP)
clientMessage = "";
while clientMessage != "exit":
    # clientMessage = input("Hit enter to have the client ask for most optimal highway (Or type \"exit\" to exit):\n>");

    # tcpSocket.send(clientMessage.encode())
    print("waiting to recieve the most optimal road based on time from server...")
    data = tcpSocket.recv(1024)
    print("recieved this from server:", data.decode())
    
    
    clientMessage = input("Hit enter ask for most optimal highway (Or type \"exit\" to exit):\n>");

    
    #TODO: Send the message to your server
    #TODO: Receive a reply from the server for the best highway to take
    #TODO: Print the best highway to take
    
tcpSocket.close();

