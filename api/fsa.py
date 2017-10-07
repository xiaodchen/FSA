import webapp2, jinja2, os, time, re, hmac, hashlib, random
from string import letters
from google.appengine.ext import db
import requests
import re
from lxml import html


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
def gql_json_parser(query_obj):
    result = []
    for entry in query_obj:
        result.append(dict([(p, unicode(getattr(entry, p))) for p in entry.properties()]))
    return result

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

def get_parameters(url):
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
        price_string = float(price_string.replace(',', '.'))
    except IndexError, TypeError:
        print('Didn\'t find the \'price\' element, trying again later...')

    name_selector = "//*[@id='productTitle']"
    try:
        # extract the price from the string
        name_string = tree.xpath(name_selector)[0].text.strip()
        name_string = name_string.encode('utf8')
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

    description_selector = "//li[@class='showHiddenFeatureBullets']/span[@class='a-list-item']/text()"
    description_string = []
    try:
        # extract the price from the string
        for t in tree.xpath(description_selector):
            description_string.append(t.strip())
            print description_string
    except IndexError, TypeError:
        print('Didn\'t find the \'description\' element, trying again later...')

    return (imagelink_string, name_string, price_string, description_string)

def newFSAItem(productKey, category): 
	link = 'https://www.amazon.com/dp/{0}/'.format(productKey)
	imagelink, name, price, description = get_parameters(link)

	item = FSAItems(link = link,
					imagelink = imagelink, 
					name = name, 
					price = price, 
					category = category, 
					description = description)
	item.put()
	return item.key().id()

class FSAItems(db.Model):
	link = db.LinkProperty()
	imagelink = db.LinkProperty()
	name = db.TextProperty(required = True)
	price = db.FloatProperty(required = True)
	category = db.StringProperty()
	description = db.StringListProperty()
	created = db.DateTimeProperty(auto_now_add = True)
	last_modified = db.DateTimeProperty(auto_now = True)

	def render(self):
		# self._render_text = self.description.replace('\n', '<br>')
		# print '@@@@@@@', self._render_text 
		return render_str("post.html", p = self)

class FSAHandler(webapp2.RequestHandler): 

	def write(self, *a, **kw): 
		self.response.out.write(*a, **kw)

	def render(self, template, **kw): 
		self.write(self.render_str(template, **kw))

	def render_str(self, template, **params):
		t = jinja_env.get_template(template)
		return t.render(**params)

class MainPage(FSAHandler): 
	def get(self, *args, **kwargs): 
		import json
		allFSAItems = list(FSAItems.all().order('-created'))

		allFSAItemsStr = gql_json_parser(allFSAItems)
		print json.dumps(allFSAItemsStr)
		self.render('front.html', 
					allFSAItems = allFSAItems, allFSAItemsStr=json.dumps(allFSAItemsStr))

	def post(self, *args, **kwargs): 
		productKey = self.request.get('productKey')
		category = self.request.get('category')

		print '@@@@@@@@@@', productKey, category
		FSAItem_id = newFSAItem(productKey, category)
		time.sleep(0.1)
		self.redirect('/')


app = webapp2.WSGIApplication([('/', MainPage), 
							   ], 
							   debug=True)
