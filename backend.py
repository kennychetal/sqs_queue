#!/usr/bin/env python

'''
  Back end server
'''

# Library packages
#import json
import os
import re
import sys
import json
import os.path
# Installed packages
import boto.sqs

from bottle import route, run, request, response, default_app

AWS_REGION = "us-west-2"
QUEUE_OUT = "ex6_out"
MAX_WAIT_S = 20 # SQS sets max. of 20 s
PORT = 8081

try:
    conn = boto.sqs.connect_to_region(AWS_REGION)
    if conn == None:
        sys.stderr.write("Could not connect to AWS region '{0}'\n".format(AWS_REGION))
        sys.exit(1)

    '''
      EXTEND:
      Add code to open the output queue.
    '''
    q = conn.create_queue('kenny2')



except Exception as e:
    sys.stderr.write("Exception connecting to SQS\n")
    sys.stderr.write(str(e))
    sys.exit(1)

@route('/')
def app():
    #m = {'id': 0, 'f': 10, 's': 10, 'actual_s': 5}
    msg = None
    wq = q.get_messages()
    if(len(wq)>0):
      m = wq[0]
      msg = m.get_body()
      msg = json.loads(msg)
      q.delete_message(m)
      print "alive"
    if msg == None:
        response.status = 204 # "No content"
        return 'Queue empty\n'
    else:
        resp = msg
        return resp

app = default_app()
run(app, host="localhost", port=PORT)
