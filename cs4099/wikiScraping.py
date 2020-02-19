import requests
import pandas as pd
import csv

from bs4 import BeautifulSoup
from IPython.display import display_html
from lxml import etree

url = requests.get('https://en.wikipedia.org/wiki/List_of_medical_roots,_suffixes_and_prefixes').text
soup = BeautifulSoup(url, 'lxml')
# print(soup.prettify())

print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

tables = soup.findAll('table')
# print(tables)

print("---------------------------------------------------------------------------------------------------------------------------------------------------------------------------")

# parser = etree.HTMLParser()
# tree = etree.fromstring(tables, parser)
# results = tree.xpath('//tr/td [position() = 1]')

# for r in results:
#     print(r.text)

display_html(tables, raw=True)

print("\nrows\n")

for row in tables:
    print(row[0])

print("\nfin")