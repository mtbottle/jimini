#! /usr/bin/env python

import retrievemail
import os
import time
import subprocess
import poplib

import sendmail
 


print "Running Mail Parser and Mail Sender script"

orders = retrievemail.parseEmailAndFetchOrderInfo()
#print orders
for order in orders:
    print "Processing Order:" + str(order)
    print order['from']
    print order['to']
    print order.get('coupon',None)

    #construct the email
    subject = 'Your Origami is ready to print!'
    body = ''
    userMail = 'guruprasad.jg@gmail.com'
    fromMail = 'jimini.Origami@gmail.com'

    #send the email
    sendmail.send_jemini_email(fromMail, userMail, subject , body)


print "Done processing all orders!"
