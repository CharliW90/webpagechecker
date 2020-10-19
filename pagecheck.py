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

server = smtplib.SMTP('smtp.gmail.com', 587)
server.starttls()
server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
server.login(os.environ.get("gmail_send_account"), os.environ.get("gmailpassword"))
fromaddr = [os.environ.get("gmail_send_account")]
toaddrs = [os.environ.get("gmail_recipient_account")]

def test_conn_open(server):
    try:
        status = server.noop()[0]
    except:  # smtplib.SMTPServerDisconnected
        status = -1
    return True if status == 250 else False

url = os.environ.get("page_tocheck")
divclass = os.environ.get("divclass_tocheck")
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
request = Request(url, headers=headers)
response = urlopen(request)
page = BeautifulSoup(response, 'html.parser')
shop = page.find('div', {"class": divclass})
snapshot = str(shop)
currentHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
print("Successfully hashed snapshot of the div class: " + divclass + " at " + url)
print("Hash: " + currentHash)
print((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
errorcount = 0
readfail = 0

while True:

    try:

        response = urlopen(url)
        page = BeautifulSoup(response, 'html.parser')
        shop = page.find('div', {"class": os.environ.get("divclass_tocheck")})
        snapshot = str(shop)
        currentHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
        if not test_conn_open(server):
            logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
            print("smtp client closed.  reconnecting." + logdate)
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(os.environ.get("gmail_send_account"), os.environ.get("gmailpassword"))
            fromaddr = [os.environ.get("gmail_send_account")]
            toaddrs = [os.environ.get("gmail_recipient_account")]
            continue
        time.sleep(30)
        response = urlopen(url)
        page = BeautifulSoup(response, 'html.parser')
        shop = page.find('div', {"class": os.environ.get("divclass_tocheck")})
        snapshot = str(shop)
        newHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()

        if newHash == currentHash:
            if readfail > 0:
                readfail -= 1
                continue
            else:
                continue

        else:
            logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
            prefix = str(url + ": Change Detected - ")
            header = prefix + logdate
            bodystring = str(shop)
            print(header)
            print("currentHash: " + currentHash)
            print("newHash: " + newHash)
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
                    msg = EmailMessage()
                    msg.set_content(page)
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
                    msg = EmailMessage()
                    msg.set_content(bodystring)
                    msg['From'] = os.environ.get("gmail_send_account")
                    msg['To'] = os.environ.get("gmail_recipient_account")
                    msg['Subject'] = str(header)
                    server.send_message(msg)
                    server.quit()
