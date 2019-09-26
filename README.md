# PosterPy
A fixture creator for blogs.

## Requirements
- [Python 3](https://www.python.org/)
- [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/)
- [Requests 2](https://requests.kennethreitz.org//en/master/)

## Usage
```
usage: poster.py [-h] [-u USER] [-p PASSWD]

A fixture creator for blogs

Optional arguments:
  -h, --help                  Show this help message and exit
  -u USER, --user USER        The user to authenticate
  -p PASSWD, --passwd PASSWD  The authentication password
```

## Configuration
The file [config.ini](https://github.com/o-alquimista/PosterPy/blob/master/config.ini)
comes with placeholder values to help you configure this tool. You are required to
configure that file before starting.

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