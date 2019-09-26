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
parser.add_argument("-n", type=int, default=100, help="The number of payloads to send (defaults to 100)")
parser.add_argument("--logincsrf", help="Enable CSRF token support on login", action="store_true", default=False)
parser.add_argument("--requestcsrf", help="Enable CSRF token support on main request", action="store_true", default=False)
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('../config/config.ini')

loginURL = config['login']['login_url']
loginCSRFName = config['login']['login_csrf_name']

requestURL = config['request']['request_url']
requestCSRFName = config['request']['request_csrf_name']

# Start a session
client = requests.Session()

def login(username, password, loginURL, csrfEnabled, loginCSRFName, client):
    payload = {
        'username':username,
        'password':password,
    }

    if csrfEnabled:
        print('[STATUS] Login CSRF enabled.')
        # Start scraping for the hidden field
        soup = BeautifulSoup(client.get(loginURL).text, 'html.parser')
        hiddenInput = soup.find(attrs={"name": loginCSRFName})
        payload[loginCSRFName] = hiddenInput['value']
    else:
        print('[STATUS] Login CSRF disabled.')

    client.post(url=loginURL, data=payload)
    return

def post(numberOfPayloads, requestURL, csrfEnabled, requestCSRFName, client):
    if csrfEnabled:
        print('[STATUS] Main request CSRF enabled.')
    else:
        print('[STATUS] Main request CSRF disabled.')

    for i in range(1, numberOfPayloads + 1):
        # Generate a random string used to circumvent the unique value constraint
        random_slug = ''.join(random.choices(string.ascii_lowercase, k=8))

        payload = {
            'post[title]':'How to Build Python from Source '+random_slug,
            'post[summary]':'Installing Python is easy using the pre-built installers and packages from your operating system. However, if you want to build the cutting-edge version directly from GitHub master branch, you will have to build your own version from source. You may also want to do it just to reinforce your understanding of Python. This guide will walk through the steps needed to build Python 3 from source and then create a virtual environment that you can use for projects.',
            'post[body]':'Installing Python is easy using the pre-built installers and packages from your operating system. However, if you want to build the cutting-edge version directly from GitHub master branch, you will have to build your own version from source. You may also want to do it just to reinforce your understanding of Python. This guide will walk through the steps needed to build Python 3 from source and then create a virtual environment that you can use for projects.',
        }

        if csrfEnabled:
            # Start scraping for the hidden field
            soup = BeautifulSoup(client.get(requestURL).text, 'html.parser')
            hiddenInput = soup.find(attrs={"name": requestCSRFName})
            payload[requestCSRFName] = hiddenInput['value']

        client.post(url=requestURL, data=payload)

        print('Item ' + str(i) + ' sent.', end='\r', flush=True)

    print(str(i) + ' items sent.')
    return

# User authentication
if args.user and args.passwd:
    print('[STATUS] Authenticating...')
    login(args.user, args.passwd, loginURL, args.logincsrf, loginCSRFName, client)
else:
    print('[STATUS] Authentication disabled.')

# Execute main request
post(args.n, requestURL, args.requestcsrf, requestCSRFName, client)