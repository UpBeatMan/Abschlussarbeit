from selenium import webdriver

import time
import os
import shutil
import subprocess
import csv


__version__ = "0.1.0"

# * Required: manual setup before script execution!
# * Download the geckodriver for mozilla firefox testing in selenium
# * Add the geckodriver folder path to your PATH environment variable

# REPLACE: <username> with your user name %USERPROFILE%
# TODO: Input username during runtime
USERNAME = "Yochanan"

FIREFOX_DIR = "C:\\Users\\" + USERNAME + "\\AppData\\Roaming\\Mozilla\\Firefox"

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


# TODO: Chromium selenium driver

print("List all existing current Firefox profiles:")
old_profiles = os.listdir(PROFILES_DIR)
for profile in old_profiles:
    print(f"{PROFILES_DIR}\{profile}")

# Backup ini files and profile directory
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


# * Delete ini files and profile directory
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
# ! close Firefox Browser manually
subprocess.Popen(["C:\Program Files\Mozilla Firefox\\firefox.exe"])
print(
    " !!! Please close the Firefox Browser manually !!! \nNew profiles have been created"
)

print("Sleep for 5 seconds...")
time.sleep(5)

# filter by default-release name tag with a list-comprehension to access this profile later
profile_list = os.listdir(PROFILES_DIR)
new_profiles = [profile for profile in profile_list if "default-release" in profile]
print(f"The new default-release profiles name is:\n {new_profiles[0]}")
new_profile_dir = PROFILES_DIR + "\\" + new_profiles[0]

# * Firefox Selenium Driver Start
profile = webdriver.FirefoxProfile(new_profile_dir)
# profile.set_preference(
#     "browser.download.manager.showWhenStarting", False
# )  # FIXME: Test without this option
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ALLOWED_FILETYPE)
browser = webdriver.Firefox(profile)
print("Webdriver for Firefox started")

# * Read csv file
csv_file = open(CSV)
csv_reader = csv.reader(csv_file)
csv_data = list(csv_reader)
print("CSV table data loaded")
print(f"The csv table has {len(csv_data)} rows.")

line_count = 1
while line_count < len(csv_data):
    if line_count == len(csv_data) - 1:
        print(f"Line {line_count}: {csv_data[line_count][0]}")
        browser.get(csv_data[line_count][0])
        browser.find_element_by_id("exportpt").click()
        browser.find_element_by_id("exporthlgt").click()
        # ! close Firefox Browser manually
        print(" !!! Please close the Firefox Browser manually !!! ")
        print("Wait for 10 seconds to finish test download.")
        time.sleep(10)
        browser.close()
        print("Webdriver for Firefox closed!")
        line_count += 1
    else:
        print(csv_data[line_count][0])
        browser.get(csv_data[line_count][0])
        line_count += 1

print(f"Processed {line_count} lines.")
