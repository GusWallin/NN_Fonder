from bs4 import BeautifulSoup
import requests
import time
import math
import numpy as np
from pathlib import Path
import pandas as pd
from tabulate import tabulate
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementClickInterceptedException
from selenium import webdriver
import functions

# settings
pd.pandas.set_option('display.max_columns', None)

# global variables
file_path = Path().parent.absolute()
start_page = 30  # page to start from
csv_file_name = 'Fonder_total.csv'

# path to webdriver for chrome
DRIVERPATH = r"C:\Program Files (x86)\chromedriver.exe"

# setup
driver = webdriver.Chrome(DRIVERPATH)
driver.get("https://www.nordnet.se/marknaden/fondlistor?sortField=name&sortOrder=asc&selectedTab=overview&page=" + str(start_page))

# soup = BeautifulSoup(driver.page_source, 'lxml')
# table = soup.find_all('table')[0]
# tab_data = [[cell.text for cell in row.find_all(
#     ["th", "td"])] for row in table.find_all("tr")]

# global variables
page_counter = int(start_page)
total_df = pd.DataFrame()

# while loop runs until all pages have been iterated and saved to the csv.
while True:

    print('page: ' + str(page_counter))

    merge_df = pd.merge(functions.get_fund_info(driver), functions.get_fund_results(
        driver), right_index=True, left_index=True)

    total_df = total_df.append(merge_df)

    try:
        functions.get_next_page(driver)
        page_counter += 1

    except:
        print('exception, end of pages')
        break

total_df = total_df.applymap(functions.clean_data_number)
# print(total_df.info())
# print(total_df.head())

# save output to a file output


total_df.to_csv('' + str(file_path) + '\\' + csv_file_name)
print('File saved as ' + csv_file_name +
      'with ' + str(len(total_df.index)) + ' rows')

driver.quit()
