#!/usr/bin/env python

'''
  Front end Web server
'''

# Library packages
import os
import re
import sys
import json
import os.path

# Installed packages
import boto.sqs
import boto.sqs.message
from boto.sqs.message import Message

from bottle import route, run, request, response, abort, default_app

AWS_REGION = "us-west-2"
QUEUE_IN = "ex6_in"
QUERY_PATTERN = "^f=[0-9]+&s=[0-9]+$"
MAX_SECONDS = 180
REQ_ID_FILE = "reqid.txt"

PORT = 8080

query_pattern = re.compile(QUERY_PATTERN)

if not os.path.isfile(REQ_ID_FILE):
    with open(REQ_ID_FILE, 'w', 0) as req_file:
        req_file.write("0\n")

try:
    req_file = open(REQ_ID_FILE, 'r+', 0)
    request_count = int(req_file.readline())
except IOError as exc:
    sys.stderr.write("Exception reading request id file '{0}'\n".format(REQ_ID_FILE))
    sys.stderr.write(exc)
    sys.exit(1)

    
@route('/load')
def load():
    global request_count

    if not query_pattern.match(request.query_string):
        abort(400, "Query string does not match pattern '{0}'".format(QUERY_PATTERN))

    fraction = int(request.query.f)
    if fraction > 100:
        abort(400, "f greater than 100%: {0}".format(fraction))
    
    seconds = int(request.query.s)
    if seconds > MAX_SECONDS:
        abort(400, "s ({0}) greater than {1} seconds".format(seconds, MAX_SECONDS))

    '''
      EXTEND:
      Replace the following print with code that enqueues the request in
      JSON representation on the SQS queue.
    '''

    # 1) Create Dict 2) Create Message 3) Convert Dict to Json 4) Write Message to SQS QUEUE
    dict_sqs = {'request_count': request_count, 'fraction': fraction, 'seconds': seconds};
    m = Message()
    js = json.dumps(dict_sqs)
    m.set_body(js)
    q.write(m)
    #print ("\nfrontend.py received request {0}: {1}% for {2} seconds\n".format(request_count, fraction, seconds))
    
    request_count += 1
    req_file.seek(0)
    req_file.write(str(request_count))
    req_file.flush()
    os.fsync(req_file.fileno())
    
    response.status = 202 # "Accepted" (for later processing)
    return "Done\n"

try:
    conn = boto.sqs.connect_to_region(AWS_REGION)
    if conn == None:
        sys.stderr.write("Could not connect to AWS region '{0}'\n".format(AWS_REGION))
        sys.exit(1)

    '''
      EXTEND:
      Add code here to create the queue.
    '''
    q = conn.create_queue('kenny')

except Exception as e:
    sys.stderr.write("Exception connecting to SQS\n")
    sys.stderr.write(str(e))
    sys.exit(1)

app = default_app()
run(app, host="localhost", port=PORT)


    
