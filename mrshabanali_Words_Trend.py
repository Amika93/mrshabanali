from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
import numpy as np
import os

mobileFiles = os.listdir('mrshabanali/mobilePages')

def dateExwordCount(fileName):
    with open(fileName, 'r', encoding="utf-8") as f:
        htmlText = f.read()
        cleanHTML = BeautifulSoup(htmlText, 'html.parser')
        bulkDate = cleanHTML.find('span', class_='post-date')
        date = bulkDate.text.replace(',', '')
        entries = cleanHTML.find_all('div', {"id": "content"})
        text = [t.get_text() for t in entries]
        words = text[0].split()
        return [len(words), date[:-7] + date[-4:]]

wordCount = []
for file in mobileFiles:
    filePath = 'mrshabanali/mobilePages/'+file
    wordCount.append(dateExwordCount(filePath))

d = {}

for item in wordCount:
    d.setdefault(item[1],[0]).append(item[0])


xAxis = []
yAxis = []
for k,v in d.items():
    xAxis.append(k)
    yAxis.append(sum(v))

index = np.arange(len(xAxis))
plt.bar(index, yAxis)
plt.xlabel('Date', fontsize=10)
plt.ylabel('Words', fontsize=10)
plt.xticks(index, xAxis, fontsize=5, rotation=30)
plt.show()