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

#! Proof of Concept with Firefox discontinued - only partially working !
__version__ = "0.1.0"

#* Required: manual setup before script execution!
#* Download the geckodriver for mozilla firefox testing in selenium
#* Add the geckodriver folder in your webdriver path of choice
#* or simply add it to your PATH environment variable

USERNAME = input(" Profile path location - enter your windows-username here: ")

FIREFOX_DIR = "C:\\Users\\" + USERNAME + "\\AppData\\Roaming\\Mozilla\\Firefox"
WEBDRIVER = "C:\\webdriver\\geckodriver.exe"

PROFILES_DIR = FIREFOX_DIR + "\\Profiles"
PROFILES_INI = FIREFOX_DIR + "\\profiles.ini"
PROFILES_INS = FIREFOX_DIR + "\\installs.ini"

BACKUP_DIR = FIREFOX_DIR + "\\BACKUP-PROFILES" + "_" + time.strftime("%Y%m%d-%H%M%S")
BACKUP_INI = BACKUP_DIR + "\\profiles.ini"
BACKUP_INS = BACKUP_DIR + "\\installs.ini"

CSV = (
    "C:\\Users\\"
    + USERNAME
    + "\\Abschlussarbeit\\MultithreadingPoC\\SQLiteGenerator\\data.csv"
)
ALLOWED_FILETYPE = "application/octet-stream"


print("List all existing current Firefox profiles:")
old_profiles = os.listdir(PROFILES_DIR)
for profile in old_profiles:
    print(f"{PROFILES_DIR}\{profile}")

#* Backup ini files and profile directory
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


#* Delete ini files and profile directory
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

# open Firefox to create a new profile
#! close Firefox Browser manually
subprocess.Popen(["C:\Program Files\Mozilla Firefox\\firefox.exe"])
print(
    " !!! Please close the Firefox Browser manually !!! \nNew profile has been created"
)

input("Press a key when you have closed the firefox browser")

# filter by default-release name tag with a list-comprehension to access this profile later
profile_list = os.listdir(PROFILES_DIR)
new_profiles = [profile for profile in profile_list if "default-release" in profile]
print(f"The new default-release profiles name is:\n {new_profiles[0]}")
new_profile_dir = PROFILES_DIR + "\\" + new_profiles[0]
print(new_profile_dir)

#* Firefox Selenium Driver Start

# Start Browser
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
option.set_preference(
    "browser.helperApps.neverAsk.saveToDisk",
    "application/octet-stream, application/pdf, image/png, application/msword, text/csv, application/Zip",
)
# load profile
pfadffprofile = new_profile_dir
ffprofile = webdriver.firefox.firefox_profile.FirefoxProfile(
    profile_directory=pfadffprofile
)
driver = webdriver.Firefox(
    firefox_profile=ffprofile,
    options=option,
    executable_path=WEBDRIVER,
)
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
#* Read csv file with web links
csv_file = open(CSV)
csv_reader = csv.reader(csv_file)
csv_data = list(csv_reader)
print("CSV table data loaded")
print(f"The CSV table has {len(csv_data)-1} rows")

line_count = 1
#! Deactivated the if case for the download feature - deprecated feature!
#! If activated the script gets stuck after the download has been started.
#! It never continues although the download successfully finishes after a while.
while line_count < len(csv_data) - 1:
    #     # Last csv line contains download example
    if (
        line_count == len(csv_data) - 1
    ):  # to activate download of application/octet-stream
        print(f"Line {line_count}: {csv_data[line_count][0]}")
        driver.get(csv_data[line_count][0])
        # Automatic confirmation of the download popup window
        driver.find_element_by_id("exportpt").click()
        driver.find_element_by_id("exporthlgt").click()
        # ! close Firefox Browser manually
        print(" !!! Please close the Firefox Browser manually !!! ")
        print("Wait for 10 seconds to finish test download.")
        time.sleep(10)
        line_count += 1
    #   # All other csv lines open simple websites urls
    else:
        print(f"Line {line_count}: {csv_data[line_count][0]}")
        driver.get(csv_data[line_count][0])
        line_count += 1

print(f"Processed {line_count} lines and opened them successfully in {new_profiles[0]}")

# copy ur stuff after use or periodically
print("safe Profile")
pfadffprofile = save_temp_profile
print("Saving profile " + ffTempProfilePath + " to " + pfadffprofile)
print("Choose - D for directory - and let the files copy. The browser will close automatically after the download")
os.system(
    "xcopy " + ffTempProfilePath + " " + pfadffprofile + " /Y /G /K /R /E /S /C /H"
)
print("Files should be copied :/")

# close driver
driver.quit()
print("Webdriver for Firefox closed!")

#! Short introduction to the firefox selenium problem - TL;DR: I couldn't get it to work properly. It works on Chrome browser. Deprecated the firefox approach!
#! In order to save changes made by the script its necessary to bypass selenium cleanliness. Although it seems to even with a workaround don't work for file downloads.
#* import selenium
#* import sys
#*
# #* 1- set profile
#* profile = os.path.dirname(sys.argv[0]) + "/selenita"
#* fp = webdriver.FirefoxProfile(profile)
#* driver = webdriver.Firefox(firefox_profile=fp)

# #* 2- get tmp file location
#* profiletmp = driver.firefox_profile.path

# #* but... the current profile is a copy of the original profile :/
#* print "running profile " + profiletmp

#* driver.get("http://httpbin.org")
#* time.sleep(2)
#* raw_input("Press a key when finish doing things") # for example after you have installed an extension.

# #* 3- then save back
#* print "saving profile " + profiletmp + " to " + profile
#* if os.system("cp -R " + profiletmp + "/* " + profile ):
#*     print "files should be copied :/"

#* driver.quit()
#* sys.exit(0)
