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


def get_next_page(driver):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.LINK_TEXT, 'Nästa')))
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")
    element.click()
    time.sleep(2)


def get_fund_info(driver):
    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "tabs-tab-0")))
    element.click()
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    results_table = soup.find_all('table')[0]
    results_table_data = [[cell.text for cell in row.find_all(
        ["th", "td"])] for row in results_table.find_all("tr")]

    results_frame = pd.DataFrame(results_table_data)
    # print(results_frame.head())

    return results_frame
# function to get the results page and data for each fund.


def get_fund_results(driver):

    element = WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.ID, "tabs-tab-1")))
    element.click()
    time.sleep(1)

    soup = BeautifulSoup(driver.page_source, 'lxml')
    results_table = soup.find_all('table')[0]
    results_table_data = [[cell.text for cell in row.find_all(
        ["th", "td"])] for row in results_table.find_all("tr")]

    results_frame = pd.DataFrame(results_table_data)
    # print(results_frame.head())

    return results_frame

# clean dataframes percentage numbers.


def clean_data_number(number):

    str_number = str(number)
#    print(str_number)

    if not str_number or len(str_number) == 0:
        return np.nan

    elif '%0,00' in str_number:
        return '0.00'

    elif '--' in str_number:
        return '-' + str_number.split(' ')[1]

    elif '++' in str_number:
        return str_number.split(' ')[1]

    elif '%' in str_number:
        return str_number.split(' ')[1]

    else:
        return number
