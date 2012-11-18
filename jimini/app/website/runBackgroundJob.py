#! /usr/bin/env python

import retrievemail
import os
import time
import subprocess
import poplib

import sendmail
import re
 
def fetchGeneratedMail(emailString):
    splits = re.split('@', emailString)
    userId = splits[0].replace("\"","") 
    return  userId + '@jimini.co'


def fetchUserMailForGeneratedMail(generatedEmail):
    userMail = 'guruprasad.jg@gmail.com'
    return userMail

def fetchBody(coupon):
    if coupon is not None:
        url = 'www.jimini.co/rap/'+coupon
    else:
        url = 'www.jimini.co'
    body = 'Find your origami here: '+url
    return body 

print "Running Mail Parser and Mail Sender script"

orders = retrievemail.parseEmailAndFetchOrderInfo()
for order in orders:
    print "Processing Order:" + str(order)
    generatedMail = fetchGeneratedMail(order['to'])
    userMail = fetchUserMailForGeneratedMail(generatedMail)
    
    #print order['to']
    coupon= order.get('coupon',None)

    #construct the email
    subject = 'Your Origami is ready to print!'
    body =  fetchBody(coupon)
    fromMail = 'jimini.Origami@gmail.com'

    #send the email
    sendmail.send_jemini_email(fromMail, userMail, subject , body)

print "Done processing all orders!"
