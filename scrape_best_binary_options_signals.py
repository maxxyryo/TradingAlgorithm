import requests
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

print("Opening browser...")
options = Options()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
url = "https://best-binary-options-signals.com/free-binary-options-signals/"
driver.get(url)

signals = driver.find_element_by_id('expiredsignals')
print(signals.text)
driver.close()
quit()
