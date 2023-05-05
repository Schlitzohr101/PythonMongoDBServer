from pymongo import MongoClient, database
import subprocess
import threading
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

