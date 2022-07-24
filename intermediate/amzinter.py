import requests
from bs4 import BeautifulSoup

import csv
import logging


def http_client():
    session = requests.Session()
    session.headers.update(
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                          " AppleWebKit/537.36 (KHTML, like Gecko)"
                          "Chrome/74.0.3729.157 Safari/537.36"
        }
    )

    def log_url(res, *args, **kwargs):
        logging.info(f"{res.url}, {res.status_code}")

    session.hooks["response"] = log_url
    return session


def open_asins_from_file(filename: str):
    logging.info(f"opening {filename}")
    lines = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        for line in data:
            lines.append(line[0])
    return lines


def make_request(client, baseurl: str, asin: str):
    try:
        response = client.get(baseurl + asin)
    except requests.RequestException:
        logging.warning(f"HTTP Error for {asin}")
        return
    if response.status_code == 200:
        return response, asin


def extract_data(response: tuple):
    soup = BeautifulSoup(response[0].text, 'lxml')
    asin = response[1]
    try:
        item = (
            asin,
            soup.select_one("span#productTitle").text.strip(),
            soup.select_one("span.a-price span").text,
        )
        logging.info(f'scraped item successfully {item}')
        return item
    except AttributeError:
        logging.info(f"No Matching Selectors found for {asin}")
        item = (asin, "no data", "no data")
        return item


def save_to_csv(results: list):
    with open('results.csv', 'w') as f:
        csv_writer = csv.writer(f)
        for line in results:
            csv_writer.writerow(line)
    logging.info("saved file sucessfully")


def main():
    logging.basicConfig(filename='amzscraper.log', format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info(f"---starting new---")

    results = []
    client = http_client()
    baseurl = "https://www.amazon.co.uk/dp/"
    asins = open_asins_from_file('asins.csv')
    for asin in asins:
        html = make_request(client, baseurl, asin)
        if html is None:
            logging.info("passing due to make_request error")
        else:
            results.append(extract_data(html))
    save_to_csv(results)
    logging.info(f"---finished---")


if __name__ == '__main__':
    main()
