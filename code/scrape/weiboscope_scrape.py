'''
*need python3 filename.py
- scraping the latest censored text from weiboscope
- get all the URL (max200)
- Then scrape three major parameters: created at, censored at, content for each link
- data processing to clean the data
- export to a json file (for the javascript program)

To do:
- automate the process with acculated text that write on the existing json file
- store the accumulated data and check duplicate id (check link- url + read json + loop data)
- still need to special handle some tweets:
    - https://weiboscope.jmsc.hku.hk/list.php?id=4493266445221255
    -  http://t.cn/A6wAXHW1
- possible need to change to csv as the file grows
'''

import requests
from urllib.request import urlopen
import time
from bs4 import BeautifulSoup
import re
import json

url = 'https://weiboscope.jmsc.hku.hk/latest.php'
response = requests.get(url)
print(response)

soup = BeautifulSoup(response.content, 'html.parser')
href = [i['href'] for i in soup.find_all('a', href=True)]
#print(project_href)

jsonData = {
    "description": "This file contains sample weibo data: permission denied posts",
    "source": "https://weiboscope.jmsc.hku.hk/latest.php",
    "Number_censored_messages": "Past 7 days, max 200, order by publication date",
    "credit": "Fu, King Wa, Hong Kong University",
    "lastUpdate": time.ctime(),
    "data": []}

for link in href:
    print(link)
    url2 = link
    response2 = requests.get(url2)
    soup2 = BeautifulSoup(response2.content, 'html.parser')
    data = soup2.find('p')
    #extract CreatedAt:
    dataCreated = re.findall(r'<p><b>Cr.*?<p><b>', str(data))  #extract the field name
    dataCreated = re.sub(r'<[A-Za-z\/][^>]*>', '', str(dataCreated)) #remove html tags
    dataCreated = re.sub(r'Created+\s+At:+\s', '', str(dataCreated)) #remove the field name
    dataCreated = re.sub(r'(\[\'|\'])','', str(dataCreated))    #remove '[]'
    #extract Censored At:
    dataCensored = re.findall(r'<p><b>Ce.*?<p>', str(data))  #extract the field name
    dataCensored = re.sub(r'<[A-Za-z\/][^>]*>', '', str(dataCensored)) #remove html tags
    dataCensored = re.sub(r'Censored+\s+At:+\s', '', str(dataCensored)) #remove the field name
    dataCensored = re.sub(r'(\[\'|\'])','', str(dataCensored))  #remove '[]'
    #extract content:
    dataContent = re.findall(r'<p><b>Con.*', str(data))  #extract the field name
    dataContent = re.sub(r'<[A-Za-z\/][^>]*>', '', str(dataContent)) #remove html tags
    dataContent = re.sub(r'Content:\s', '', str(dataContent))   #remove the field name
    dataContent = re.sub(r'(Image.*|\\u200b|http[\S]+\s)', '', str(dataContent))  #remove image, unicode and http
    dataContent = re.sub(r'(\[\'|\'])','', str(dataContent))  #remove '[]'
    dataContent = str(dataContent).strip()
    #print data on console
    if not dataContent == '':
        print(dataCreated)
        print(dataCensored)
        print(dataContent)
        #push to jsonData
        jsonData['data'].append({
            'content': dataContent,
            'createdAt': dataCreated,
            'censoredAt': dataCensored
        })
    else:
        print("nothing")

#write json
with open('data.json', 'w', encoding='utf-8') as jsonfile:
    json.dump(jsonData, jsonfile, indent=4, separators=(',', ': '),ensure_ascii=False)

'''
#test
url2 = 'https://weiboscope.jmsc.hku.hk/list.php?id=4493266445221255'
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.content, 'html.parser')
data = soup2.find('p')
#df = df.replace() #e.g t.cn/xxxx [space
print(data)
#extract CreatedAt:
dataCreated = re.findall(r'<p><b>Cr.*?<p><b>', str(data))
dataCreated = re.sub(r'<[A-Za-z\/][^>]*>', '', str(dataCreated))
dataCreated = re.sub(r'Created+\s+At:+\s', '', str(dataCreated))
dataCreated = re.sub(r'(\[\'|\'])','', str(dataCreated))
#extract Censored At:
dataCensored = re.findall(r'<p><b>Ce.*?<p>', str(data))
dataCensored = re.sub(r'<[A-Za-z\/][^>]*>', '', str(dataCensored))
dataCensored = re.sub(r'Censored+\s+At:+\s', '', str(dataCensored))
dataCensored = re.sub(r'(\[\'|\'])','', str(dataCensored))
#extract content:
dataContent = re.findall(r'<p><b>Con.*', str(data))
dataContent = re.sub(r'<[A-Za-z\/][^>]*>', '', str(dataContent))
dataContent = re.sub(r'Content:\s', '', str(dataContent))   #remove the field name
dataContent = re.sub(r'(Image.*|\\u200b|http[\S]+\s)', '', str(dataContent))  #remove image, unicode and http
dataContent = re.sub(r'(\[\'|\'])','', str(dataContent))
dataContent = str(dataContent).strip()
#print data on console
if not dataContent == '':
    print(dataCreated)
    print(dataCensored)
    print(dataContent)
else:
    print("nothing")
'''
