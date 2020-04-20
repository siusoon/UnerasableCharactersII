'''
*need python3 filename.py
- scraping the latest censored text from weiboscope
- get all the URL (max200)
- Then scrape three major parameters: created at, censored at, content for each link
- data processing to clean the data
- export to a json file (for the javascript program)

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
    dataContent = re.sub(r'<p>.*?Content: ', '', str(data)) #start till Content:
    dataContent = re.sub(r'<[A-Za-z\/][^>]*>', '', str(dataContent)) #remove html tags
    dataContent = re.sub(r'(Image.*|\\u200b|http[\S]+\s)', '', str(dataContent))  #remove image, unicode and http
    dataContent = re.sub(r'(\[\'|\'])','', str(dataContent)) #remove '[]'
    dataContent = str(dataContent).strip()
    #print data on console
    if not dataContent == '':
        print(dataCreated)
        print(dataCensored)
        print(dataContent)
        #push to jsonData
        with open('data.json') as json_file:
            data = json.load(json_file)
            jsonData = data['data']
            # python object to be appended
            jsonData.append({
                'id': link,
                'content': dataContent,
                'createdAt': dataCreated,
                'censoredAt': dataCensored
            })
        # write json - existing file
        def write_json(data, filename='data.json'):
            with open(filename,'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, separators=(',', ': '),ensure_ascii=False)

        write_json(data)
    else:
        print("nothing")
