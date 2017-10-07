from lxml import html

import requests
import re
selector = "//*[@id='priceblock_ourprice']"
def get_price(url):
    r = requests.get(url, headers={
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    })
    r.raise_for_status()
    tree = html.fromstring(r.text)
    try:
        # extract the price from the string
        price_string = re.findall('\d+.\d+', tree.xpath(selector)[0].text)[0]
        return float(price_string.replace(',', '.'))
    except IndexError, TypeError:
        print('Didn\'t find the \'price\' element, trying again later...')

print get_price('https://www.amazon.com/dp/B00KPQB2SS/')