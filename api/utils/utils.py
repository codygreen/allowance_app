from enum import Enum
from redis import Redis
from typing import List, Union
import threading, os

class RedisMsg:
    def __init__(self, id, content):
        self.id = id
        self.content = content

    def __str__(self):
        # return f"id: {self.id}, content: {self.content}"
        return("id: {}, content: {}".format(self.id, self.content))

    def __repr__(self):
        # return f"RedisMsg(id={self.id}, content={self.content})"
        return("RedisMsg(id={}, content={})".format(self.id, self.content))

class MsgId(Enum):
    new_events = ">"
    all_events = "0"

class Consumer:
    def __init__(
            self, 
            redis: Redis, 
            stream_name: str, 
            group_name: str,
            worker_name: Union[str, int] = f"{os.getpid()}{threading.get_ident()}",
            batch_size: int = 1,
            max_wait_time_ms: int = 10000,
            poll_time_ms: int = 1000,
            cleanup_on_exit: bool = True
            ):
        self.redis = redis
        self.stream_name = stream_name
        self.group_name = group_name
        self.worker_name = worker_name
        self.batch_size = batch_size
        self.max_wait_time_ms = max_wait_time_ms
        self.poll_time_ms = poll_time_ms
        self.cleanup_on_exit = cleanup_on_exit
        self._create_group()
        
    def _create_group(self):
        groups = self.redis.xinfo_groups(self.stream_name)
        for group in groups:
            if group.get('name') == self.group_name:
                return
        self.redis.xgroup_create(self.stream_name, self.group_name, id=0)

    def ack_event(self, event_id: str):
        self.redis.xack(self.stream_name, self.group_name, event_id)

    def get_events(self) -> List[RedisMsg]:
        events = []
        # event = self.redis.xpending(
        #     self.   
        # )
        event = self.redis.xreadgroup(
            self.group_name,
            self.worker_name,
            {self.stream_name: MsgId.new_events.value},
            count=self.batch_size,
            block=self.max_wait_time_ms
        )
        events.extend(event)
        return events        
