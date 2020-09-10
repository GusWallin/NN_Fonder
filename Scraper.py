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

#global variables

file_path = Path().parent.absolute()
start_page = 1  # page to start from
csv_file_name = 'Fonder_total.csv'
# path to webdriver for chrome

DRIVERPATH = r"C:\Program Files (x86)\chromedriver.exe"

# setup
driver = webdriver.Chrome(DRIVERPATH)
