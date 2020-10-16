import os
import requests
import time
import smtplib
from email.message import EmailMessage
import hashlib
from urllib.request import urlopen
from bs4 import BeautifulSoup
from datetime import datetime

url = os.environ.get("pagetocheck")
response = urlopen(url)
page = BeautifulSoup(response, 'html.parser')
shop = page.find('div', {"class": "products-flex-container"})
snapshot = str(shop)
currentHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
print("successfully hashed snapshot of shop")
print("Hash: " + currentHash)
print(datetime.now(gmt))
        
while True:

    try:

        response = urlopen(url)
        page = BeautifulSoup(response, 'html.parser')
        shop = page.find('div', {"class": "products-flex-container"})
        snapshot = str(shop)
        currentHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
        time.sleep(30)
        response = urlopen(url)
        page = BeautifulSoup(response, 'html.parser')
        shop = page.find('div', {"class": "products-flex-container"})
        snapshot = str(shop)
        newHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()

        if newHash == currentHash:
            continue

        else:

            logdate = str(datetime.now())
            prefix = str("York Ghost Merchants Shop: Change Detected -")
            header = prefix + " " + logdate
            print(header)
            print("currentHash: " + currentHash)
            print("newHash: " + newHash)
            msg = EmailMessage()
            msg.set_content(shop)
            msg['From'] = 'arcadius.webster@googlemail.com'
            msg['To'] = 'acey.williams@googlemail.com'
            msg['Subject'] = str(header)
            fromaddr = 'arcadius.webster@googlemail.com'
            toaddrs = ['acey.williams@googlemail.com']
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('arcadius.webster@googlemail.com', os.environ.get("gmailpassword"))
            server.send_message(msg)
            server.quit()
            response = urlopen(url)
            page = BeautifulSoup(response, 'html.parser')
            shop = page.find('div', {"class": "products-flex-container"})
            snapshot = str(shop)
            currentHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
            time.sleep(30)
            continue

    except Exception as e:

        print(e)
        logdate = str(datetime.now())
        prefix = str("York Ghost Merchants Shop: Error -")
        errormsg = str(e)
        header = prefix + " " + errormsg + " " + logdate
        msg = EmailMessage()
        msg.set_content(url)
        msg['From'] = 'arcadius.webster@googlemail.com'
        msg['To'] = 'acey.williams@googlemail.com'
        msg['Subject'] = str(header)
        fromaddr = 'arcadius.webster@googlemail.com'
        toaddrs = ['acey.williams@googlemail.com']
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('arcadius.webster@googlemail.com', os.environ.get("gmailpassword"))
        server.send_message(msg)
        server.quit()
