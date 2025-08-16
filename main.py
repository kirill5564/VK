import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
import os
import argparse


def shorten_link(token, url):
    payload = {"v": 5.199,
               "access_token": token,
               "url": url}
    response = requests.get("https://api.vk.ru/method/utils.getShortLink",
                            params=payload)
    response.raise_for_status()
    return response.json()["response"]["short_url"]


def count_clicks(token, url):
    parsed = urlparse(url)
    key = parsed.path[1:]
    payload = {"v": 5.199,
               "access_token": token,
               "url": url,
               "key": key,
               "interval": "forever"}
    response = requests.get("https://api.vk.ru/method/utils.getLinkStats",
                            params=payload)
    response.raise_for_status()
    return response.json()["response"]["stats"][0]["views"]


def is_shorten_link(token, url):
    parsed = urlparse(url)
    if parsed.netloc != "vk.cc":
        return False
    try:
        count_clicks(token, url)
        return True
    except KeyError:
        return False


if __name__ == '__main__':
    load_dotenv()
    token = os.environ["VK_TOKEN"]
    parser = argparse.ArgumentParser(description='Сокращение ссылок VK')
    parser.add_argument('url', help='URL для обработки')
    args = parser.parse_args()
    try:
        if is_shorten_link(token, args.url):
            print("Количество переходов:", count_clicks(token, args.url))
        else:
            print("Сокращенная ссылка:", shorten_link(token, args.url))
    except KeyError:
        print("Неправильная ссылка")


