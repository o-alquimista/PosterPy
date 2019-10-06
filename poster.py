#!/usr/bin/env python3

'''
PosterPy, a fixture creator for blogs.

Copyright 2019 Douglas Silva (0x9fd287d56ec107ac)

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
'''

import random, string, requests, argparse, configparser
from bs4 import BeautifulSoup

parser = argparse.ArgumentParser(description="A fixture creator for blogs.")
parser.add_argument("-u", "--user", help="The user to authenticate")
parser.add_argument("-p", "--passwd", help="The authentication password")
parser.add_argument("-n", "--num-payloads", type=int, default=100, help="The number of payloads to send (default: 100)")
parser.add_argument("--login-csrf", help="Enable CSRF token support on login", action="store_true", default=False)
parser.add_argument("--request-csrf", help="Enable CSRF token support on main request", action="store_true", default=False)
parser.add_argument("--unique-field", help="Enable unique form field support", action="store_true", default=False)
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('config.ini')

# Start a session
client = requests.Session()

def login(user, password, csrfEnabled, client, config):
    url = config['login']['login_url']
    csrfName = config['login']['login_csrf_name']
    firstCredential = config['login_payload']['first_credential']
    secondCredential = config['login_payload']['second_credential']

    payload = {
        firstCredential:user,
        secondCredential:password,
    }

    if csrfEnabled:
        print('[STATUS] Login CSRF enabled.')

        # Start scraping for the hidden field
        soup = BeautifulSoup(client.get(url).text, 'html.parser')
        hiddenInput = soup.find(attrs={"name": csrfName})
        payload[csrfName] = hiddenInput['value']

    client.post(url=url, data=payload)

def post(numberOfPayloads, csrfEnabled, uniqueFieldEnabled, client, config):
    url = config['request']['request_url']
    csrfName = config['request']['request_csrf_name']
    uniqueFormField = config['request']['unique_field']

    payload = {}

    # Retrieve the payload
    for formField in config['payload']:
        payload[formField] = config['payload'][formField]

    if uniqueFieldEnabled:
        print('[STATUS] Unique form field set to "' + uniqueFormField + '"')

    if csrfEnabled:
        print('[STATUS] Main request CSRF enabled.')

    for i in range(1, numberOfPayloads + 1):
        if uniqueFieldEnabled:
            # A random string guarantees that the chosen value will always be unique
            random_slug = ''.join(random.choices(string.ascii_lowercase, k=8))
            payload[uniqueFormField] = config['payload'][uniqueFormField] + ' ' + random_slug

        if csrfEnabled:
            # Start scraping for the hidden field
            soup = BeautifulSoup(client.get(url).text, 'html.parser')
            hiddenInput = soup.find(attrs={"name": csrfName})
            payload[csrfName] = hiddenInput['value']

        client.post(url=url, data=payload)

        print('Item ' + str(i) + ' sent.', end='\r', flush=True)

    print(str(i) + ' items sent.')

# User authentication
if args.user and args.passwd:
    print('[STATUS] Authenticating...')
    login(args.user, args.passwd, args.login_csrf, client, config)

# Execute main request
post(args.num_payloads, args.request_csrf, args.unique_field, client, config)