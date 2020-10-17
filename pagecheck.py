import os
import requests
import time
import smtplib
from email.message import EmailMessage
import hashlib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime
from datetime import timedelta

url = os.environ.get("page_tocheck")
response = urlopen(url)
page = BeautifulSoup(response, 'html.parser')
shop = page.find('div', {"class": os.environ.get("divclass_tocheck")})
snapshot = str(shop)
currentHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
print("successfully hashed snapshot of shop")
print("Hash: " + currentHash)
print((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
errorcount = 0
        
while True:

    try:

        response = urlopen(url)
        page = BeautifulSoup(response, 'html.parser')
        shop = page.find('div', {"class": os.environ.get("divclass_tocheck")})
        snapshot = str(shop)
        currentHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
        time.sleep(60)
        response = urlopen(url)
        page = BeautifulSoup(response, 'html.parser')
        shop = page.find('div', {"class": os.environ.get("divclass_tocheck")})
        snapshot = str(shop)
        newHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()

        if newHash == currentHash:
            continue

        else:

            logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
            prefix = str("York Ghost Merchants Shop: Change Detected - ")
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
            fromaddr = [os.environ.get("gmail_send_account")]
            toaddrs = [os.environ.get("gmail_recipient_account")]
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login(os.environ.get("gmail_send_account"), os.environ.get("gmailpassword"))
            server.send_message(msg)
            server.quit()
            response = urlopen(url)
            page = BeautifulSoup(response, 'html.parser')
            shop = page.find('div', {"class": os.environ.get("divclass_tocheck")})
            snapshot = str(shop)
            currentHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
            time.sleep(300)
            continue
    
    except (http.client.IncompleteRead) as e:
        
            logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
            error = str("Incomplete Read: ")
            print(error + logdate)
            continue
        
    except Exception as e:

                print(e)
                errorcount +=1
                if errorcount < 10:
                    logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                    errornum = str(errorcount)
                    prefix = str("York Ghost Merchants Shop: Error #" + errornum)
                    errormsg = str(e)
                    header = str(prefix + errormsg + " - " + logdate)
                    print(header)
                    print(errormsg)
                    print(bodystring)
                    msg = EmailMessage()
                    msg.set_content(page)
                    msg['From'] = os.environ.get("gmail_send_account")
                    msg['To'] = os.environ.get("gmail_recipient_account")
                    msg['Subject'] = str(header)
                    fromaddr = [os.environ.get("gmail_send_account")]
                    toaddrs = [os.environ.get("gmail_recipient_account")]
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.login(os.environ.get("gmail_send_account"), os.environ.get("gmailpassword"))
                    server.send_message(msg)
                    server.quit()
                    time.sleep(300)
                    continue
                else:
                    logdate = str((datetime.now() + timedelta(hours=1)).strftime("%Y-%m-%d %H:%M:%S"))
                    prefix = str("York Ghost Merchants Shop: Final Error - ")
                    suffix = str(": APP OFFLINE")
                    errormsg = str(e)
                    errordetail = str(page)
                    bodystring = str(errormsg + '\n' + errordetail)
                    header = str(prefix + errormsg + suffix + " - " + logdate)
                    print(header)
                    print(errormsg)
                    print(bodystring)
                    msg = EmailMessage()
                    msg.set_content(bodystring)
                    msg['From'] = os.environ.get("gmail_send_account")
                    msg['To'] = os.environ.get("gmail_recipient_account")
                    msg['Subject'] = str(header)
                    fromaddr = [os.environ.get("gmail_send_account")]
                    toaddrs = [os.environ.get("gmail_recipient_account")]
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.starttls()
                    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
                    server.login(os.environ.get("gmail_send_account"), os.environ.get("gmailpassword"))
                    server.send_message(msg)
                    server.quit()
