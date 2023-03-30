from flask import Flask, request, Response, jsonify #Useful flask functionality
import requests #Send and receive HTTP requests
import json #Convert to and from JSON
import pika #Consume RABBITMQ
import sys #System requirements
import os #Pulls from the OS

#For more info on RABBITMQ coding, see https://www.rabbitmq.com/getstarted.html

rabbitMQHost = os.getenv("$RABBITMQ_HOST") or "127.0.0.1" #Load the rabbit host (currently 127.0.0.1, but environment placeholder put for later)
queueName = "taskQueue" #Set the rabbitmq queue name
print("Connecting to rabbitmq({})".format(rabbitMQHost)) #Print to the console that it is connecting to the queue

#Built following tutorial 4: https://www.rabbitmq.com/tutorials/tutorial-four-python.html

connection = pika.BlockingConnection( #Setup a connection for RABBITMQ
    pika.ConnectionParameters(host = rabbitMQHost)) #Set up the host for the connection
channel = connection.channel() #Build out a channel for the RABBITMQ queue

channel.queue_declare(queue = queueName) #Declare the queue in the channel

print(" [*] Waiting for info. To exit press CTRL+C") #Print a note showing that the queue is waiting

#Callback: a default function in RABBITMQ that catches messages as they are pulled from the queue. Only the definition is default, the rest is user defined
#Input: The channel, the HTTP method type, properties of the message, and the actual data body
#Output: None
def callback(ch, method, properties, body):
    recBody = body.decode() #Decode the data body 
    print(" [x] Received %r" % recBody) #Print that the data has been received
    ch.basic_ack(delivery_tag = method.delivery_tag) #Send an acknowledgement back to the queue


#Setup a basic consumer for the RABBITMQ queue. Basically, if you see something in the queue held in variable queueName, call the callback function
channel.basic_consume(
    queue = queueName, on_message_callback = callback)

channel.start_consuming() #Start consuming messages