#!/usr/bin/python

'''
Takes argument based on Frugl URL
'''

import time

time0 = time.time()

import grocery
from selenium import webdriver
import sys


driver = webdriver.Chrome()

driver.get('https://www.frugl.com.au/browse/'+sys.argv[1])


print('Loading items...')
grocery.load_all_items(driver)
time1 = time.time()
print('{} s'.format(time1 - time0))


print('Collecting data...')
products = grocery.collect_data(driver)
time2 = time.time()
print('{} s'.format(time2 - time1))
print('Data generated!')


print('PRODUCTS BY PRICE PER UNIT:')
# Print
for grocery in products:
	print('${:<7.2f}{:<8}{:<55}{:<}'.format(grocery.pricePerUnit, grocery.unit, grocery.name, grocery.supermarket))

print("—\nNumber of products: {}".format(len(products)))

driver.close()

print('Total time: {} s'.format(time.time() - time0))
