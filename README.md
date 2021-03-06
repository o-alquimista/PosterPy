# PosterPy
A fixture creator for web applications.

## Features
- Handles the CSRF token
- Optional user authentication
- Flexible payload configuration

## Requirements
- [Python 3](https://www.python.org/)
- [BeautifulSoup 4](https://www.crummy.com/software/BeautifulSoup/)
- [Requests 2](https://requests.readthedocs.io/en/master/)

## Usage
The file [config.ini](https://github.com/o-alquimista/PosterPy/blob/master/config/config.ini) allows you to configure this tool according to your web application and define the payloads. You must configure that file first, then run `main.py`. See `--help` for usage information.

```
python3 main.py -u username -p password -n 100 --login-csrf --request-csrf --unique-field
```

## License
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
