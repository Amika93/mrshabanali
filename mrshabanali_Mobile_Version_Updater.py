from requests import get
from bs4 import BeautifulSoup
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'}


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


def newLinksAgg(url):
    newLinks = []
    linksToCheck = []
    linksToCheck = urlEx(url) + linksToCheck
    with open('mrshabanali/list.txt', 'r') as links:
        lines = links.readlines()
        if lines:
            lastLink = lines[len(lines) - 1][:-1]
        else:
            lastLink = None
        if lastLink == linksToCheck[-1]:
            return None
        elif (lastLink in linksToCheck) and (lastLink != linksToCheck[-1]):
            newLinks = linksToCheck[(linksToCheck.index(lastLink) + 1):] + newLinks
            return newLinks
        elif lastLink not in linksToCheck:
            newLinks = linksToCheck + newLinks
            return newLinks


def update_list():
    pageToCheck = 'http://mrshabanali.com/page/'
    linksToAppend = []
    pageNumber = 1

    while True:
        nwlst = newLinksAgg(pageToCheck + str(pageNumber))
        if nwlst == None:
            print('Your List is Up To Date!')
            break
        elif len(nwlst) == 10:
            linksToAppend = nwlst + linksToAppend
            pageNumber += 1
        else:
            print('Link Found, Your List is Updating...')
            linksToAppend = nwlst + linksToAppend
            break

    if len(linksToAppend) > 0:
        with open('mrshabanali/list.txt', 'a') as f:
            for item in linksToAppend:
                f.write("%s\n" % item)
    print('Done!')


def update_files():
    mobileFiles = os.listdir('mrshabanali/mobilePages')
    mobileNames = [int(f.replace(".html", "")) for f in mobileFiles]

    if mobileNames:
        lastMobileFileNumber = max(mobileNames)
    else:
        lastMobileFileNumber = 0

    with open('mrshabanali/list.txt', 'r') as f:
        lines = f.readlines()
        if lastMobileFileNumber == len(lines):
            print('Your Mobile List Is Up To Date!')
        elif lastMobileFileNumber < len(lines):
            i = lastMobileFileNumber + 1
            for l in range(lastMobileFileNumber, len(lines)):
                save_page(lines, l, i)
                i += 1
            print('Done!')
        else:
            print('No New Mobile Files!')


def save_page(lines, l, i):
    response = get(str(lines[l]), headers=headers)
    response.encoding = 'utf-8'
    cleanHTML = BeautifulSoup(response.text, 'html.parser')
    fileName = 'mrshabanali/mobilePages/%0.6d.html' % i
    with open(fileName, 'w', encoding="utf-8") as file:
        file.write(str(cleanHTML))
        print(fileName + ' added to mobilePages!')


if __name__ == '__main__':
    update_list()
    update_files()
