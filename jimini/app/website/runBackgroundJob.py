#! /usr/bin/env python

import retrievemail
import os
import time
import subprocess

print "Running Mail Parser and Mail Sender script"

#while 1==1:
#print "inside loop"
#time.sleep(2)

print "inside loop"
time.sleep(2)

orderInfo = retrievemail.parseEmailAndFetchOrderInfo()
print orderInfo

print "Oh!! I got killed, somebody restart me!"
