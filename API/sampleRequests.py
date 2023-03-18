import requests #Send and receive HTTP requests
import json #Convert to and from JSON
import os #Operating system

REST = os.getenv("REST") or "127.0.0.1:5000" #Load the rest host

#MakeRequest: makes a predetermined request
#Input: The HTTP method, the endpoint the request is going to, the data being sent
#Output: The response
def makeRequest(method, endpoint, data):
	print(f"Response to http://{REST}/{endpoint} request is") #Print where the request is going
	jsonData = json.dumps(data) #Dump the data into a json format
	response = method(f"http://{REST}/{endpoint}", data=jsonData, headers={'Content-type': 'application/json'}) #Send the request.
	print(f"response code {response.status_code}, raw response is {response.text}") #Print what comes back
	return response.text #Return the response


makeRequest(requests.post, "api/postData", {"sentData" : "Hello"}) #Make the request for testing purposes