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
        logging.info(res.url)

    def check_status(res, *args, **kwargs):
        res.raise_for_status()

    session.hooks["response"] = log_url, check_status
    return session


def open_asins_from_file(filename):
    logging.info(f"opening {filename}")
    lines = []
    with open(filename, newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
        for line in data:
            lines.append(line[0])
    return lines


def make_request(client, baseurl, asin):
    try:
        response = client.get(baseurl + asin)
    except:
        logging.warning(f"HTTP Error for {asin}")
        return
    return response, asin


def extract_data(response):
    soup = BeautifulSoup(response[0].text, 'lxml')
    asin = response[1]
    item = (
        asin,
        soup.select_one("span#productTitle").text.strip(),
        soup.select_one("span.a-price span").text,
    )
    logging.info(f'scraped item sucessfully {item}')
    return item


def save_to_csv(results):
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


