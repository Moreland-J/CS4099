import requests
import pandas as pd
import re
import csv
import time

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
    # NEW SECTION FOR GOING THROUGH EACH OF THE FIXES
    clean = []
    change = []
    delete = []
    for num, fix in enumerate(fixes, start = 0):
        # REMOVES NON-FIXES
        if '-' not in fix:
            delete.append(fix)
            # print("deleted: " + fix + " " + str(num))
            continue
        
        if check(fix):
            change.append(fix)
            # print("error in: " + fix)
        else:
            clean.append(fix)

    fixes = clean

    print("changes")
    changed = []
    while len(change) > 0:
        for i, ch in enumerate(change, start = 0):

            # TACKLE LISTS FIRST
            # ADD EXTRAS TO END OF FIXES (or insert)
            if "," in ch:
                print("split ,")
                l = ch.split(",")
                change.remove(ch)
                for j in range(0, len(l)):
                    l[j] = l[j].strip(" ")
                    if cleaned(fix):
                        changed.append(l[j])
                    elif "-" in l[j]:
                        delete.append(l[j])
                    else:
                        change.insert(l[j], i)
                print(ch)
            # Done me thinks

            # SECONDLY, HYPERLINKS
            # DETECT href AND DETECT ">[fix]</a>" REPEAT <b> PRACTISE
            if "href" in ch:
                print("href")
                start = ch.find('>')
                end = ch.find('</a>')
                ch = ch[start:end][1:0]
                # SPECIAL CASE WHERE BRACKETS AFTER HYPERLINK </a>

            if " or " in ch:
                temp = ch.split(" or ")
                del ch
                fixes.insert(num, temp[0])
                fixes.insert(num + 1, temp[1])

            # THEN HANDLE BRACKETS WITH ONLY ONE LETTER INSIDE
            # REMOVE BRACKETS AND ADD BOTH WITH AND WITHOUT ONE LETTER TO LIST
            if "(" in ch:
                print(ch + " ()")
                start = ch.find('(')
                end = ch.find(')')
                change.append(ch + ch[start:end][1:0])
                if ch.startswith('-'):
                    ch = ch[0:start]
                elif ch.endswith('-'):
                    ch = ch[0:start] + '-'

def cleaned(fix):
    return not ("-" not in fix or "," in fix or "href" in fix or " or " in fix or "(" in fix)

def cleanSymbols(change):
    # PERFORM SPLIT ACTIONS
    # IF STILL CONTAINS PROBLEMS THEN RECURSE
    print()

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