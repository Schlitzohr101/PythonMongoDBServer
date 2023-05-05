import socket
import ipaddress
import threading
import time
import contextlib
import errno
from dataclasses import dataclass
import MongoDBConnection as mongo
from MongoDBConnection import TrafficData
import random
import sys

maxPacketSize = 1024
defaultPort = 5500 #TODO: Set this to your preferred port

def GetFreePort(minPort: int = 1024, maxPort: int = 65535):
    for i in range(minPort, maxPort):
        print("Testing port",i);
        with contextlib.closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as potentialPort:
            try:
                potentialPort.bind(('localhost', i));
                potentialPort.close();
                print("Server listening on port",i);
                return i
            except socket.error as e:
                if e.errno == errno.EADDRINUSE:
                    print("Port",i,"already in use. Checking next...");
                else:
                    print("An exotic error occurred:",e);

def GetServerData():
    return mongo.QueryDatabase();


def ListenOnTCP(tcpSocket: socket.socket, socketAddress):
    print('Client connected on:', socketAddress)
    print("prompting mongoDB for data")
    #got a connection on this socket so get mongo data and process for best road in the given time period
    #start with dictionary...
    trafficDict = {}
    data = GetServerData()
    for item in data:
        sumOfTopic = 0.0
        topic = ""
        for key, value in item.getPayload().items():
            print("key:",key)
            print("value:",value)
            if key.lower().find("topic") == -1 and key.lower().find("time") == -1:
                sumOfTopic += value
                print("sumOfTopic:",sumOfTopic)
            elif key.lower().find("topic") != -1:
                topic = value
        trafficDict[topic] = sumOfTopic/3.0
    
    print("trafficDict:",trafficDict)
    lowestVal = 50000
    topic = ""
    for key, value in trafficDict.items():
        if value < lowestVal:
            topic = key
            lowestVal = value
    
    message = "Based on sensor data, the best highway is "+topic+" with a average time of "+str(lowestVal)
    
    tcpSocket.sendall(message.encode())
    






def CreateTCPSocket() -> socket.socket:
    tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM);
    tcpPort = defaultPort
    
    while True: 
        print("Please enter in a port, or leave empty for default",end="")
        cur_port = input(": ")
        try:
            cur_port = int(cur_port)
            tcpPort = cur_port
            break
        except Exception as e:
            if cur_port == "":
                tcpPort = defaultPort
                break
            print("that is not a valid port... Try again")
    
    print("TCP Port:",tcpPort);
    tcpSocket.bind(('localhost', tcpPort));
    return tcpSocket;

def LaunchTCPThreads():
    tcpSocket = CreateTCPSocket();
    tcpSocket.listen(5);
    while True:
        print("waiting for accept...")
        connectionSocket, connectionAddress = tcpSocket.accept();
        connectionThread = threading.Thread(target=ListenOnTCP, args=[connectionSocket, connectionAddress]);
        connectionThread.start();

if __name__ == "__main__":
    tcpThread = threading.Thread(target=LaunchTCPThreads);
    tcpThread.start();

    while True:
        time.sleep(1);
    print("Ending program by exit signal...");
    # GetServerData()