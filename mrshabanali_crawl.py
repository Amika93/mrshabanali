from requests import get
from bs4 import BeautifulSoup
import os
from pathlib import Path
import datetime

print('starting at : ', datetime.datetime.now())

Path("mrshabanali/mobilePages").mkdir(parents=True, exist_ok=True)

def urlEx(url):
    newList = []
    response = get(url)
    response.encoding = 'utf-8'
    cleanHTML = BeautifulSoup(response.text, 'html.parser')
    h2 = cleanHTML.find_all('h2')
    for item in h2:
        link = item.find('a')
        newList.insert(0, link['href'])
    return newList

url = 'http://mrshabanali.com'
response = get(url)
cleanHTML = BeautifulSoup(response.text, 'html.parser')
pageLinks = cleanHTML.find_all('a', class_='page-numbers')
pageNumbers = [a.get_text() for a in pageLinks]
lastPage = int(pageNumbers[-2])

linksList = []
url = 'http://mrshabanali.com/page/'
for i in range(lastPage, 0, -1):
    linksList += urlEx(url + str(i))

with open('mrshabanali/list.txt', 'w') as f:
    for item in linksList:
        f.write("%s\n" % item)

with open('mrshabanali/list.txt', 'r') as f:
    i=1
    for line in f:
        headers = {'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'}
        response = get(str(line), headers=headers)
        response.encoding = 'utf-8'
        cleanHTML = BeautifulSoup(response.text, 'html.parser')
        fileName = 'mrshabanali/mobilePages/'+str(i)+'.txt'
        with open(fileName, 'w', encoding="utf-8") as file:
            file.write(str(cleanHTML))
            print(fileName+' added')
        i+=1
print('Done!')
print('finished at : ', datetime.datetime.now())