import time
import re
from selenium.webdriver.common.keys import Keys

class Grocery(object):

	def __init__(self, name, brand, supermarket, weight, price, pricePerUnit, unit):
		self.name 	= name
		self.brand  = brand
		self.supermarket = supermarket
		self.weight = weight
		self.price  = price
		self.pricePerUnit = pricePerUnit
		self.unit = unit

def load_all_items(driver):
	'''
	Scroll down all the way in order to load all the items in the category.
	'''

	time.sleep(1)

	SCROLL_PAUSE_TIME = 0.6

	# Get scroll height
	last_height = driver.execute_script("return document.body.scrollHeight")

	while True:
		# Scroll down to bottom
		driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

		# Wait to load page
		time.sleep(SCROLL_PAUSE_TIME)

		# Calculate new scroll height and compare with last scroll height
		new_height = driver.execute_script("return document.body.scrollHeight")
		if new_height == last_height:
			break
		last_height = new_height


def collect_data(driver):
	'''
	Store the relevant fields in lists for each category.
	'''

	# Collect product name
	products_name = [elem.text for elem in driver.find_elements_by_class_name('name')]
	# Collect product brand
	products_brand = [elem.text for elem in driver.find_elements_by_class_name('brand')]
	# Collect supermarket
	products_supermarket = [elem.text.replace('\n', ' ') for elem in driver.find_elements_by_class_name('has-supplier-icons')]
	# Collect product weight
	products_weight = [elem.text for elem in driver.find_elements_by_class_name('measure')]
	# Collect product price
	products_price = [elem.text for elem in driver.find_elements_by_class_name('price')]
	# Collect pricePerUnit
	products_price_per_unit = [elem.text for elem in driver.find_elements_by_class_name('measure-range')]
	# Check that attirbute count matches
	assert len(products_name) == len(products_brand) == len(products_supermarket) == len(products_weight) == len(products_price) == len(products_price_per_unit)

	############## Separate "per kg" (with range as well), "each"
	print('Regex chopping...')

	products_ppu = []
	products_unit = []

	for product_ppu in products_price_per_unit:
		try:
			match = re.search(r'\$([0-9]{1,3}\.[0-9]{1,2}) ([\w\s]+)', product_ppu)
			products_ppu.append(float(match.group(1)))
			products_unit.append(match.group(2))
		except AttributeError:
			products_ppu.append(0.0)
			products_unit.append('n/a')





	####################################

	# Generate list of objects
	products = []
	for i in range(len(products_name)):
		products.append(Grocery(products_name[i], products_brand[i], products_supermarket[i], products_weight[i], products_price[i], products_ppu[i], products_unit[i]))

	print('Sorting...')
	# To sort the list in place...
	products.sort(key=lambda x: x.pricePerUnit, reverse=False)
	products.sort(key=lambda x: x.unit, reverse=False)

	return products





