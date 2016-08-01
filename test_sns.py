from gevent import monkey
monkey.patch_all()

import gevent
from gevent.queue import Empty, Queue

import boto.sns
from config import *
import sys


def sns_messager(client, heap):
    http_arn = ARN_BASE + "where is this from?"
    try:
        while True:
            message = heap.get(timeout=1)
            client.publish(http_arn, message, subject="sns test.")
    except Empty:
        print "Finished."


workers, messages = 400, 1200
print "\nDEFAULTS: workers: %d, messages: %d\n" % (workers, messages)
print "If one wishes to use more or less workers to send more or less messages:\n"
print "\tpython test_sns.py <num_workers> <num_messages>\n\n"
args = sys.argv[1:]
if len(args) > 0:
    workers = int(args[0])
if len(args) > 1:
    message = int(args[1])


# We shall attempt to use one boto client across all green threads.
# So that, we do not need to keep re-connecting.
client = boto.sns.connect_to_region("us-west-1", aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET)

heap = Queue()
for i in range(messages):
    message_id = "id:%d" % (i)
    heap.put(message_id)

green_threads = [gevent.spawn(sns_messager, client, heap) for i in range(workers)]

gevent.joinall(green_threads)
