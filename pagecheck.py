import os
import requests
import time
import smtplib
from email.message import EmailMessage
import hashlib
from urllib.request import urlopen

url = os.environ.get("pagetocheck")
response = urlopen(url).read()
currentHash = hashlib.sha224(response).hexdigest()

while True:

    try:

        response = urlopen(url).read()
        currentHash = hashlib.sha224(response).hexdigest()
        time.sleep(30)
        response = urlopen(url).read()
        newHash = hashlib.sha224(response).hexdigest()

        if newHash == currentHash:
            continue

        else:

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
            server.login('arcadius.webster@googlemail.com', '1926ArcadiusWebster5328')
            server.send_message(msg)
            server.quit()
            print("change-detected")
            response = urlopen(url).read()
            currentHash = hashlib.sha224(response).hexdigest()
            time.sleep(30)
            continue

    except Exception as e:

        msg = EmailMessage()
        msg.set_content(url)
        msg['From'] = 'arcadius.webster@googlemail.com'
        msg['To'] = 'acey.williams@googlemail.com'
        msg['Subject'] = 'York Ghost Merchants Shop: NETWORK FAILURE'
        fromaddr = 'arcadius.webster@googlemail.com'
        toaddrs = ['acey.williams@googlemail.com']
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login('arcadius.webster@googlemail.com', os.environ.get("gmailpassword"))
        server.send_message(msg)
        server.quit()
