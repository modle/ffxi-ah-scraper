import ast
import datetime
import os
import syslog
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  

syslog.syslog('scrape started')

script_path = os.getenv('SCRIPT_PATH')

syslog.syslog('path is {}'.format(script_path))

def get_users():
    f = open("{}/users.txt".format(script_path), "r")
    users = f.read().split("\n")
    return users


def scrape():
    file_path = "{}/output/{}".format(script_path, user)
    soup = get_soup()
    current_sales = parse_sales(soup)
    old_sales = get_previous(file_path)
    write_new(current_sales, file_path)
    do_diff(old_sales, current_sales)


def get_soup():
    url = 'https://www.ffxiah.com/player/Asura/{}'.format(user)
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    source = browser.page_source
    browser.close()
    return BeautifulSoup(source, features="html.parser")


def parse_sales(soup):
    sales_data = soup.find_all(id='player-sales')

    try:
        table = soup.find_all('table')[0]
    except:
        # no sales history
        return []

    diff_count = 0

    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    output = []

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        output.append([ele for ele in cols if ele])

    if user not in output[0][0]:
        print ("no data for user {}".format(user))

    start_index = 0
    for i, o in enumerate(output, start=0):
        if o and 'Price History' in o[0]:
            start_index = i
            break

    new_contents = output[start_index+2:start_index+12]
    new_joined = []
    for entry in new_contents:
        stringified = ", ".join(entry)
        if 'Screenshots' in stringified:
            break
        if entry[2] != user:
            continue
        sold_item = "{} - {}".format(entry[0], entry[4])
        new_joined.append(sold_item)
    return new_joined


def get_previous(file_path):
    try:
        f = open(file_path, "r")
        return ast.literal_eval(f.read())
    except:
        return []


def write_new(contents, file_path):
    if not contents:
        return
    f = open(file_path, "w+")
    f.write(str(contents))


def do_diff(old, new):
    list_diff = [i for i in old + new if i not in old]
    if list_diff:
        print ("{} new sales:\ncount: {}\n{}".format(user, len(list_diff), list_diff))
    write_diff(list_diff)


def write_diff(diff):
    if not diff:
        return
    time = datetime.datetime.now()
    f = open("{}/diff".format(script_path), "a+")
    f.write("\n{} : ".format(time))
    f.write(str(diff))
    

if __name__ == "__main__":
    users = get_users()
    # threading is weird; this makes user available for all of the thread
    for user in users:
        scrape_thread = threading.Thread(target=scrape)
        scrape_thread.start()
        scrape_thread.join()
