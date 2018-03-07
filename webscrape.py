#! python3
# webscrape.py 
import csv
import requests, os
from bs4 import BeautifulSoup
import re
import subprocess, sys
import urllib, time

###################
#Set up variables
###################
headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

url = 'TARGET_URL'
page = 1
#if products go by pages
last_page = "4"
sku = '000001'
os.chdir("/YOUR_DIRECTORY")
brand = ""
size = ""
title = ""
link = ""
price = ""

###################
#Create CSV
###################
with open("YOUR_FILENAME.csv", "wb") as toWrite:
	writer = csv.writer(toWrite, delimiter=",", quoting=csv.QUOTE_NONE, quotechar='')
	writer.writerow(['\"sku\"','\"brand\"','\"title\"','\"size\"','\"price\"','\"link\"'])

	###################
	#Scrape website pages and save them locally
	###################
	for i in range(1, int(last_page) + 1):
		urls = url1 + str(i) + url2
		urllib.urlretrieve(urls, "/YOUR_TEMP_DIRECTORY/p" + unicode(page).encode("ascii") + ".htm")

		###################
		#Scrape local pages
		###################
		scrape_url = 'http://www.YOUR-WEBSITE.com/YOUR_TEMP_DIRECTORY/p' + unicode(page).encode("ascii") + '.htm'
		res2 = requests.get(scrape_url)
		soup2 = BeautifulSoup(res2.text, "html.parser")	

		###################
		#Each item
		###################
		for div in soup2.find_all('div', { 'class' : 'ProductInfo' }):
			for item in div.findAll('a', { 'class' : 'pname' }):
				link = item.get("href")
				title = item.text.replace(',',"") if ',' in item.text else item.text
			em_tag = div.find("em")

			
			check = 0
			if(em_tag.find('strike')): 
				unwanted = em_tag.find('strike')
				unwanted.extract()
				check = 1
			
			price = em_tag.text.lstrip(' ')[1:] if check == 1 else em_tag.text[1:]	
			sku = int(sku) + 1
			print('\"BN-AU-' + '%06d' % (sku) + '\"',' \"' + unicode(brand).encode("ascii") + '\"',' \"' + unicode(title).encode("ascii", "ignore") + '\"',' \"' + size + '\"',' \"' + price + '\"',' \"' + unicode(link).encode("ascii") + '\"')
			writer.writerow(['\"BN-AU-' + '%06d' % (sku) + '\"',' \"' + unicode(brand).encode("ascii") + '\"',' \"' + unicode(title).encode("ascii", "ignore") + '\"',' \"' + size + '\"',' \"' + unicode(price).encode("ascii") + '\"',' \"' + unicode(link).encode("ascii") + '\"'])
		
		page += 1
