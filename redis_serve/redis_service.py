import os
import redis
import json


class RedisService:
    _instance = None

    def __init__(self):
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(RedisService, cls).__new__(cls)
            cls._instance._init_connection()
        return cls._instance

    def _init_connection(self):
        self.redis = redis.Redis(
            host=os.getenv("REDIS_CLOUD_HOST"),
            port=int(os.getenv("REDIS_CLOUD_PORT")),
            username=os.getenv("REDIS_CLOUD_USERNAME"),
            password=os.getenv("REDIS_CLOUD_PASSWORD"),
            decode_responses=True,
        )

    def setTemporalInfo(self, key, data, ttl=100):
        json_data = json.dumps(data)
        if ttl is None:
            self.redis.set(key, json_data)
        else:
            self.redis.setex(key, ttl, json_data)

    def getTemporalInfo(self, key):
        data = self.redis.get(key)
        if data is not None:
            return json.loads(data)
        return None

    def deleteTemporalInfo(self, key):
        self.redis.delete(key)

    def publish(self, channel, message):
        """Publish JSON message to a channel"""
        self.redis.publish(channel, json.dumps(message))

    def subscribe(self, channel):
        """Subscribe to a channel and return the pubsub object"""
        pubsub = self.redis.pubsub()
        pubsub.subscribe(channel)
        return pubsub

    def storeChatStream(self, chatBody):
        pass
