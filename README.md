# PosterPy
A fixture creator for web applications (primarily for blogs).

### Features
- Handles the CSRF token
- Optional user authentication

## Requirements
- [Python 3](https://www.python.org/)
- [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/)
- [Requests 2](https://requests.kennethreitz.org//en/master/)

## Usage
```
usage: poster.py [-h] [-u USER] [-p PASSWD] [-n N] [--logincsrf] [--requestcsrf]

A fixture creator for blogs.

optional arguments:
  -h, --help                  show this help message and exit
  -u USER, --user USER        The user to authenticate
  -p PASSWD, --passwd PASSWD  The authentication password
  -n N                        The number of payloads to send (defaults to 100)
  --logincsrf                 Enable CSRF token support on login
  --requestcsrf               Enable CSRF token support on main request
```

## Configuration
The file [config.ini](https://github.com/o-alquimista/PosterPy/blob/master/config.ini)
allows you to configure this tool according to your web application. You must
configure that file before PosterPy can perform its function.

## License
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