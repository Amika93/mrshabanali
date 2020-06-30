from requests import get
from bs4 import BeautifulSoup
import os

headers = {
    'user-agent': 'Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36'}


def url_ex(url):
    new_list = []
    response = get(url)
    response.encoding = 'utf-8'
    clean_html = BeautifulSoup(response.text, 'html.parser')
    h2 = clean_html.find_all('h2')
    for item in h2:
        link = item.find('a')
        new_list.insert(0, link['href'])
    return new_list


def new_links_agg(url):
    new_links = []
    links_to_check = []
    links_to_check = url_ex(url) + links_to_check
    with open('mrshabanali/list.txt', 'r') as links:
        lines = links.readlines()
        if lines:
            last_link = lines[len(lines) - 1][:-1]
        else:
            last_link = None
        if last_link == links_to_check[-1]:
            return None
        elif (last_link in links_to_check) and (last_link != links_to_check[-1]):
            new_links = links_to_check[(links_to_check.index(last_link) + 1):] + new_links
            return new_links
        elif last_link not in links_to_check:
            new_links = links_to_check + new_links
            return new_links


def update_list():
    page_to_check = 'http://mrshabanali.com/page/'
    links_to_append = []
    page_number = 1

    while True:
        nwlst = new_links_agg(page_to_check + str(page_number))
        if nwlst == None:
            print('Your List is Up To Date!')
            break
        elif len(nwlst) == 10:
            links_to_append = nwlst + links_to_append
            page_number += 1
        else:
            print('Link Found, Your List is Updating...')
            links_to_append = nwlst + links_to_append
            break

    if len(links_to_append) > 0:
        with open('mrshabanali/list.txt', 'a') as f:
            for item in links_to_append:
                f.write("%s\n" % item)
    print('Done!')


def update_files():
    mobile_files = os.listdir('mrshabanali/mobilePages')
    mobile_names = [int(f.replace(".html", "")) for f in mobile_files]

    if mobile_names:
        last_mobile_file_number = max(mobile_names)
    else:
        last_mobile_file_number = 0

    with open('mrshabanali/list.txt', 'r') as f:
        lines = f.readlines()
        if last_mobile_file_number == len(lines):
            print('Your Mobile List Is Up To Date!')
        elif last_mobile_file_number < len(lines):
            i = last_mobile_file_number + 1
            for l in range(last_mobile_file_number, len(lines)):
                save_page(lines, l, i)
                i += 1
            print('Done!')
        else:
            print('No New Mobile Files!')


def save_page(lines, l, i):
    response = get(str(lines[l]), headers=headers)
    response.encoding = 'utf-8'
    clean_html = BeautifulSoup(response.text, 'html.parser')
    file_name = 'mrshabanali/mobilePages/%0.6d.html' % i
    with open(file_name, 'w', encoding="utf-8") as file:
        file.write(str(clean_html))
        print(file_name + ' added to mobilePages!')


if __name__ == '__main__':
    update_list()
    update_files()
