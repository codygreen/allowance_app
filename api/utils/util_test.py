"""Unit tests for the utils module."""
import sys
import unittest
from os import environ
from utils import Consumer, RedisMsg
from redis import Redis

sys.path.append('..')

redis_hostname = environ.get('REDIS_HOSTNAME', 'localhost')
redis_port = environ.get('REDIS_PORT', 6379)
stream_name = environ.get('REDIS_STREAM_NAME', 'unit_test')
group_name = environ.get('REDIS_GROUP_NAME', 'unit_test_group')
worker_name = environ.get('REDIS_WORKER_NAME', 'unit_test_group_worker')

test_event = {
    "_id": "642e04f5fd409569f23aa6b0",
    "userId": "642b03b9f0d9fe0007309f0f",
    "amount": 50,
    "type": "gift",
    "state": "pending",
    "date": "2023-04-05T10:10:49.414031"
}

class TestRedisUtil(unittest.TestCase):
    """Unit tests for the Redis consumer class."""
    @classmethod
    def setUpClass(cls) -> None:
        """Set up the test class."""
        # connect to redis
        cls.redis = Redis(redis_hostname, redis_port, db=0, decode_responses=True)

    @classmethod
    def tearDownClass(cls) -> None:
        """Tear down the test class."""
        # delete the consumer group
        cls.redis.xgroup_delconsumer(stream_name, group_name, worker_name)
        cls.redis.xgroup_destroy(stream_name, group_name)
        # close redis connection
        cls.redis.close()

    def setUp(self) -> None:
        """Set up the test case before each run"""
        # add an event to the stream
        self.event_id = self.redis.xadd(stream_name, test_event)
        self.consumer = Consumer(self.redis, stream_name, group_name, worker_name)
        self.events = self.consumer.get_events()

    def tearDown(self) -> None:
        """Tear down the test case after each run"""
        # ack and delete the event from the stream
        self.redis.xack(stream_name, group_name, self.event_id)
        self.redis.xdel(stream_name, self.event_id)

    def test_ack_event(self):
        """Test the ack_event method."""
        print('Testing Redis Consumer ack_event')
        # ensure our pending count is 1
        self.assertEqual(self.redis.xpending(stream_name, group_name)['pending'], 1)
        self.consumer.ack_event(self.event_id)
        # ensure our pending count is 0
        self.assertEqual(self.redis.xpending(stream_name, group_name)['pending'], 0)

    def test_consumer(self):
        """Test the Consumer class."""
        print('Testing Redis Consumer')
        self.assertTrue(self.consumer.redis)

        # assert that the consumer created a consumer group
        self.assertTrue(
            any(
            group_name in group.values() for group in self.redis.xinfo_groups(stream_name)
            )
        )

    def test_get_events(self):
        """Test the get_events method."""
        print('Testing Redis Consumer get_events')
        # assert that consumer.get_events() created a consumer group worker
        self.assertTrue(
            any(
                worker_name in worker.values()
                    for worker in self.redis.xinfo_consumers(stream_name, group_name)
            )
        )
        # assert that consumer.get_events() returned a list of events
        self.assertTrue(self.events)
        self.assertGreater(len(self.events), 0)

    def test_redis_msg(self):
        """Test the RedisMsg class."""
        print('Testing Redis Consumer redis_msg')
        msg = RedisMsg(self.event_id, test_event)
        self.assertEqual(msg.id, self.event_id)
        self.assertEqual(msg.content, test_event)

unittest.main()
