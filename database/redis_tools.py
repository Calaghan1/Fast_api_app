import os
import pickle
from typing import Any

import redis

local_host = 'localhost'
local_port = 6379
docker: str = str(os.getenv('REDIS_HOST'))
docker_port: str = str(os.getenv('REDIS_PORT'))

end_host = ''
if docker:
    end_host = docker
else:
    end_host = 'localhost'
port = ''
if docker_port:
    port = docker_port
else:
    port = 6379
class RedisTools:
    def __init__(self) -> None:
        self.rd = redis.Redis(host=docker, port=docker_port)

    def set_pair(self, key: str, value: Any) -> None:
        data = pickle.dumps(value)
        self.rd.set(key, data)

    def get_value(self, key: str) -> Any:
        data = self.rd.get(key)
        if data:
            return pickle.loads(data)
        else:
            return data

    def del_key(self, key: str) -> None:
        self.rd.delete(key)

    def find_and_del(self, pattern: str) -> None:
        for key in self.rd.scan_iter(match='*' + pattern + '*'):
            self.rd.delete(key)

    def del_all(self) -> None:
        self.rd.flushall()


rd = RedisTools()
