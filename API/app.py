##
from flask import Flask, request, Response, jsonify #Useful flask functionality
import requests #Send and receive HTTP requests
import json #Convert to and from JSON
import pika #Consume RABBITMQ
import sys #System requirements
import os #Operating system

REST = os.getenv("rest") or "127.0.0.1:5000" #Load the rest host
app = Flask(__name__) #Set the flask app name

rabbitMQHost = os.getenv("$RABBITMQ_HOST") or "127.0.0.1" #Load the rabbit host (currently 127.0.0.1, but environment placeholder put for later)
queueName = "taskQueue" #Set the rabbitmq queue name
print("Connecting to rabbitmq({})".format(rabbitMQHost)) #Print to the console that it is connecting to the queue

#Build the rabbit connection
connection = pika.BlockingConnection(
	pika.ConnectionParameters(host=rabbitMQHost))
channel = connection.channel() #Open the rabbit channel

channel.queue_declare(queue='task_queue') #Declare the queue

#PostData: posts the data I send to the rabbit queue
#Input: None, but sent data is pulled from the http request
#Output: None
@app.route("/api/postData", methods = ["POST"]) #Routing structure: @appName.route("URLfromtheNormalRoute", methods = ["HTTPMETHOD"])
def postData():
	sentData = json.loads(request.data) #Load the json data from the request
	sentData = sentData["sentData"] #Get the sent data from the call, which I appropriately named "sentData"

	#Publish the request to the RABBITMQ queue
	channel.basic_publish(
		exchange='', #Send the exchange, which is empty because I did not set up an exchange
		routing_key = queueName, #Send the queue as the routing key
		body = sentData) #Send the data as the body
	print(" [x] Sent %r" % sentData) #Print that the request was sent

	connection.close() #Close the rabbit connection

	#Return a response saying that the action was queued
	return Response(response=json.dumps({"Action" : "Queued"}), status=200, mimetype="application/json")

app.run(host = "0.0.0.0", port = 5000) #Run the flask app