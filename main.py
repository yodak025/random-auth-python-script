import base64
import sys
from typing import List
from argparse import ArgumentParser, Namespace

import requests
import logging


def parse_args(args: List) -> Namespace:
    parser = ArgumentParser(description="Our first program")
    parser.add_argument('-u', '--username', type=str, required=False)
    parser.add_argument('-p', '--password', type=str, required=False)
    parser.add_argument('-s', '--save', type=str, required=False)
    parser.add_argument('-v', '--verbose', type=bool, required=False, default=False)
    return parser.parse_args(args)


def get_logger(verbose: bool) -> logging.Logger:
    if not verbose:
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')
    return logging.getLogger(__name__)


def get_random_auth(logger):
    endpoint = 'https://randomuser.me/api/'
    response = requests.get(endpoint)
    if response.ok:
        data = response.json()
        logger.debug(f"Received data: {data}")
        user = data["results"][0]["login"]
        return user['username'], user['password']


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
    logger = get_logger(parsed_args.verbose)

    if not parsed_args.username or not parsed_args.password:
        logger.info("Username or password not provided, fetching random credentials")
        try:
            parsed_args.username, parsed_args.password = get_random_auth(logger)
        except Exception as e:
            logger.error(f"Failed to fetch random credentials: {e}")
            logger.info("Please provide username and password using -u and -p flags")
            return
    else:
        logger.info("Using provided username and password")

    try:
        response = get_httpbin_data(parsed_args.username, parsed_args.password)
    except RuntimeError:
        logger.error("Failed to get data from httpbin.org. Server could be down, please try again later.")

    if parsed_args.save:
        try:
            with open(parsed_args.save, 'w') as f:
                f.write(str(response))
            logger.info(f"Response saved to {parsed_args.save}")
        except Exception as e:
            logger.error(f"Failed to save response to file: {e}")

    print(response)


if __name__ == '__main__':
    main(sys.argv[1:])
