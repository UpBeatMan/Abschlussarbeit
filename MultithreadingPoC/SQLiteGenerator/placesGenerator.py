from selenium import webdriver
import csv, time
import os, shutil

__version__ = "0.1.0"

# Download the geckodriver for mozilla firefox testing in selenium
# Add the geckodriver folder path to your PATH environment variable

# REPLACE: <username> with your user name %USERPROFILE%
# TODO: Input username during runtime
USERNAME = "<username>"

BACKUP_DIR = ("C:\\Users\\" + USERNAME + "\\AppData\\Roaming\\Mozilla\\Firefox\\BACKUP_PROFILES")
PROFILES_INI = (
    "C:\\Users\\" + USERNAME + "\\AppData\\Roaming\\Mozilla\\Firefox\\profiles.ini"
)
PROFILES_DIR = (
    "C:\\Users\\" + USERNAME + "\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles"
)
CSV = (
    "C:\\Users\\"
    + USERNAME
    + "\\Abschlussarbeit\\MultithreadingPoC\\SQLiteGenerator\\data.csv"
)
ALLOWED_FILETYPE = "application/octet-stream"


# Chromium selenium driver

# Backup ini file and profile directory from Firefox
if not os.path.exists(BACKUP_DIR):
    os.mkdir(BACKUP_DIR)
BACKUP_INI = BACKUP_DIR + "\\profiles.ini"
BACKUP_DIR = BACKUP_DIR + "\\Profiles"

# TODO: add installs.ini
# if os.path.exists(PROFILES_INI):
#     shutil.copy(PROFILES_INI, BACKUP_INI)
#     print('Created backup for file "profiles.ini"')
# else:
#     print('Can\'t create Backup for file "profiles.ini"')
# if os.path.exists(PROFILES_DIR):
#     shutil.copytree(PROFILES_DIR, BACKUP_DIR)
#     print('Created backup for directory "Profiles/"')
# else:
#     print('Can\'t create Backup for directory "Profiles/"')

# # Delete ini file and profile directory
# if os.path.exists(PROFILES_INI):
#     os.remove(PROFILES_INI)
#     print('File "profiles.ini" deleted')
# else:
#     print("File does not exist")

# if os.path.exists(PROFILES_DIR):
#     shutil.rmtree(PROFILES_DIR)
#     print('Directory "Profiles/" deleted')
# else:
#     print("Directory does not exist")

subprocess.Popen(['C:\Program Files\Mozilla Firefox\\firefox.exe', '-new-tab']) # way to open firefox and create new profiles

# Firefox selenium
profile = webdriver.FirefoxProfile() #!!! search and add new profile name between paranthesis
profile.set_preference("browser.download.manager.showWhenStarting", False) #FIXME: Test without this option
profile.set_preference("browser.helperApps.neverAsk.saveToDisk", ALLOWED_FILETYPE)

browser = webdriver.Firefox(profile)
print("Webdriver for Firefox started!")

csv_file = open(CSV)
csv_reader = csv.reader(csv_file)
csv_data = list(csv_reader)
print("CSV table data loaded.")
print(f"The csv table has {len(csv_data)} rows.")

line_count = 1
while line_count < len(csv_data):
    if line_count == 100:
        print(f"Line {line_count}: {csv_data[line_count][0]}")
        browser.get(csv_data[line_count][0])
        # browser.find_element_by_id("exportpt").click()
        # browser.find_element_by_id("exporthlgt").click()
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
