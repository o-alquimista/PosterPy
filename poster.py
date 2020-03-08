'''
PosterPy, a fixture creator for web applications.

Copyright 2019-2020 Douglas Silva (0x9fd287d56ec107ac)

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

import random, string, requests, argparse, configparser, logging
from bs4 import BeautifulSoup

class PosterPy:
    def __init__(self):
        parser = argparse.ArgumentParser(description='A fixture creator for web applications.')
        parser.add_argument('-u', '--user', help='The user to authenticate')
        parser.add_argument('-p', '--passwd', help='The authentication password')
        parser.add_argument('-n', '--num-payloads', type=int, default=100, help='The number of payloads to send (default: 100)')
        parser.add_argument('--login-csrf', help='Enable CSRF token support on login', action='store_true', default=False)
        parser.add_argument('--request-csrf', help='Enable CSRF token support on main request', action='store_true', default=False)
        parser.add_argument('--unique-field', help='Enable unique form field support', action='store_true', default=False)
        self.arguments = parser.parse_args()

        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.client = requests.Session()

        logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)

    def execute(self):
        if self.arguments.user and self.arguments.passwd:
            logging.info('Authenticating...')
            self.login()

        self.post()

    def login(self):
        url = self.config['login']['url']
        csrf_name = self.config['login']['csrf_name']
        first_credential = self.config['login_payload']['first_credential']
        second_credential = self.config['login_payload']['second_credential']

        payload = {
            first_credential:self.arguments.user,
            second_credential:self.arguments.passwd,
        }

        if self.arguments.login_csrf:
            logging.info('Login CSRF enabled.')

            soup = BeautifulSoup(self.client.get(url).text, 'html.parser')
            hidden_input = soup.find(attrs={'name': csrf_name})
            payload[csrf_name] = hidden_input['value']

        self.client.post(url=url, data=payload)

    def post(self):
        url = self.config['request']['url']
        csrf_name = self.config['request']['csrf_name']
        unique_form_field = self.config['request']['unique_field']

        payload = {}

        for form_field in self.config['payload']:
            payload[form_field] = self.config['payload'][form_field]

        if self.arguments.unique_field:
            logging.info('Unique form field set to %s', unique_form_field)

        if self.arguments.request_csrf:
            logging.info('Main request CSRF enabled.')

        for i in range(1, self.arguments.num_payloads + 1):
            if self.arguments.unique_field:
                random_slug = ''.join(random.choices(string.ascii_lowercase, k=8))
                payload[unique_form_field] = self.config['payload'][unique_form_field] + ' ' + random_slug

            if self.arguments.request_csrf:
                soup = BeautifulSoup(self.client.get(url).text, 'html.parser')
                hidden_input = soup.find(attrs={'name': csrf_name})
                payload[csrf_name] = hidden_input['value']

            self.client.post(url=url, data=payload)

            print('Item ' + str(i) + ' sent.', end='\r', flush=True)

        print(str(i) + ' items sent.')