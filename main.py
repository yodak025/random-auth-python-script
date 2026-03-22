import base64
import sys
from typing import List
from argparse import ArgumentParser, Namespace

import requests


def parse_args(args: List) -> Namespace:
   parser = ArgumentParser(description="Our first program")
   parser.add_argument('-u', '--username', type=str, required=True)
   parser.add_argument('-p', '--password', type=str, required=True)

   return parser.parse_args(args)


def get_auth_header(username: str, password: str) -> str:
   encoded_auth_string = f"{username}:{password}".encode('ascii')
   b64_auth_string = base64.b64encode(encoded_auth_string)
   return f"Basic {b64_auth_string.decode('ascii')}"


def get_httpbin_data(username: str, password: str) -> dict:
   endpoint = f"https://httpbin.org/basic-auth/{username}/{password}"
   headers = {'Accept': 'application/json', 'Authorization': get_auth_header(username, password)}
   response = requests.get(endpoint, headers=headers)
   if response.ok:
       return response.json()

   raise RuntimeError("Unable to get response from server")


def main(args: List):
   parsed_args = parse_args(args)
   response = get_httpbin_data(parsed_args.username, parsed_args.password)
   print(response)


if __name__ == '__main__':
   main(sys.argv[1:])