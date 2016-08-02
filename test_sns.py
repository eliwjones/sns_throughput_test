from gevent import monkey
monkey.patch_all()

import gevent
from gevent.queue import Empty, Queue

import boto.sns
from config import *
import time
import sys


def logger(done):
    counter = 0
    while True:
        done.get()
        counter += 1
        if counter % 50 == 0:
            print "[%s] %d Messages Sent!" % (time.strftime("%H:%M:%S", time.localtime()), counter)


def sns_messager(client, heap, done):
    topic_arn = ARN_BASE + ":dean-test-topic"
    try:
        while True:
            message = heap.get(timeout=1)
            client.publish(topic_arn, message, subject="sns test.")
            done.put(1)
    except Empty:
        print "Finished."


workers = 100
messages = 1000
batch_size = 50
print "\nDEFAULTS: workers: %d, messages: %d\n" % (workers, messages)
print "If one wishes to use more or less workers to send more or less messages:\n"
print "\tpython test_sns.py <num_workers> <num_messages> <batch_size>\n\n"
args = sys.argv[1:]
if len(args) > 0:
    workers = int(args[0])
if len(args) > 1:
    messages = int(args[1])
if len(args) > 2:
    batch_size = int(args[2])


# We shall attempt to use one boto client across all green threads.
# So that, we do not need to keep re-connecting.
client = boto.sns.connect_to_region(REGION, aws_access_key_id=ACCESS_KEY, aws_secret_access_key=SECRET)

heap = Queue()
done = Queue()
for i in range(messages):
    message_id = "id:%d" % (i)
    heap.put(message_id)

gevent.spawn(logger, done)

# Slowly ramp up workers as SNS wakes up.
green_threads = []
while workers:
    print "[%s] Starting %d Threads!" % (time.strftime("%H:%M:%S", time.localtime()), batch_size)
    green_threads += [gevent.spawn(sns_messager, client, heap, done) for i in range(batch_size)]
    workers -= batch_size
    gevent.sleep(5)


gevent.joinall(green_threads)
