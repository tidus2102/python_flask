from rq import Queue
from worker import conn

default_queue = Queue("default", connection=conn)
high_queue = Queue("high", connection=conn)
low_queue = Queue("low", connection=conn)