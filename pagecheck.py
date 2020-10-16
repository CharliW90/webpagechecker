import os
import requests
import time
import smtplib
from email.message import EmailMessage
import hashlib
from urllib.request import urlopen
from requests_html import HTMLSession

url = os.environ.get("pagetocheck")
session = HTMLSession()
response = session.get(url)
shop = response.html.xpath(/html/body/div[1]/main/article/section[2]/div[2]/div/section/div[2])
print(shop)
currentHash = hashlib.sha224(shop).hexdigest() 

while True:

    try:

        session = HTMLSession()
        response = session.get(url)
        shop = response.html.xpath(/html/body/div[1]/main/article/section[2]/div[2]/div/section/div[2])
        print(shop)
        currentHash = hashlib.sha224(shop).hexdigest()
        time.sleep(30)
        shop = response.html.xpath(/html/body/div[1]/main/article/section[2]/div[2]/div/section/div[2])
        newHash = hashlib.sha224(shop).hexdigest()

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
