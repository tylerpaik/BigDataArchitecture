import redis as r
import os

#Instantiate redis db
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
redis_client = r.Redis(host=REDIS_HOST, port=REDIS_PORT)