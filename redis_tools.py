import os
import pickle

import redis

local_host = 'localhost'
docker: str = str(os.getenv('REDIS_HOST'))
docker_port: str = str(os.getenv('REDIS_PORT'))


class RedisTools:
    def __init__(self) -> None:
        self.rd = redis.Redis(host=docker, port=int(docker_port))

    def set_pair(self, key, value):
        data = pickle.dumps(value)
        self.rd.set(key, data)

    def get_value(self, key):
        data = self.rd.get(key)
        if data:
            return pickle.loads(data)
        else:
            return data

    def del_key(self, key):
        self.rd.delete(key)

    def del_all(self):
        self.rd.flushall()
