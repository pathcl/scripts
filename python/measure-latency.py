#!/usr/bin/env python3
# You'll need BeautifulSoup
try:

    from bs4 import BeautifulSoup
    import requests
    import re
    import sys
    
except ImportError:
    print("please check your modules")
    

def main(url):
    """ Submits your domain to bytecheck.com and then extract info
    """
    payload = {'domain':url}
    post = requests.post('http://www.bytecheck.com', data=payload)
    soup = BeautifulSoup(post.text, 'html.parser')
    text = (soup.get_text(separator=' ', strip=True))
    result = re.findall(r'\w+.\w+.\d+.\d+', text)
    print(result)


if __name__ == '__main__':
    if len(sys.argv) <= 1:
        print("Usage: ./measure-latency.py www.trololo.com")
    else:
        url = sys.argv[1]
        main(url)
