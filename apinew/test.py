from lxml import html

import requests
import re

def get_price(url):
    r = requests.get(url, headers={
        'User-Agent':
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
            '(KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
    })
    r.raise_for_status()
    tree = html.fromstring(r.text)

    price_selector = "//*[@class='a-size-medium a-color-price']"
    try:
        # extract the price from the string
        price_string = re.findall('\d+.\d+', tree.xpath(price_selector)[0].text)[0]
        print float(price_string.replace(',', '.'))
    except IndexError, TypeError:
        print('Didn\'t find the \'price\' element, trying again later...')

    name_selector = "//*[@id='productTitle']"
    try:
        # extract the price from the string
        name_string = tree.xpath(name_selector)[0].text.strip()
        print name_string
    except IndexError, TypeError:
        print('Didn\'t find the \'name\' element, trying again later...')

    imagelink_selector = "//*[@id='imgTagWrapperId']/img/@data-old-hires"
    try:
        # extract the price from the string
        imagelink_string = tree.xpath(imagelink_selector)[0]
        print imagelink_string
    except IndexError, TypeError:
        print('Didn\'t find the \'imagelink\' element, trying again later...')

    imagelink_selector = "//li[@class='showHiddenFeatureBullets']/span[@class='a-list-item']/text()"
    try:
        # extract the price from the string
        for t in tree.xpath(imagelink_selector):
            imagelink_string = t.strip()
            print imagelink_string
    except IndexError, TypeError:
        print('Didn\'t find the \'imagelink\' element, trying again later...')

print get_price('https://www.amazon.com/dp/{0}/'.format('B072JWYC54'))


