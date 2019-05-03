import ast
import threading
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options  

def get_users():
    f = open("users.txt", "r")
    users = f.read().split("\n")
    return users


def scrape(user):
    file_path = "output/{}".format(user)
    soup = get_soup(user)
    current_sales = parse_sales(soup, user)
    old_sales = get_previous(file_path)
    write_new(current_sales, file_path)
    do_diff(old_sales, current_sales)


def get_soup(user):
    url = 'https://www.ffxiah.com/player/Asura/{}'.format(user)
    options = Options()
    options.headless = True
    browser = webdriver.Firefox(options=options)
    browser.get(url)
    source = browser.page_source
    browser.close()
    return BeautifulSoup(source, features="html.parser")


def parse_sales(soup, user):
    sales_data = soup.find_all(id='player-sales')
    table = soup.find_all('table')[0]

    diff_count = 0

    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    output = []

    for row in rows:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        output.append([ele for ele in cols if ele])

    print (output[0])
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
        new_joined.append(", ".join(entry))
    return new_joined


def get_previous(file_path):
    try:
        f = open(file_path, "r")
        return ast.literal_eval(f.read())
    except:
        return []


def write_new(contents, file_path):
    f = open(file_path, "w+")
    f.write(str(contents))


def do_diff(old, new):
    list_diff = [i for i in old + new if i not in old]
    if list_diff:
        print ("{} new sales:\ncount: {}\n{}".format(user, len(list_diff), list_diff))


if __name__ == "__main__":
    users = get_users()
    for user in users:
        scrape_thread = threading.Thread(target=scrape, args=(user,))
        scrape_thread.start()
        scrape_thread.join()
