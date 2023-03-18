# API

This is currently a basic template for the API with RABBITMQ functionality coded in. This assumes RABBITMQ is already setup and running. As a basic template, this API only has one method to send JSON specified in the "sampleRequest" file into the api.

To start:

In one command line prompt, navagate to the flaskAPI file and run python3 flaskAPI.py

In a separate command line prompt, navagate to the flaskWorker file and run python3 flaskWorker.py

In one final command line prompt, navagate to the sampleRequest file and run python3 sampleRequest.py .

After that is run, the response of 200 and "Hello" should be shown on the sampleRequests prompt and the worker prompt should acknowledge that it received the "Hello" data.

This current version is only here to show basic functionality currently and will be changed with time.
