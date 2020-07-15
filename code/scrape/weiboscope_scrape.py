#!/usr/bin/python3
'''
weiboscope_scrape.py is part of the art project Unerasable Characters II, developed by Winnie Soon
More: http://siusoon.net/unerasable-characters-ii/
last update: 15 Jul 2020

Logic:
*need python3 filename.py
1. Retrieve data from weiboscope
- check error response (http - weiboscope)
- get individual censored data (with error check), & only process those have been censored within 24 hours against current time
- store in temp arrays and prepare to append to the JSON file in one go
2. Update json
- loop through all the temp data arrays and update the JSON file in one go
3. cleaning JSON data (update with latest count + timestamp + remove too old data (more than a year) to avoid the file keep expanding over time)
*4. sendemail() if any connection fail entirely (now only log the file)

to implement:
- update the variable 'path'
- set the cron job frequency (now is daily) e.g /opt/alt/python36/bin/python3.6 <filepath+filename.py>

next/oustanding:
- client side's chinese font
- cleaning data e.g url, space, emoji handling
'''

import requests
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import json
import logging
import datetime
from datetime import datetime as dt, timedelta
from dateutil.relativedelta import relativedelta
import time
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
import pytz

path = "YOUR_PATH"
HK = pytz.timezone('Asia/Hong_Kong')
LOG_timestamp = datetime.datetime.now(HK)
logging.basicConfig(filename=path + "logfilename.log", level=logging.INFO)

#define arrays for json
t_dataCreated = []
t_dataCensored = []
t_dataContent = []
t_url = []

def requests_retry_session(
    retries=3,
    backoff_factor=0.3,
    status_forcelist=(500, 502, 504),
    session=None,
):
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session

def processData( dataresponse, link ):
    soup2 = BeautifulSoup(dataresponse.content, 'html.parser')
    data = soup2.find('p')
    #extract Censored At:
    dataCensored = re.findall(r'<p><b>Ce.*?<p>', str(data))  #extract the field name
    dataCensored = re.sub(r'<[A-Za-z\/][^>]*>', '', str(dataCensored)) #remove html tags
    dataCensored = re.sub(r'Censored+\s+At:+\s', '', str(dataCensored)) #remove the field name
    dataCensored = re.sub(r'(\[\'|\'])','', str(dataCensored))  #remove '[]'
    date_time_obj = datetime.datetime.strptime(dataCensored, '%Y-%m-%d %H:%M:%S.%f')
    #compare time withtin 24 hours (LOG_timestamp - now and the data censored )
    current_time = LOG_timestamp.strftime('%Y %d %m %H %M %S')
    current_time = datetime.datetime.strptime(current_time,'%Y %d %m %H %M %S')
    censored_time = date_time_obj.strftime('%Y %d %m %H %M %S')
    censored_time = datetime.datetime.strptime(censored_time,'%Y %d %m %H %M %S')
    difference = current_time - censored_time
    minDiff = difference.total_seconds() / 60
    if minDiff < 1440:   #24 hours in the form of minutes
        #extract CreatedAt:
        dataCreated = re.findall(r'<p><b>Cr.*?<p><b>', str(data))  #extract the field name
        dataCreated = re.sub(r'<[A-Za-z\/][^>]*>', '', str(dataCreated)) #remove html tags
        dataCreated = re.sub(r'Created+\s+At:+\s', '', str(dataCreated)) #remove the field name
        dataCreated = re.sub(r'(\[\'|\'])','', str(dataCreated))    #remove '[]'
        #extract content:
        dataContent = re.sub(r'<p>.*?Content: ', '', str(data)) #start till Content:
        dataContent = re.sub(r'<[A-Za-z\/][^>]*>', '', str(dataContent)) #remove html tags
        dataContent = re.sub(r'(Image.*|\\u200b|http[\S]+\s)', '', str(dataContent))  #remove image, unicode and http
        dataContent = re.sub(r'(\[\'|\']|\n|\r)','', str(dataContent)) #remove '[]' and new line
        dataContent = str(dataContent).strip()
        if not dataContent == '': #store the data into arrays
            t_dataCreated.append(dataCreated)
            t_dataCensored.append(dataCensored)
            t_dataContent.append(dataContent)
            t_url.append(link)
            print('Censored within 24 hours')
            print('dataCreated: ' + dataCreated)
            print('dataCensored: ' + dataCensored)
            print('dataContent: ' + dataContent)
        else:
            print("nothing in the tweet")
#2. Update JSON file with the gathered data
def processJSON():
    with open(path+'data.json') as json_file:
        data = json.load(json_file)
        jsonData = data['data']
        # python object to append
        for i in range(len(t_url)):
            jsonData.append({
                'id': t_url[i],
                'content': t_dataContent[i],
                'createdAt': t_dataCreated[i],
                'censoredAt': t_dataCensored[i]
            })
    # write json - existing file
    def write_json(data, filename=path+'data.json'):
        with open(filename,'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, separators=(',', ': '),ensure_ascii=False)
    write_json(data)

def processURL():
    soup = BeautifulSoup(response.content, 'html.parser')
    href = [i['href'] for i in soup.find_all('a', href=True)]
    for url2 in href:
        try:
            response2 = requests_retry_session().get(url2, timeout=10)
        except Exception as e:
            print('Fail:', e.__class__.__name__)
            sendemail()
        else:
            print('Success:', url2)
            processData( response2, url2 )
    processJSON()

def sendemail():
    #send the fail report email to the author
    print('nothing + send email')
    logging.info(str(LOG_timestamp) + " - critical issues & the script stops")
#3 cleaning data
def cleaningJSON():
    with open(path+'data.json') as f: #read json file data
        data = json.load(f)
        #update the count and time
        try:
            for i in range(len(data['data'])):
                #check createdAt within 1 year
                date_time_obj = datetime.datetime.strptime(data['data'][i]['createdAt'], '%Y-%m-%d %H:%M:%S')
                current_time = LOG_timestamp - relativedelta(years=1)
                current_time = current_time.strftime('%Y %d %m %H %M %S')
                current_time = datetime.datetime.strptime(current_time,'%Y %d %m %H %M %S')
                created_time = date_time_obj.strftime('%Y %d %m %H %M %S')
                created_time = datetime.datetime.strptime(created_time,'%Y %d %m %H %M %S')
                if created_time < current_time:
                    data['data'].pop(i) #delete the whole object
        except IndexError:
            pass
        data["Number_censored_messages"] = len(data['data'])
        data["last_update"]= str(LOG_timestamp) + " (HK time)"

    with open(path+'data.json','w', encoding='utf-8') as f: #write json file
        print(json.dump(data, f, indent=4, ensure_ascii=False))

# **start here**
#1. Retrieve data from weiboscope
url = 'https://weiboscope.jmsc.hku.hk/latest.php'
try:
    response = requests_retry_session().get(url,timeout=50)
except Exception as e:
    print('Fail:', e.__class__.__name__)
    sendemail()
else:
    print('Success:', response.status_code)
    processURL()
    cleaningJSON()
