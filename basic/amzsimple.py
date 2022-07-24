import requests
from bs4 import BeautifulSoup

url = "https://www.amazon.co.uk/dp/B07TYQTTYQ"

headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        " AppleWebKit/537.36 (KHTML, like Gecko)"
        "Chrome/74.0.3729.157 Safari/537.36"
    }

resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "lxml")

item = {
    "name": soup.select_one("span#productTitle").text.strip(),
    "price": soup.select_one("span.a-price span").text,
}

print(item)
