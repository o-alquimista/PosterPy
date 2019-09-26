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

parser = argparse.ArgumentParser(description="A fixture creator for blogs")
parser.add_argument("-u", "--user", help="The user to authenticate")
parser.add_argument("-p", "--passwd", help="The authentication password")
args = parser.parse_args()

config = configparser.ConfigParser()
config.read('../config/config.ini')

loginURL = config['request.data']['loginURL']
requestURL = config['request.data']['requestURL']

# Start a session
client = requests.Session()

def login(username, password, loginURL, client):
    # Start scraping for the hidden field
    soup = BeautifulSoup(client.get(loginURL).text, 'html.parser')
    hidden_input = soup.find(id="login__token")
    csrf_token = hidden_input['value']

    payload = {
      'username':username,
      'password':password,
      '_csrf_token':csrf_token,
    }

    # Authenticate
    client.post(url=loginURL, data=payload)
    return

if args.user and args.passwd:
    username = args.user
    password = args.passwd
    login(username, password, loginURL, client)

# The fixture creation loop
for i in range(1, 101):
    # Start scraping for the hidden field
    soup = BeautifulSoup(client.get(requestURL).text, 'html.parser')
    hidden_input = soup.find(id="post__token")
    csrf_token = hidden_input['value']

    # Generate a random string used to circumvent the unique value constraint
    random_slug = ''.join(random.choices(string.ascii_lowercase, k=6))

    payload = {
      'post[title]':'How to Build Python from Source '+random_slug,
      'post[summary]':'Installing Python is easy using the pre-built installers and packages from your operating system. However, if you want to build the cutting-edge version directly from GitHub master branch, you will have to build your own version from source. You may also want to do it just to reinforce your understanding of Python. This guide will walk through the steps needed to build Python 3 from source and then create a virtual environment that you can use for projects.',
      'post[body]':'Installing Python is easy using the pre-built installers and packages from your operating system. However, if you want to build the cutting-edge version directly from GitHub master branch, you will have to build your own version from source. You may also want to do it just to reinforce your understanding of Python. This guide will walk through the steps needed to build Python 3 from source and then create a virtual environment that you can use for projects.',
      'post[_token]':csrf_token,
    }

    # Execute request
    client.post(url=requestURL, data=payload)
    print('Item '+str(i)+' published.')

print('All items published.')