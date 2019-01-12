import argparse
import sys
import os
import json
from dotenv import load_dotenv
import requests

BITLY_URL = 'https://api-ssl.bitly.com/v4'


def prepare_headers(token):
    bearer_token = f'Bearer {token}'
    headers = {
        'Authorization': bearer_token,
        'Content-type': 'application/json'
    }
    return headers


def check_bitly_authorization(headers):
    auth_bitly_url = f'{BITLY_URL}/user'
    response = requests.get(auth_bitly_url, headers=headers)
    return response.ok


def shorten_link(headers, url_to_shorten):
    shorten_bitly_url = f'{BITLY_URL}/shorten'

    request_body = json.dumps(
        {'long_url': url_to_shorten})

    response = requests.post(
        shorten_bitly_url,
        headers=headers,
        data=request_body)

    try:
        json_response = response.json()
    except ValueError as e:
        return None, f'Cannot parse response from bitly: {e}'

    if not response.ok:
        error_description = json_response.get('description', None)
        error_message = json_response.get('message', None)
        error_text = 'Error message: {}, error description: {}'
        error_text = error_text.format(error_message, error_description)
        return None, error_text

    shortened_link = json_response.get('link')
    shortened_link_res = f'Link has been generated: {shortened_link}'
    return shortened_link_res, None


def get_info_about_bitlink(headers, bitlink):
    bitlink = bitlink.strip('/').lstrip('http://')
    bitlink_info_bitly_url = f'{BITLY_URL}/bitlinks/{bitlink}'

    response = requests.get(bitlink_info_bitly_url, headers=headers)

    try:
        json_response = response.json()
    except ValueError as e:
        return None, f'Cannot parse response from bitly: {e}'

    if not response.ok:
        error_description = json_response.get('description', None)
        error_message = json_response.get('message', None)
        error_text = 'Error message: {}, error description: {}'
        error_text = error_text.format(error_message, error_description)
        return None, error_text

    return json_response, None


def get_click_summary_for_bitlink(headers, bitlink):
    bitlink = bitlink.strip('/').lstrip('http://')
    bitlink_click_summary_url = f'{BITLY_URL}/bitlinks/{bitlink}/clicks/summary'

    summary_response = requests.get(
        bitlink_click_summary_url,
        headers=headers,
        params={'units': -1, 'unit': 'day'})

    try:
        json_response = summary_response.json()
    except ValueError as e:
        return None, f'Cannot parse response from bitly: {e}'

    if not summary_response.ok:
        error_description = json_response.get('description', None)
        error_message = json_response.get('message', None)
        error_text = 'Error message: {}, error description: {}'
        error_text = error_text.format(error_message, error_description)
        return None, error_text

    clicks_res = json_response.get('total_clicks')
    res = f'Bitly link clicks total summary : {clicks_res}'
    return res, None


def process_user_input(auth_token, input_string):
    headers = prepare_headers(auth_token)

    if not check_bitly_authorization(headers):
        return None, 'Wrong credentials'

    bitlink_info, bitlink_info_error_msg = get_info_about_bitlink(
        headers,
        input_string)

    if bitlink_info is None:

        generated_bitlink, generated_bitlink_error_msg = shorten_link(
            headers,
            input_string)
        return generated_bitlink, generated_bitlink_error_msg

    else:

        click_summary, click_summary_error_msg = get_click_summary_for_bitlink(
            headers,
            input_string
        )
        return click_summary, click_summary_error_msg


def create_argument_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'url',
        type=str,
        help='Url to shorten or shortened url to get summary.')
    return parser


if __name__ == '__main__':
    load_dotenv()

    AUTH_TOKEN = os.getenv('auth_bitly_token')
    if AUTH_TOKEN is None:
        auth_token_required_error_message = '''
        Bitly auth token is not found.
        Please check auth_bitly_token environmental variable is exists.        
        '''
        sys.exit(auth_token_required_error_message)

    argument_parser = create_argument_parser()
    args = argument_parser.parse_args()

    result, error = process_user_input(AUTH_TOKEN, args.url)
    if result is None:
        sys.exit(error)
    print(result)
