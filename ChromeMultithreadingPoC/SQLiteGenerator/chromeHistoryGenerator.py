# !/usr/bin/env python
#!-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import Chrome

import os
import csv
import time
import shutil

#! Proof of Concept with Chrome as current testing file !
__version__ = "0.1.0"

USERNAME = input(" Profile path location - enter your windows-username here: ")
WEBDRIVER = "C:\\webdriver\\chromedriver.exe"
CHROME_DIR = "C:\\Users\\" + USERNAME + "\\AppData\\Local\\Google\\Chrome\\User Data"
DEFAULT_DIR = CHROME_DIR + "\\Default"
BACKUP_DIR = CHROME_DIR + "\\BACKUP-PROFILES" + "_" + time.strftime("%Y%m%d-%H%M%S")

CSV = (
    "C:\\Users\\"
    + USERNAME
    + "\\Abschlussarbeit\\MultithreadingPoC\\SQLiteGenerator\\data.csv"
)

#* Backup ini files and profile directory
os.mkdir(BACKUP_DIR)
print(f'Created backup directory "BACKUP_PROFILES_<timestamp>" in {BACKUP_DIR}.')

if os.path.exists(DEFAULT_DIR):
    target_dir = BACKUP_DIR + "\\Default"
    shutil.copytree(DEFAULT_DIR, target_dir)
    print(f'Created backup for {DEFAULT_DIR} directories in "{BACKUP_DIR}"')
else:
    print(f'The profile directory does not exist in "{DEFAULT_DIR}"')

#* Delete ini files and profile directory
if os.path.exists(DEFAULT_DIR):
    shutil.rmtree(DEFAULT_DIR)
    print(f'Directory "{DEFAULT_DIR}" deleted')
else:
    print(f'Directory "{DEFAULT_DIR}" does not exist')

#* Read csv file with web links
csv_file = open(CSV)
csv_reader = csv.reader(csv_file)
csv_data = list(csv_reader)
print("csv table data loaded")
print(f"The csv  table has {len(csv_data)-1} rows")

#* Chrome Selenium Driver Start
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

# ! The chromedriver doesn't create any temporary profiles. 
# ! It will apply all changes to the Default Directory by Default.
# * C:\Users\<username>\AppData\Local\Google\Chrome\User Data\Default

driver.quit()
