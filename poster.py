import random, string, requests
from bs4 import BeautifulSoup

# The URL of the request
url = 'http://devdungeon.org/admin/new'

for i in range(1, 101):
    # Starts a session
    client = requests.Session()

    # Parse the response from the URL
    soup = BeautifulSoup(client.get(url).text, 'html.parser')

    # Retrieve the CSRF token
    hidden_input = soup.find(id="post__token")
    csrf_token = hidden_input['value']

    # Generate a random string used to circumvent unique value requirement
    random_slug = ''.join(random.choices(string.ascii_lowercase, k=6))

    # The data to be posted
    payload = {
      'post[title]':'How to Build Python from Source '+random_slug,

      'post[summary]':'Installing Python is easy using the pre-built installers and packages from your operating system. However, if you want to build the cutting-edge version directly from GitHub master branch, you will have to build your own version from source. You may also want to do it just to reinforce your understanding of Python. This guide will walk through the steps needed to build Python 3 from source and then create a virtual environment that you can use for projects.',

      'post[body]':'Installing Python is easy using the pre-built installers and packages from your operating system. However, if you want to build the cutting-edge version directly from GitHub master branch, you will have to build your own version from source. You may also want to do it just to reinforce your understanding of Python. This guide will walk through the steps needed to build Python 3 from source and then create a virtual environment that you can use for projects.',

      'post[_token]':csrf_token,
    }

    # Post it
    client.post(url=url, data=payload)

    print('Item '+str(i)+' published.')
