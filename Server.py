import socket
import ipaddress
import threading
import time
import contextlib
import errno
# from dataclasses import dataclass
# import MongoDBConnection as mongo
# from MongoDBConnection import TrafficData

from pymongo import MongoClient, database
import pymongo
from datetime import datetime, timedelta
import time

DBName = "test" #Use this to change which Database we're accessing
connectionURL = "mongodb+srv://wemx836:dbpass88@cardatacluster.s0zsnzy.mongodb.net/?retryWrites=true&w=majority" #Put your database URL here
sensorTable = "TrafficDataSet" #Change this to the name of your sensor data table

class TrafficData:
	_id = None
	_time = None
	_payload = None

	def __init__(self, id = None, time = None, payload = None):
		self._id = id
		self._time = time
		self._payload = payload

	def setId(self, newId):
		self._id = newId

	def setTime(self, newTime):
		self._time = newTime

	def setPayload(self, newPayload):
		self._payload = newPayload
  
	def getPayload(self):
		return self._payload

  
    

def QueryToList(query):
	#TODO: Convert the query that you get in this function to a list and return it
	print("query:",query)
	documentList = []
	for document in query:
		print("document:",document)
		temp = TrafficData()
		temp.setId(document["_id"])
		temp.setTime(document["time"])
		temp.setPayload(document["payload"])
		documentList.append(temp)
  
	return documentList
  #HINT: MongoDB queries are iterable

def QueryDatabase():
	global DBName
	global connectionURL
	global currentDBName
	global running
	global filterTime
	global sensorTable
	cluster = None
	client = None
	db = None
	try:
		print("in try for MongoDbConnection...")
		cluster = connectionURL
		client = MongoClient(cluster)
		db = client[DBName]
		print("Database collections: ", db.list_collection_names())
		# print("db:",db)
		#We first ask the user which collection they'd like to draw from.
		sensorTable = db[sensorTable]

		print("Table:", sensorTable)
		#We convert the cursor that mongo gives us to a list for easier iteration.
		timeCutOff = datetime.now() - timedelta(minutes=5) #TODO: Set how many minutes you allow

		return QueryToList(sensorTable.find({"time":{"$gte":timeCutOff}}))
		# currentDocuments = QueryToList(sensorTable.find({"time":{"$lte":timeCutOff}}))

		# print("Current Docs:",currentDocuments)
		# for item in currentDocuments:
		# 	print("curr_item:",item)
		# print("Old Docs:",oldDocuments)

		# totalPayloadData = 0.0

		

	except Exception as e:
		print("Please make sure that this machine's IP has access to MongoDB.")
		print("Error:",e)
		exit(0)



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
    return QueryDatabase();


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