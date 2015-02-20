#! /usr/env/python
# The most basic calculation app for Homeward Bound. 
# This one simply returns the given measurement.

import zmq;
import json;

version = 1;
storeAddress = "tcp://*:2002";
subscribeAddress = "tcp://127.0.0.1:2001";
subscribeTopic = "calculation_v"+str(version);
storeHeader = "StoreMeasurement";
headerLen = len(subscribeTopic);

# Create publish socket
context = zmq.Context();
pubSocket = context.socket(zmq.PUB);
pubSocket.bind(storeAddress);
print("Listening for calculation requests on "+subscribeAddress);

# Create subscribe socket
subSocket = context.socket(zmq.SUB);
subSocket.connect(subscribeAddress);
subSocket.setsockopt_string(zmq.SUBSCRIBE, subscribeTopic);

def createResponse(msg):
    start = msg.index(subscribeTopic)+headerLen;
    print("Measurement extracted: "+msg[start:]);
    return storeHeader+msg[start:];

 # On message, create the new message and publish it
try:
    while True:
        msgs = subSocket.recv_multipart();
        for msg in msgs:
            print('Received msg: '+str(msg));
            resp = createResponse(str(msg));
            pubSocket.send_string(resp);
        # Create response message
except KeyboardInterrupt:
    pass

   

print("Exiting...");
