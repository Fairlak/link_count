import requests
import os
import argparse
from urllib.parse import urlparse
from dotenv import load_dotenv


def shorten_link(token, url):  
  link_for_shorten = 'https://api-ssl.bitly.com/v4/shorten'
  body = {
    'long_url': url
  }
  headers = {
    'Authorization': 'Bearer {}'.format(token)
  }
  response = requests.post(link_for_shorten, headers=headers, json=body)
  response.raise_for_status()
  bitly_response = response.json()
  shorten_link = bitly_response['id']
  return shorten_link


def count_clicks(token, bitlink):
  parsed_bitlink = urlparse(bitlink)
  netloc = parsed_bitlink.netloc
  path = parsed_bitlink.path
  url = 'https://api-ssl.bitly.com/v4/bitlinks/{}{}/clicks/summary'.format(netloc, path)
  headers = {
    'Authorization': 'Bearer {}'.format(token)
  }
  response = requests.get(url, headers=headers)
  response.raise_for_status()
  return response.json()['total_clicks']

  
if __name__ == '__main__':
  load_dotenv()
  parser = argparse.ArgumentParser()
  parser.add_argument("full_link", help="link shortening")
  args = parser.parse_args()
  link = args.full_link
  bitly_token = os.getenv('BITLY_TOKEN')  
  try:
    try:      
      clicks_count = count_clicks(bitly_token, link)
      print(clicks_count)
    except requests.exceptions.HTTPError:
      bitlink = shorten_link(bitly_token, link)
      print(bitlink)
  except requests.exceptions.HTTPError:
    print('Неправильная ссылка')
