#Scrape the dynamic signals website using Selenium
import requests
import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

print("Opening browser...")
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
driver.get("https://signals.investingstockonline.com/free-binary-signal-page")

while True:
	print("Scraping table row and data...")
	for tr in driver.find_elements_by_tag_name("tr"):
		time.sleep(5)
		for td in tr.find_elements_by_tag_name("td"):
			print(td.get_attribute("innerText"))
			if td >= 5:
				break
			time.sleep(1)

