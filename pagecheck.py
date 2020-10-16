import os
import requests
import time
import smtplib
from email.message import EmailMessage
import hashlib
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = os.environ.get("pagetocheck")
response = urlopen(url)
page = BeautifulSoup(response, 'html.parser')
shop = page.find('div', {"class": "products-flex-container"})
snapshot = str(shop)
currentHash = hashlib.sha224(snapshot.encode('utf-8')).hexdigest()
print("successfully hashed snapshot of shop")
print("snapshot: " + snaphsot)
print("Hash: " + currentHash)
        
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

            print("webpage-change-detected")
            msg = EmailMessage()
            msg.set_content(url)
            msg['From'] = 'arcadius.webster@googlemail.com'
            msg['To'] = 'acey.williams@googlemail.com'
            msg['Subject'] = 'York Ghost Merchants Shop: Change Detected'
            fromaddr = 'arcadius.webster@googlemail.com'
            toaddrs = ['acey.williams@googlemail.com']
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
            server.login('arcadius.webster@googlemail.com', os.environ.get("gmailpassword"))
            server.send_message(msg)
            server.quit()
            response = urlopen(url).read()
            currentHash = hashlib.sha224(response).hexdigest()
            time.sleep(30)
            continue

    except Exception as e:

        print(e)
        msg = EmailMessage()
        msg.set_content(url)
        msg['From'] = 'arcadius.webster@googlemail.com'
        msg['To'] = 'acey.williams@googlemail.com'
        msg['Subject'] = 'York Ghost Merchants Shop: NETWORK FAILURE' + e
        fromaddr = 'arcadius.webster@googlemail.com'
        toaddrs = ['acey.williams@googlemail.com']
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('arcadius.webster@googlemail.com', os.environ.get("gmailpassword"))
        server.send_message(msg)
        server.quit()
