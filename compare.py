import ast
import threading

users = ['Chihemihe', 'Tikamajere', 'Kitiaramatar', 'Cheeheemeehee', 'Amomapilla', 'Lauralanthalesa', 'Crowmane']

def compare(user):
    print()
    print('showing diff for {}'.format(user))
    file_path = "output/{}".format(user)
    f = open(file_path, "r")
    olds = ast.literal_eval(f.read())
    news = olds.copy()
    news[1] = "asdf"
    list_diff = [i for i in olds + news if i not in olds or i not in news]
    print (list_diff)

for user in users:
    scrape_thread = threading.Thread(target=compare, args=(user,))
    scrape_thread.start()
    scrape_thread.join()
