from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  
import threading

users = ['Chihemihe', 'Tikamajere', 'Kitiaramatar', 'Cheeheemeehee', 'Amomapilla', 'Lauralanthalesa', 'Crowmane']

def scrape(user):
    url = 'https://www.ffxiah.com/player/Asura/{}'.format(user)
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    source = browser.page_source

    soup = BeautifulSoup(source, features="html.parser")

    sales_data = soup.find_all(id='player-sales')
    #print(sales_data)
    sales_data_tables = soup.find_all('table')

    for table in sales_data_tables:
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        output = []
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            output.append([ele for ele in cols if ele])

        start_index = 0
        for i, o in enumerate(output, start=0):
            if o and 'Price History' in o[0]:
                start_index = i
                break
        print (output[start_index+2:start_index+12])
        break

for user in users:
    scrape_thread = threading.Thread(target=scrape, args=(user,))
    scrape_thread.start()
    scrape_thread.join()
