# DataOPS-Technical-task
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
