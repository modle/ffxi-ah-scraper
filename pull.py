
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  

url = 'https://www.ffxiah.com/player/Asura/Tikamajere'

options = Options()
options.headless = True
browser = webdriver.Firefox(options=options)
browser.get(url)
source = browser.page_source

f = open("source", "a+")
f.write(source)
f.close()

