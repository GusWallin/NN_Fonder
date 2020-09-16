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
    results_frame.drop(0, axis=0, inplace=True)

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
    results_frame.drop(0, axis=0, inplace=True)

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

# formats the dataframe and removes unessesary columns


def format_dataframe_columns(df: pd.DataFrame):

    df.drop(df.columns[[0, 2, 3, 4, 5, 8, 9, 11, 26]],
            axis=1, inplace=True)
    df.drop(df.columns[5:18], axis=1, inplace=True)
    df.drop(df.columns[13:], axis=1, inplace=True)
    df.columns = ['Namn', 'Kategori', 'Rating', 'Årlig avgift', 'Risk', '1 vecka', '1 mån',
                  '3 mån', 'i år', '1 år', '3 år', '5 år', '10 år']
    df = df.applymap(lambda x: np.NaN if '–' in x else x)

    return df


def df_to_numeric(df: pd.DataFrame):
    df = df.apply(pd.to_numeric, errors='ignore', axis=0)
    return df

# calculates renturn rankings to new columns


def calculate_Funds(df: pd.DataFrame):

    df['Return rank sum'] = df.iloc[:, 5:13].rank(
        axis=0, method='min', ascending=False).sum(axis=1).rank(axis=0, method='min', ascending=True)

    df['Long term return ranking (3,5,10 years)'] = df.iloc[:, 10:13].rank(
        axis=0, method='min', ascending=False, na_option='bottom').sum(axis=1).rank(axis=0, method='min', ascending=True)

    df['Short term return ranking (< 1 year)'] = df.iloc[:, 5:10].rank(
        axis=0, method='min', ascending=False, na_option='bottom').sum(axis=1).rank(axis=0, method='min', ascending=True)

    df['never returned negative'] = df.iloc[:, 5:13].applymap(
        lambda x: True if math.isnan(x) or x >= 0 else False).all(1)

    return df
