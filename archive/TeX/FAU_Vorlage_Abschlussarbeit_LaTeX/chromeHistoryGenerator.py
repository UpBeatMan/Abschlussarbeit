# !/usr/bin/env python
#!-*- coding: utf-8 -*-
"""
    The chromeHistoryGenerator script safes the complete the default chrome directory in a backup directory "BACKUP_PROFILE_<timestamp>" and then creates a new default profile. In this new profile it will open all links from the data.csv file. This includes a test download at the end. The downloaded file is named random-100M and will be saved in your download folder.
"""

from selenium import webdriver
from selenium.webdriver import Chrome

import os
import csv
import time
import shutil
import getpass

#! Proof of Concept with Chrome as current testing file !
__version__ = "0.1.2"

current_username = getpass.getuser()

CHROME_DIR: str = (
    r"C:/Users/" + current_username + r"/AppData/Local/Google/Chrome/User Data"
)
DEFAULT_DIR: str = CHROME_DIR + r"/Default"
CSV: str = (
    r"C:/PythonProject/Abschlussarbeit/ChromeMultithreadingPoC/SQLiteGenerator/data.csv"
)
BACKUP_DIR: str = CHROME_DIR + r"/BACKUP-PROFILES_" + time.strftime("%Y%m%d-%H%M%S")
WEBDRIVER: str = r"C:/PythonProject/Abschlussarbeit/ChromeMultithreadingPoC/SQLiteGenerator/webdriver/chromedriver.exe"

# * backup profile directory
os.mkdir(BACKUP_DIR)
print(f'Created backup directory "BACKUP_PROFILE_<timestamp>" in {BACKUP_DIR}.')

if os.path.exists(DEFAULT_DIR):
    target_dir: str = BACKUP_DIR + r"/Default"
    shutil.copytree(DEFAULT_DIR, target_dir)
    print(f'Created backup for {DEFAULT_DIR} directories in "{BACKUP_DIR}"')
else:
    print(f'The profile directory does not exist in "{DEFAULT_DIR}"')

# * delete profile directory
if os.path.exists(DEFAULT_DIR):
    shutil.rmtree(DEFAULT_DIR)
    print(f'Directory "{DEFAULT_DIR}" deleted')
else:
    print(f'Directory "{DEFAULT_DIR}" does not exist')

# * read csv file with web links
csv_file = open(CSV)
csv_reader = csv.reader(csv_file)
csv_data = list(csv_reader)
print("csv table data loaded")
print(f"The csv  table has {len(csv_data)-1} rows")

# * chrome selenium driver start
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={CHROME_DIR}")
driver = webdriver.Chrome(executable_path=WEBDRIVER, chrome_options=options)

line_count = 0

while line_count < len(csv_data):
    if line_count == len(csv_data) - 1:
        # continue # for last line downloaded_file
        # to activate download of application/octet-stream
        print(f"Line {line_count + 1}: {csv_data[line_count][0]}")
        driver.get(csv_data[line_count][0])
        time.sleep(12)
        line_count += 1
    else:
        print(f"Line {line_count + 1}: {csv_data[line_count][0]}")
        driver.get(csv_data[line_count][0])
        line_count += 1

print(f"Processed {line_count} lines and opened them successfully")

# ! The chromedriver doesn't create any temporary profiles like the geckodriver for firefox.
# ! It will apply all changes to the Default Directory by Default. The default path is following:
# ! C:\Users\<current_username>\AppData\Local\Google\Chrome\User Data\Default

# * chrome selenium driver exit
driver.quit()
