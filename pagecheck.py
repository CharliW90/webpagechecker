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
url = os.environ.get("page_tocheck")
divclass = os.environ.get("divclass_tocheck")
divclassexpectation = os.environ.get("expected_result")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
request = Request(url, headers=headers)
accountLoginURL = str(url + "/account/login")

def hash_fetch():
    global response
    response = urlopen(request)
    global page
    page = BeautifulSoup(response, 'html.parser')
    global shop
    shop = page.find('div', {"class": divclass})
    global snapshot
    snapshot = str(shop)
    global result
    result = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
    return result

newHash = hash_fetch()
print("Successfully hashed snapshot of the div class: " + divclass + " at " + url)
print("Hash: " + newHash)
print((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
startupPageContent = str(shop)

if startupPageContent != divclassexpectation
    print("App Deployed Succesfully but the startup page does not match expected page...")
    time.sleep(570)
    print("Rechecking startup page and expected page...")
    time.sleep(30)
    startupPageContent = str(shop)

while not (startupPageContent == divclassexpectation):
    print("Startup page does not match expected page!")
    time.sleep(570)
    print("Rechecking startup page and expected page...")
    time.sleep(30)
    startupPageContent = str(shop)
else:
    print("Startup Page Content matches expected page.  App deployed.")
    sms_ping("App Deployed Succesfully with startup page matching expected page.")

    hashes = 0
    errorcount = 0
    readfail = 0
    readsuccess = 0

    # account login
    with Session() as s:
        accountLogin = s.get(accountLoginURL)
        print(accountLogin)

    # begin loop to check page for changes
    while True:

        try:
            currentHash = newHash
            time.sleep(30)
            if not test_conn_open(server):
                logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                print("smtp client closed.  reconnecting... " + logdate)
                open_conn()
            newHash = hash_fetch()

            if newHash == currentHash:
                hashes += 1
                if hashes >= 100:
                    print("succesfully completed " + str(hashes) + " hashes")
                    hashes = 0
                if readfail > 0:
                    readsuccess += 1
                    if readsuccess >= 10:
                        readfail = 0
                        readsuccess = 0
                        print("Read Successful 10 Times :: Incomplete Read Count Reset")
                continue

            else:
                logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                prefix = str(url + ": Change Detected - ")
                header = prefix + logdate
                bodystring = str(shop)
                if str(shop) == defaultPageContent:
                    print("Page returned to empty.  Resuming monitoring.")
                    continue
                else:
                    print(header)
                    print("currentHash: " + currentHash)
                    print("newHash: " + newHash)
                    sms_ping(header)
                    if not test_conn_open(server):
                        logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                        print("smtp client closed.  reconnecting." + logdate)
                        open_conn()
                    msg = EmailMessage()
                    msg.set_content(bodystring)
                    msg['From'] = os.environ.get("gmail_send_account")
                    msg['To'] = os.environ.get("gmail_recipient_account")
                    msg['Subject'] = str(header)
                    server.send_message(msg)
                    response = urlopen(url)
                    page = BeautifulSoup(response, 'html.parser')
                    shop = page.find('div', {"class": os.environ.get("divclass_tocheck")})
                    snapshot = str(shop)
                    currentHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
                    time.sleep(150)
                    continue

        except http.client.IncompleteRead:

                readfail += 1
                logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                error = str("Incomplete Read #" + str(readfail) + ": ")
                print(error + logdate)
                if readfail >= 10:
                    logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                    prefix = str(url + ": Final Read Error - ")
                    suffix = str(": APP OFFLINE")
                    errormsg = str("10th Incomplete Read")
                    header = str(prefix + errormsg + suffix + " - " + logdate)
                    print(header)
                    print(errormsg)
                    if not test_conn_open(server):
                        logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                        print("smtp client closed.  reconnecting." + logdate)
                        open_conn()
                    msg = EmailMessage()
                    msg.set_content(errormsg)
                    msg['From'] = os.environ.get("gmail_send_account")
                    msg['To'] = os.environ.get("gmail_recipient_account")
                    msg['Subject'] = str(header)
                    server.send_message(msg)
                    server.quit()
                else:
                    continue

        except Exception as e:

                    print(e)
                    errorpageheaders = str(response.headers)
                    print("Page headers: " + errorpageheaders)
                    errorcount +=1
                    if errorcount < 10:
                        logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                        errornum = str(errorcount)
                        prefix = str(url + ": Error #" + errornum)
                        errormsg = str(e)
                        header = str(prefix + errormsg + " - " + logdate)
                        print(header)
                        print(errormsg)
                        if not test_conn_open(server):
                            logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                            print("smtp client closed.  reconnecting." + logdate)
                            open_conn()
                        msg = EmailMessage()
                        msg.set_content(errorpageheaders)
                        msg['From'] = os.environ.get("gmail_send_account")
                        msg['To'] = os.environ.get("gmail_recipient_account")
                        msg['Subject'] = str(header)
                        server.send_message(msg)
                        time.sleep(150)
                        continue
                    else:
                        logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                        prefix = str(url + ": Final Error - ")
                        suffix = str(": APP OFFLINE")
                        errormsg = str(e)
                        errordetail = str(page)
                        bodystring = str(errormsg + '\n' + errordetail)
                        header = str(prefix + errormsg + suffix + " - " + logdate)
                        print(header)
                        print(errormsg)
                        print(bodystring)
                        errorpageheaders = str(response.headers)
                        print("Page headers: " + errorpageheaders)
                        if not test_conn_open(server):
                            logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                            print("smtp client closed.  reconnecting." + logdate)
                            open_conn()
                        msg = EmailMessage()
                        msg.set_content(errorpageheaders)
                        msg['From'] = os.environ.get("gmail_send_account")
                        msg['To'] = os.environ.get("gmail_recipient_account")
                        msg['Subject'] = str(header)
                        server.send_message(msg)
                        server.quit()
