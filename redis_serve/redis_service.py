import os
import redis
import json

class RedisService:
    def __init__(self):
        self.redis = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), decode_responses=True)
        
    def setTemporalInfo(self, key, data, ttl=100):
        json_data = json.dumps(data)
        self.redis.setex(key, ttl, json_data)
        
    def getTemporalInfo(self, key):
        data = self.redis.get(key)
        if data is not None:
            return json.load(data)
        return None

    def storeChatStream(self, chatBody):
        pass