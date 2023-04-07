"""Redis consumer class"""
from enum import Enum
from typing import List, Union
import threading
import os
from redis import Redis

class RedisMsg:
    """Redis message class"""
    def __init__(self, msg_id, content):
        self.id = msg_id
        self.content = content

    def __str__(self):
        return f"id: {self.id}, content: {self.content}"

    def __repr__(self):
        return f"RedisMsg(id={self.id}, content={self.content})"

class MsgId(Enum):
    """Message id enum"""
    NEW_EVENTS = ">"
    ALL_EVENTS = "0"

# pylint: disable=too-many-instance-attributes, too-many-arguments
class Consumer:
    """Redis consumer class"""
    def __init__(
            self,
            redis: Redis,
            stream_name: str,
            group_name: str,
            worker_name: Union[str, int] = f"{os.getpid()}{threading.get_ident()}",
            batch_size: int = 1,
            max_wait_time_ms: int = 10000,
            poll_time_ms: int = 1000
            ):
        self.redis = redis
        self.stream_name = stream_name
        self.group_name = group_name
        self.worker_name = worker_name
        self.batch_size = batch_size
        self.max_wait_time_ms = max_wait_time_ms
        self.poll_time_ms = poll_time_ms
        self._create_group()

    def _create_group(self):
        """Create Redis consumer group if it does not exist"""
        groups = self.redis.xinfo_groups(self.stream_name)
        for group in groups:
            if group.get('name') == self.group_name:
                return
        self.redis.xgroup_create(self.stream_name, self.group_name, id=0)

    def ack_event(self, event_id: str):
        """Acknowledge event"""
        self.redis.xack(self.stream_name, self.group_name, event_id)

    def get_events(self) -> List[RedisMsg]:
        """Get events from Redis stream"""
        events = []
        # event = self.redis.xpending(
        #     self.
        # )
        event = self.redis.xreadgroup(
            self.group_name,
            self.worker_name,
            {self.stream_name: MsgId.NEW_EVENTS.value},
            count=self.batch_size,
            block=self.max_wait_time_ms
        )
        events.extend(event)
        return events
