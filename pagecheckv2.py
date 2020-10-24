import os
import requests
import http.client
import time
import smtplib
from email.message import EmailMessage
import hashlib
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta
from twilio.rest import Client

# heroku deployment stage
time.sleep(30)

# gmail connection stage
def open_conn():
    global server
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(os.environ.get("gmail_send_account"), os.environ.get("gmailpassword"))
    global fromaddr
    fromaddr = [os.environ.get("gmail_send_account")]
    global toaddrs
    toaddrs = [os.environ.get("gmail_recipient_account")]
    logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
    print("smtp client opened: " + logdate)
    
open_conn()

# test gmail connection...

def test_conn_open(server):
    try:
        status = server.noop()[0]
    except:  # smtplib.SMTPServerDisconnected
        status = -1
    return True if status == 250 else False

if not test_conn_open(server):
    logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
    print("smtp client failed at startup.  reconnecting... " + logdate)
    open_conn()
else:
    logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
    print("smtp client succesfully logged in: " + logdate)

# prepare twilio connection
Twilio_Account_SID = os.environ.get("Twilio_Account_SID") 
Twilio_Auth_Token = os.environ.get("Twilio_Auth_Token")
recipient_num = os.environ.get("recipients_mobile_number")
sender_num = os.environ.get("twilio_mobile_number")

def sms_ping(message):
    twilio_client = Client(Twilio_Account_SID, Twilio_Auth_Token)
    twilio_client.messages.create(to=recipient_num, 
                           from_=sender_num, 
                           body="Webpage Checker Ping! " + message)

# prepare variables
baseurl = os.environ.get("page_tocheck")
pageurl = os.environ.get("item_tocheck")
divclass = os.environ.get("divclass_tocheck")
url = baseurl + pageurl
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
request = Request(url, headers=headers)
accountLoginURL = str(baseurl + "/account/login")
attempts = 0

def page_fetch():
    global response
    response = urlopen(request)
    global page
    page = BeautifulSoup(response, 'html.parser')
    global shop
    shop = page.find('div', {"class": divclass})
    global snapshot
    snapshot = str(shop)
    return snapshot

while True:
    try:
        page_fetch()
        print("Page Found!")
        time.sleep(120)
        continue
    except Exception as e:
        if e.code == 404:
            attempts += 1
            if attempts >= 120:
                print("120 unsuccessful attempts. Continuing...")
                attempts = 0
            time.sleep(30)
