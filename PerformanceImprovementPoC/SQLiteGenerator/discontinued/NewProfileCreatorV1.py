# !/usr/bin/env python
#!-*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver import Firefox
from selenium.webdriver.firefox.options import Options

import time
import os
import shutil
import subprocess
import csv

# ! Firefox version discontinued - only partially working - no downloads possible!
__version__ = "0.1.0" # * New-Profile-Creator - Version 1

# * Requires manual setup before script execution!
# * Download the geckodriver for mozilla firefox testing in selenium.
# * Add the geckodriver webdriver in known folder of your PATH user environment variable.

USERNAME = input(" Profile path location - enter your windows-username here: ")

FIREFOX_DIR = "C:\\Users\\" + USERNAME + "\\AppData\\Roaming\\Mozilla\\Firefox"
WEBDRIVER = "C:\\PythonProject\\Abschlussarbeit\\PerformanceImprovementPoC\\SQLiteGenerator\\webdriver\\geckodriver.exe"

PROFILES_DIR = FIREFOX_DIR + "\\Profiles"
PROFILES_INI = FIREFOX_DIR + "\\profiles.ini"
PROFILES_INS = FIREFOX_DIR + "\\installs.ini"

BACKUP_DIR = FIREFOX_DIR + "\\BACKUP-PROFILES" + "_" + time.strftime("%Y%m%d-%H%M%S")
BACKUP_INI = BACKUP_DIR + "\\profiles.ini"
BACKUP_INS = BACKUP_DIR + "\\installs.ini"

CSV = "C:\\PythonProject\\Abschlussarbeit\\PerformanceImprovementPoC\\SQLiteGenerator\\data.csv"

# * Overview of all firefox profiles
print("List all existing current Firefox profiles:")
old_profiles = os.listdir(PROFILES_DIR)
for profile in old_profiles:
    print(f"{PROFILES_DIR}\{profile}")

# * Backup ini files and profile storage directory
os.mkdir(BACKUP_DIR)
print(f'Created backup directory "BACKUP_PROFILES_<timestamp>" in {BACKUP_DIR}.')

if os.path.exists(PROFILES_DIR):
    for profile in old_profiles:
        profiles = PROFILES_DIR + "\\" + str(profile)
        backups = BACKUP_DIR + "\\" + str(profile)
        shutil.copytree(profiles, backups)
        print(f'Created backup for {profile} directories in "{backups}"')
else:
    print(f'The profile directory does not exist in "{PROFILES_DIR}"')

if os.path.exists(PROFILES_INI):
    shutil.copy(PROFILES_INI, BACKUP_INI)
    print(f'Created backup for file "profiles.ini" in "{BACKUP_INI}"')
else:
    print(f'The file "profiles.ini" does not exist in "{PROFILES_INI}"')

if os.path.exists(PROFILES_INS):
    shutil.copy(PROFILES_INS, BACKUP_INS)
    print(f'Created backup for file "installs.ini" in "{BACKUP_INS}"')
else:
    print(f'The file "installs.ini" does not exist in "{PROFILES_INS}"')


# * Delete ini files and profile storage directory
if os.path.exists(PROFILES_DIR):
    shutil.rmtree(PROFILES_DIR)
    print(f'Directory "{PROFILES_DIR}" deleted')
else:
    print(f'Directory "{PROFILES_DIR}" does not exist')

if os.path.exists(PROFILES_INI):
    os.remove(PROFILES_INI)
    print(f'File "{PROFILES_INI}" deleted')
else:
    print(f'File "{PROFILES_INI}" does not exist')

if os.path.exists(PROFILES_INS):
    os.remove(PROFILES_INS)
    print(f'File "{PROFILES_INS}" deleted')
else:
    print(f'File "{PROFILES_INS}" does not exist')

# * open Firefox to create a new profile
subprocess.Popen(["C:\Program Files\Mozilla Firefox\\firefox.exe"])
print(
    " !!! Please close the Firefox Browser manually !!! \nNew profile has been created"
)
# ! close Firefox Browser manually
input("Press a key when you have closed the firefox browser")

# * Filter by default-release name tag with a list-comprehension to access this profile later
profile_list = os.listdir(PROFILES_DIR)
new_profiles = [profile for profile in profile_list if "default-release" in profile]
print(f"The new default-release profiles name is:\n {new_profiles[0]}")
new_profile_dir = PROFILES_DIR + "\\" + new_profiles[0]
print(new_profile_dir)

# * Firefox Selenium Driver Start
# * Start Browser
option = Options()
# set options as u like, for example:
# options.add_argument("--headless")
# print("Firefox Headless Browser Invoked")
option.log.level = "warn"
option.set_preference("browser.link.open_newwindow", 3)
option.set_preference("browser.link.open_newwindow.restriction", 0)
option.set_preference("browser.download.folderList", 2)
option.set_preference("browser.download.manager.showWhenStarting", False)
option.set_preference("browser.download.dir", FIREFOX_DIR)
# * all allowed filetypes for a download
option.set_preference(
    "browser.helperApps.neverAsk.saveToDisk",
    "application/octet-stream, application/pdf, image/png, application/msword, text/csv, application/Zip",
)
# * load profile
pfadffprofile = new_profile_dir
ffprofile = webdriver.firefox.firefox_profile.FirefoxProfile(
    profile_directory=pfadffprofile
)
# * start selenium webdriver
driver = webdriver.Firefox(
    firefox_profile=ffprofile,
    options=option,
    executable_path=WEBDRIVER,
)
# * Search and store temporary selenium firefox profile
print("Get the temporary firefox profile path of the selenium instance")
driver.get("about:support")
box = driver.find_element_by_id("profile-dir-box")
ffTempProfilePath = box.text
print("ffTempProfilePath: ", ffTempProfilePath)
profile_name = ffTempProfilePath.rsplit("\\", 1)[-1]
print(profile_name)
print("Webdriver for Firefox has been started")
save_temp_profile = (
    "C:\\Users\\"
    + USERNAME
    + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles\\"
    + profile_name
)
# * Read csv file with web links
csv_file = open(CSV)
csv_reader = csv.reader(csv_file)
csv_data = list(csv_reader)
print("CSV table data loaded")

csv_length = len(csv_data)
print(f"The CSV table has {csv_length} rows")


# ! default state working: download in last line of csv table skipped
deactivate_download = 1
# ! to activate last line download uncomment line below to overwrite default value above
# deactivate_download = 0

line_start = 0

# * With line_start = 1 the last line of the csv table will be skipped
# ! If line_start = 0 the download link will be visited and the script will get stuck after the download has been started.
# ! The script never continues to the next steps unfortunately, although the download successfully finishes after a while.
while line_start < (csv_length - deactivate_download):
    if line_start == csv_length - 1:
        # * Case for the last line download link in the csv table of application/octet-stream
        print(f"Line {line_start}: {csv_data[line_start][0]}")
        driver.get(csv_data[line_start][0])
        # * Automatic confirmation of the download popup window
        driver.find_element_by_id("exportpt").click()
        driver.find_element_by_id("exporthlgt").click()
        print(" !!! Please close the Firefox Browser manually !!! ")
        print("Wait for 10 seconds to finish test download.")
        time.sleep(10)
        # ! Script is stuck - can't copy temporary profile!
        # ! Close Firefox Browser manually!
        line_start += 1
    else:
         # * Standard case for all other regular website visits (without a download popup window)
        print(f"Line {line_start}: {csv_data[line_start][0]}")
        driver.get(csv_data[line_start][0])
        line_start += 1

print(f"Processed {line_start+1} lines and opened them successfully in {new_profiles[0]}")

# * Copy temporary profile to replace standard profile
print("safe Profile")
pfadffprofile = save_temp_profile
print("Saving profile " + ffTempProfilePath + " to " + pfadffprofile)
print("Choose - D for directory - and let the files copy. The browser will close automatically after the download")
os.system("xcopy " + ffTempProfilePath + " " + pfadffprofile + " /Y /G /K /R /E /S /C /H")
print("Files should be copied!")

# * Close selenium webdriver
driver.quit()
print("Webdriver for Firefox closed!")

# ! Short introduction to the firefox selenium problem - TL;DR: I couldn't get file downloads to work properly with firefox. But it works on chrome.
# ! I decided to discontinue the firefox approach and switched with the next version 0.2.0 to a chrome approach.In detail (see lines below):
# ! In order to save changes made by the script, its necessary to bypass selenium cleanliness and bypass the temporary profile approach by the selenium framework,
# ! Bypassing by storing the temporary profile back as a normal profile wasn't possible with the download link active.
# ! Then the script never reached the code line for storing the temporary selenium profile back after line 184 (in particular lines 187-193).
# ! Debbuging was too difficult without any error messages and in-depth documentation of the gecko-webdriver.
# ! In direct comparison the most efficient proven choice was the transformation to use chrome instead, which has been done in Version 2.