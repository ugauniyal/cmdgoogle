import requests
from bs4 import BeautifulSoup
from terminaltables import AsciiTable, SingleTable
import json
import time
import os

user_input = input('Enter your search: ')
print('\n')
modified_input = user_input.replace(' ', '+')
search = {'q': modified_input}
r = requests.get('https://google.com/search', params=search)

soup = BeautifulSoup(r.text, 'html.parser')

search_title = soup.title.text
search_title = search_title.replace('+', ' ')

db_file = 'links.txt'

if not os.path.exists(db_file):
    with open(db_file, 'w') as f:
        f.write('{}')


with open(db_file, 'r') as f:
    links_db = json.load(f)

data = []
data.append([search_title, 'Link'])

for anchor in soup.find_all('a'):
    headlines = anchor.find_all('h3')
    if len(headlines) == 1:
        biglink = anchor['href']
        biglink_index = biglink.find('&')
        biglink = biglink[7:biglink_index]
        
        if biglink in links_db.keys():
            short_link = links_db[biglink]

        else:
            short_link_api = requests.get('https://api.shrtco.de/v2/shorten', params={'url': biglink})
            short_link_dict = json.loads(short_link_api.text)
            short_link = short_link_dict['result']['full_short_link']
            links_db[biglink] = short_link
            time.sleep(1.0)

        
        data.append([headlines[0].text, short_link])
        os.system('cls' if os.name == 'nt' else 'clear')
        table_result = SingleTable(data)
        table_result.inner_row_border = True
        print(table_result.table)

with open(db_file, 'w') as f:
    json.dump(links_db, f, indent=6)