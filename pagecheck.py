import os
import requests
import time
import smtplib
from email.message import EmailMessage
import hashlib
from urllib.request import urlopen
from bs4 import BeautifulSoup

url = os.environ.get("pagetocheck")

# Connect to the website and return the html to the variable ‘page’
try:
    page = urlopen(url)
except:
    print("Error opening the URL")

# parse the html using beautiful soup and store in variable `soup`
soup = BeautifulSoup(page, 'html.parser')

# Take out the <div> of name and get its value
content = soup.find('div', {"class": "products-flex-container"})

print(content)
