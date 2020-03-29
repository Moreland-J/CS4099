import requests
import pandas as pd
import re
import csv

from bs4 import BeautifulSoup
from IPython.display import display_html
from lxml import etree

fixes = []

def scrape():
    url = requests.get('https://en.wikipedia.org/wiki/List_of_medical_roots,_suffixes_and_prefixes').text
    soup = BeautifulSoup(url, 'lxml')
    tables = soup.findAll('table')

    string = str(soup)
    for line in string.splitlines():
        if bool(re.search('row', line)):
            start = line.find('<b>')
            end = line.find('</b>')
            fixes.append(line[start:end][3:])

def clean():
    clean = False
    count = 0
    while not clean:
        # NEW SECTION FOR GOING THROUGH EACH OF THE FIXES
        for num, fix in enumerate(fixes, start = 0):
            print(num)
            # REMOVES NON-FIXES
            if '-' not in fix:
                fixes.remove(fix)
                count = 0
                print("no -")

            # TACKLE LISTS FIRST
            # ADD EXTRAS TO END OF FIXES (or insert)
            elif "," in fix:
                print("split ,")
                l = re.compile(",").split(fix)
                fixes.remove(fix)
                for i in range(0, len(l)):
                    fixes.append(l[i])
                count = 0
            else:
                count += 1

            # SECONDLY, HYPERLINKS
            # DETECT href AND DETECT ">[fix]</a>" REPEAT <b> PRACTISE
            if "href" in fix:
                print("href")
                start = fix.find('>')
                end = fix.find('</a>')
                fixes[num] = fix[start:end][1:0]
                count = 0
                # SPECIAL CASE WHERE BRACKETS AFTER HYPERLINK </a>
            else:
                count += 1

            if " or " in fix:
                temp = fix.split(" or ")
                fixes.remove(fix)
                fixes.insert(num, temp[0])
                fixes.insert(num + 1, temp[1])

            # THEN HANDLE BRACKETS WITH ONLY ONE LETTER INSIDE
            # REMOVE BRACKETS AND ADD BOTH WITH AND WITHOUT ONE LETTER TO LIST
            if "(" in fix:
                print("()")
                start = fix.find('(')
                end = fix.find(')')
                fixes.append(fix + fix[start:end][1:0])
                if fix.startswith('-'):
                    fixes[num] = fix[0:start]
                elif fix.endswith('-'):
                    fixes[num] = fix[0:start] + '-'
                count = 0
            else:
                count += 1

        # MARK TO EXIT WHILE LOOP IF ALL ELEMENTS OF LIST ARE CLEAR OF MISTAKES
        if count == len(fixes):
            clean = True

def writeCSV():
    legit = []
    for fix in fixes:
        if "," in fix:
            pass
        elif "<" in fix:
            pass
        elif fix.startswith("-") or fix.endswith("-"):
            print(fix)
            legit.append(fix)

    file = open("../database/fixes.csv", "w+", newline="")
    file.write("fix, type\n")
    for leg in legit:
        if leg.startswith("-"):
            file.write(leg + ", suffix\n")
        elif leg.endswith("-"):
            file.write(leg + ", prefix\n")
    file.close()
    

scrape()
clean()
writeCSV()
print("\nfin")