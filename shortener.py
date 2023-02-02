import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(bitly_token, url):
    bitly_headers = {'Authorization': 'Bearer {}'.format(bitly_token)}
    url_for_post = {"long_url": url}
    link = 'https://api-ssl.bitly.com/v4/shorten'
    response = requests.post(link, headers=bitly_headers, json=url_for_post)
    response.raise_for_status()
    return response.json()['id']


def count_clicks(bitly_token, url):
    bitly_headers = {'Authorization': 'Bearer {}'.format(bitly_token)}
    parsed_url = urlparse(url)
    link = ('https://api-ssl.bitly.com/v4/bitlinks/{}{}/clicks/summary'.format(
            parsed_url.netloc, parsed_url.path))
    response = requests.get(link, headers=bitly_headers)
    response.raise_for_status()
    return response.json()['total_clicks']


def is_bitlink(bitly_token, url):
    bitly_headers = {'Authorization': 'Bearer {}'.format(bitly_token)}
    parsed_url = urlparse(url)
    check_link = ('https://api-ssl.bitly.com/v4/bitlinks/{}{}'.format(
        parsed_url.netloc, parsed_url.path))
    return requests.get(check_link, headers=bitly_headers).ok


if __name__ == "__main__":
    load_dotenv()
    parser = argparse.ArgumentParser(description='Выдает количество кликов на bit.ly или формирует bit.ly ссылку')
    parser.add_argument('url', help='ссылка bit.ly или ссылка для сокращения')
    args = parser.parse_args()
    start_url = args.url
    bitly_token = os.environ['TOKEN']
    #start_url = input('input your url: ')
    if is_bitlink(bitly_token, start_url):
        try:
            print('Количество кликов', count_clicks(bitly_token, start_url))
        except requests.exceptions.HTTPError:
            print('Wrong bitlink url input')
    else:
        try:
            print('Битлинк', shorten_link(bitly_token, start_url))
        except requests.exceptions.HTTPError:
            print('Wrong url input')
