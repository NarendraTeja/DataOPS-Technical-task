#!/usr/bin/env python
# coding: utf-8

# In[3]:


import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


driver = webdriver.Chrome(ChromeDriverManager().install())

url = "https://www.epa.gov/greenpower/green-power-partnership-national-top-100"
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

time.sleep(3)
page = driver.page_source
driver.quit()
soup = BeautifulSoup(page, 'html.parser')


# In[4]:


# to scrap the table information from webpage
table = soup.find('table',class_='tablebord')

# to scrap the headers information from table
headers = []
for th in table.find_all('th'):
    headers.append(th.text)

# to scrap the rows information from table

rows1 = table.find_all('td')
rows_list = []
for td in rows1:
    rows_list.append(td.text)

# once we got the rows we need to prepare dataframe from it 

top_companies_info = []
while rows_list != []:
    top_companies_info.append(rows_list[:5])
    rows_list = rows_list[5:]

# exporting company_detailed_details to CSV

top_100_companies  = pd.DataFrame(top_companies_info,columns=headers)
top_100_companies.to_csv('top_100_companies.csv',index=False)


# # Task2

# In[5]:


import time
import pandas as pd
import collections


from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())
# get company_detailed_url_list from the Website

url = "https://www.certipedia.com/search/certified_companies?locale=en"
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(url)

time.sleep(3)
page = driver.page_source
driver.quit()
soup = BeautifulSoup(page, 'html.parser')
company_info = soup.find_all('span',class_='certificate_links')
company_detailed_url_list = []
for idx in range(0,len(company_info)):
    company_sample = company_info[idx]
    company_detailed = company_sample.find('a')
    company_detailed_url1 = company_detailed['href']
    company_detailed_url = 'https://www.certipedia.com'+company_detailed_url1
    company_detailed_url_list.append(company_detailed_url)
company_detailed_url_list  


# In[6]:


# get inside_details_url_list for each company
inside_details_url_list = []
for item in company_detailed_url_list:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(item)
    time.sleep(3)
    page = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page, 'html.parser')
    inside_details = soup.find_all('td',class_='odd last')
    inside_details_url1 = inside_details[0].find('a')
    inside_details_url = inside_details_url1['href']
    inside_details_url = 'https://www.certipedia.com'+inside_details_url
    print(inside_details_url)
    inside_details_url_list.append(inside_details_url)

inside_details_url_list

inside_details_url_list_toremove = []
inside_details_url_list_toremove.append(inside_details_url_list[1])
inside_details_url_list_f = list(set(inside_details_url_list) - set(inside_details_url_list_toremove))
inside_details_url_list_f


# In[8]:


# get company_detailed information for each company from inside urls
# del list
company_detailed = collections.defaultdict(list)
for item in inside_details_url_list_f:
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get(item)
    time.sleep(3)
    page = driver.page_source
    driver.quit()
    soup = BeautifulSoup(page, 'html.parser')
    mark_header = soup.find_all('div',class_='quality_mark_header content-sub content-sub-first')
    Certificate_Holder = list(mark_header[0])[5].text.split(':')[1].strip()
    print(Certificate_Holder)
    company_detailed['Certificate_Holder'].append(Certificate_Holder)
    
    Test_Mark_Number = list(mark_header[0])[7].text.split(':')[1].strip()
    company_detailed['Test_Mark_Number'].append(Test_Mark_Number)
    
    certificate_scopes = []
    for ultag in soup.find_all('ul', {'id': 'certificate_type_scopes'}):
        for litag in ultag.find_all('li'):
            certificate_scopes.append(litag.text.strip())
    certificate_scopes
    certificate_scopes_f = ','.join([str(x) for x in certificate_scopes])

    company_detailed['certificate_scopes_f'].append(certificate_scopes_f)
    


# In[9]:


# exporting company_detailed_details to CSV
company_detailed_details = pd.DataFrame.from_dict(company_detailed)
company_detailed_details.to_csv('company_detailed_details.csv',index=False)


# In[ ]:





# In[ ]:




