import os
import requests
from bs4 import BeautifulSoup
import smtplib

url = os.environ["PRODUCT_URL"]
expected_price = float(os.environ["PRODUCT_PRICE"])

response = requests.get(url, headers={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36 Edg/122.0.0.0',
    'Accept-Language': 'en-US,en;q=0.9'})

soup = BeautifulSoup(response.text, 'lxml')

price = soup.find("span",  class_="a-offscreen").getText()
price = float(price.split('$')[1])
title = soup.find('span', id="productTitle").getText()
title = title.strip()

email = os.environ.get('EMAIL_ADDRESS')
password = os.environ.get('EMAIL_PASSWORD')
to_email_address = os.environ.get("TO_EMAIL_ADDRESS")

if price < expected_price:
    with smtplib.SMTP('smtp.gmail.com', port=587) as connection:
        connection.starttls()
        result = connection.login(email, password)
        connection.sendmail(
            from_addr=email,
            to_addrs=to_email_address,
            msg=f"Subject:Amazon Price Alert!\n\n{title} is available at {price}\n{url}".encode("utf-8")
        )
