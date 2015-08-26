#!/usr/bin/env python

'''
  Worker task

  Read requests from input queue, process them, and send results to the
  output queue.

  Queues are AWS SQS.
'''

# Standard libraries
import time
import json
import random

# Installed packages
import boto.sqs
import boto.sqs.message
from boto.sqs.message import Message

AWS_REGION = "us-west-2"
QUEUE_IN = "ex6_in"
QUEUE_OUT = "ex6_out"
MAX_WAIT_S = 20 # SQS sets max. of 20 s
DEFAULT_VIS_TIMEOUT_S = 60 

try:
    conn = boto.sqs.connect_to_region(AWS_REGION)
    if conn == None:
        sys.stderr.write("Could not connect to AWS region '{0}'\n".format(AWS_REGION))
        sys.exit(1)

    '''
      EXTEND:
      Add code to create the two queues.
    '''
    q1 = conn.create_queue('kenny')
    q2 = conn.create_queue('kenny2')

except Exception as e:
    sys.stderr.write("Exception connecting to SQS\n")
    sys.stderr.write(str(e))
    sys.exit(1)

while True:
    '''
      EXTEND:
      Replace the following line with code to read a message off the
      input queue, convert from JSON to a Python dict, and assign to
      `req`.
    '''
    #rs is queue from front end, going to read from it
    rs = q1.get_messages()
    if (len(rs)>0):
      m = rs[0]
      msg = m.get_body()
      #Convert json object from sqs and convert to dict so we can code..
      ds = json.loads(msg)
      actual_s = random.randint(0, ds['seconds'])
      time.sleep(actual_s)
      ds['actual_s'] = actual_s
      q1.delete_message(m)

    '''
      EXTEND:
      Replace the following line with code to put the response on the
      output queue, in JSON representation.
    '''
    if (len(rs)>0):
      m = Message()
      js = json.dumps(ds)
      m.set_body(js)
      q2.write(m) #output queue from worker so we can get backend.py to read it.
      print "Output Queue Written"
