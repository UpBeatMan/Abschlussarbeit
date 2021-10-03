# import pyhton modules
import os  # os
import configparser  # configparser
import json  # json
from time import sleep  # sleep function

# import  Model.<BrowserModel> and utility functions Model.util
from Model.FirefoxModel import FirefoxModel
from Model.EdgeModel import EdgeModel
from Model.ChromeModel import ChromeModel
from Model.util import change_file_time
from Model.util import log_message

# * from Model.util import loading_flag


class Model:
    """model class"""

    def __init__(self):
        self.profiledict = {}
        self.browsermodel = None
        self.filesystem_changed = False

    # def first_profile_loading(self):
    #     """check if there is no profile loaded"""
    #     if not self.browsermodel:
    #         return True
    #     else:
    #         return False

    def has_profile_loaded(self):
        """check if there is already a profile loaded"""
        if self.browsermodel:
            return True
        else:
            return False

    def load_profile(self, browser, name, config):
        """close a still opened profile and load a new selected profile"""
        if self.browsermodel:
            # * close previous browser profile
            self.browsermodel.close()
        if browser == "Firefox":
            config.set_profile_path(self.profiledict[browser][name][0])
            config.set_cache_path(self.profiledict[browser][name][1])
            try:
                self.browsermodel = FirefoxModel(config.profile_path, config.cache_path)
                config.set_startup_history_last_time(
                    self.browsermodel.get_history_last_time()
                )
            except:
                self.browsermodel = None
                log_message("Firefox Daten konnten nicht geladen werden", "error")
            if self.browsermodel:
                return self.browsermodel.get_history()
            else:
                return None
        elif browser == "Edge":
            config.profile_path = self.profiledict[browser][name]
            try:
                self.browsermodel = EdgeModel(config.profile_path)
                config.set_startup_history_last_time(
                    self.browsermodel.get_history_last_time()
                )
            except:
                self.browsermodel = None
                log_message("Edge Daten konnten nicht geladen werden", "error")
            if self.browsermodel:
                return self.browsermodel.get_history()
            else:
                return None
        elif browser == "Chrome":
            config.set_profile_path(self.profiledict[browser][name])
            try:
                self.browsermodel = ChromeModel(config.profile_path)
                config.set_startup_history_last_time(
                    self.browsermodel.get_history_last_time()
                )
            except:
                self.browsermodel = None
                log_message("Chrome Daten konnten nicht geladen werden", "error")
            if self.browsermodel:
                return self.browsermodel.get_history()
            else:
                return None

    def get_unsaved_handlers(self):
        """returns a list of unsaved handlers from the list comprehension"""
        if self.browsermodel:
            unsaved_handler = self.browsermodel.get_unsaved_handlers()
        else:
            unsaved_handler = None
        return unsaved_handler

    def get_saved_handlers(self): # ! not used
        """returns a list of saved handlers from the list comprehension"""

        if self.browsermodel:
            saved_handler = self.browsermodel.get_saved_handlers() # ! does not exist
        else:
            saved_handler = None
        return saved_handler

    # Get additional infos (cookies, permissions, etc.) for a given website
    def get_additional_info(self, data_type, identifier):
        """returns a dictionary containing the data for the domain view in the lower content area"""
        # data will be received by following handlers
        # CookieHandler
        # FaviconHandler
        # DownloadHandler
        # LoginHandler
        # CompromisedCredentialHandler

        data = self.browsermodel.get_additional_info(data_type, identifier)
        return data

    def get_specific_data(self, id):
        """returns the data dictionary containing all the data for a specific DataHandler"""

        if self.browsermodel:
            data = self.browsermodel.get_specific_data(id)
        else:
            data = None
        return data

    def get_form_history(self):
        """returns a dictionary dict containing the data received by the FormHistoryHandler for Firefox and the AutofillHandler for Chrome/Edge"""

        if self.browsermodel:
            data = self.browsermodel.get_form_history()
        else:
            data = None
        return data

    def get_history(self):
        """returns a dictionary containing the data received by the PlacesHandler for Firefox or the VisitsHandler for Chrome/Edge"""

        if self.browsermodel:
            data = self.browsermodel.get_history()
        else:
            data = None
        return data

    def get_addons(self):
        """returns a dictionary containing the data received by the AddonsHandler"""

        if self.browsermodel:
            data = self.browsermodel.get_addons()
        else:
            data = None
        return data

    def get_bookmarks(self):
        """returns a dictionary containing the data received by the BookmarkHandler"""

        if self.browsermodel:
            data = self.browsermodel.get_bookmarks()
        else:
            data = None
        return data

    def get_extensions(self):
        """returns a dictionary containing the data received by the ExtensionsHandler for Firefox only"""

        if self.browsermodel:
            data = self.browsermodel.get_extensions()
        else:
            data = None
        return data

    def get_session(self):
        """returns a dictionary containing the data received by the WindowHandler for Firefox only"""

        if self.browsermodel:
            data = self.browsermodel.get_session()
        else:
            data = None
        return data

    def get_session_info(self, window_id): # ! not used
        """returns a dictionary containing the data received by the ??? Handler"""

        if self.browsermodel:
            data = self.browsermodel.get_session_info(window_id) # ! does not exist
        else:
            data = None
        return data

    def get_profile(self):
        """returns a dictionary containing the data received by the ProfileHandler"""

        if self.browsermodel:
            data = self.browsermodel.get_profile()
        else:
            data = None
        return data

    def get_keywords(self):
        """returns a dictionary containing the data received by the KeywordHandler"""
        if self.browsermodel:
            data = self.browsermodel.get_keywords()
        else:
            data = None
        return data

    def get_cache(self):
        """returns a dictionary containing the data received by the CacheEntryHandler"""

        if self.browsermodel:
            data = self.browsermodel.get_cache()
        else:
            data = None
        return data

    def edit_all_data(self, delta):
        """changes timestamps of all data via a requested delta (timeperiod)"""
        if self.browsermodel:
            self.browsermodel.edit_all_data(delta)
            log_message(
                "Alle Daten via Delta\n      manipuliert\n       - Commit noch notwendig! -",
                "info",
            )
        else:
            log_message("Kein Profil ausgewählt", "info")

    def edit_selected_data_delta(self, delta, selection):
        """changes timestamps of selected data via a requested delta (timeperiod)"""

        if self.browsermodel:
            self.browsermodel.edit_selected_data_delta(delta, selection)
            log_message(
                "Ausgewählte Daten via Delta\n      manipuliert\n       - Commit noch notwendig! -",
                "info",
            )
        else:
            log_message("Kein Profil ausgewählt", "info")

    def edit_selected_data_date(self, date, selection):
        """changes timestamps of selected data via a requested specific timestamp"""

        if self.browsermodel:
            self.browsermodel.edit_selected_data_date(date, selection)
            log_message(
                "Ausgewählte Daten via Datum\n      manipuliert\n       - Commit noch notwendig! -",
                "info",
            )
        else:
            log_message("Kein Profil ausgewählt", "info")

    def commit(self, name: str = None):
        """commits changes to the sqlite databases, JSON files and others"""

        if self.browsermodel:
            self.browsermodel.commit(name)
            log_message(
                "Änderungen gespeichert\n        - Commit erfolgreich! -", "info"
            )
        else:
            log_message("Kein Profil ausgewählt", "info")

    def rollback(self, name: str = None):
        """initiates rollback procedure"""

        if self.browsermodel:
            self.browsermodel.rollback(name)
        else:
            log_message("Kein Profil ausgewählt", "info")

    def rollback_filesystem_time(self, config):
        """rollbacks the timestamp changes on profile files"""

        if not self.filesystem_changed:
            log_message(
                "Rollback Dateisystemzeit\n      übersprungen\n      Sie wurde nicht manipuliert!"
                + "\n\n      Änderungen rückgängig gemacht\n        - Rollback erfolgreich! -",
                "info",
            )
            return
        delta = config.file_system_rollback_delta
        self.browsermodel.close()
        sleep(1)
        config.set_file_system_rollback_delta(0)

        paths = [config.profile_path]
        if config.cache_path:
            paths.append(config.cache_path)

        for path in paths:
            # recursivly iterate through the dirs and files and change time
            for root, dir, files in os.walk(path):
                for d in dir:
                    path = os.path.join(root, d)
                    try:
                        change_file_time(path, delta)
                    except:
                        log_message(
                            "Ornder nicht zurückgerollt",
                            "debug",
                            "Dateisystemzeit des Ordners: \n    "
                            + path
                            + " konnte nicht zurückgerollt werden",
                        )
                for f in files:
                    path = os.path.join(root, f)
                    try:
                        change_file_time(path, delta)
                    except:
                        log_message(
                            "Datei nicht zurückgerollt",
                            "debug",
                            "Dateisystemzeit der Datei: \n    "
                            + path
                            + " konnte nicht zurückgerollt werden",
                        )
        self.filesystem_changed = False
        self.browsermodel.get_data()
        log_message(
            "Änderungen rückgängig gemacht\n        - Rollback erfolgreich! -", "info"
        )

    def change_filesystem_time(self, config):
        """changes timestamps values of the profile files"""

        now_history_last_time = self.browsermodel.get_history_last_time()
        self.browsermodel.close()
        sleep(1)
        if not now_history_last_time:
            log_message("Konnte keine History finden", "error")
        paths = [config.profile_path]
        if config.cache_path:
            paths.append(config.cache_path)
        start_timestamp = config.startup_history_last_time.timestamp()
        end_timestamp = now_history_last_time.timestamp()
        delta = start_timestamp - end_timestamp
        rollback_delta = -1 * delta
        config.set_file_system_rollback_delta(rollback_delta)

        for path in paths:
            # recursivly iterate through the dirs and files and change time
            for root, dir, files in os.walk(path):
                for d in dir:
                    path = os.path.join(root, d)
                    try:
                        change_file_time(path, delta)
                    except:
                        log_message(
                            "Ordner nicht verändert",
                            "debug",
                            "Dateisystemzeit des Ordners: \n    "
                            + path
                            + " konnte nicht editiert werden",
                        )
                for f in files:
                    path = os.path.join(root, f)
                    change_file_time(path, delta)
                    try:
                        pass
                    except:
                        log_message(
                            "Datei nicht verändert",
                            "debug",
                            "Dateisystemzeit der Datei: \n    "
                            + path
                            + " konnte nicht verändert werden",
                        )
        self.filesystem_changed = True
        log_message(
            "Dateisystemzeit manipuliert\n       - Commit noch notwendig! -", "info"
        )

    def search_profiles(self, current_username, current_os):
        """searches for installation folders of Firefox, Chrome and Edge and stores the their profile paths to a dictionary"""

        firepath = None
        firecachepath = None
        chromepath = None
        edgepath = None

        if not current_username:
            log_message("Der Nutzername konnte nicht ermittelt werden!", "error")
            return None

        if current_os == "Windows":  # Microsoft Windows
            firepath = (
                "C:/Users/" + current_username + "/AppData/Roaming/Mozilla/Firefox/"
            )
            firecachepath = (
                "C:/Users/" + current_username + "/AppData/Local/Mozilla/Firefox/"
            )
            edgepath = (
                "C:/Users/"
                + current_username
                + "/AppData/Local/Microsoft/Edge/User Data/"
            )
            chromepath = (
                "C:/Users/"
                + current_username
                + "/AppData/Local/Google/Chrome/User Data/"
            )
        elif current_os == "Linux":  # Linux Distribution
            firepath = "/home/" + current_username + "/.mozilla/firefox/"
            firecachepath = "/home/" + current_username + "/.cache/mozilla/firefox/"
            chromepath = "/home/" + current_username + "/.config/google-chrome/"
            edgepath = ""
            pass
        elif current_os == "Darwin":  # Apple Mac OS
            firepath = (
                "Users/" + current_username + "/Library/Application Support/Firefox/"
            )
            firecachepath = "Users/" + current_username + "/Library/Caches/Firefox/"
            chromepath = (
                "Users/"
                + current_username
                + "/Library/Application Support/Google/Chrome/"
            )
            edgepath = ""
        else:
            log_message("Kein kompatibles Betriebssystem gefunden", "error")
            return None

        if os.path.exists(firepath):
            self.profiledict["Firefox"] = {}
            config_parser = configparser.ConfigParser()
            config_parser.read(firepath + "profiles.ini")

            for section in config_parser.sections():
                if "Profile" in section:
                    self.profiledict["Firefox"][config_parser[section].get("Name")] = [
                        firepath + config_parser[section].get("Path")
                    ]
                    if os.path.exists(firecachepath):
                        self.profiledict["Firefox"][
                            config_parser[section].get("Name")
                        ].append(firecachepath + config_parser[section].get("Path"))

        else:
            log_message("Firefox nicht installiert", "info")
            pass

        if os.path.exists(chromepath):
            self.profiledict["Chrome"] = {}
            for file in os.listdir(chromepath):
                if ("Profile " in file) or ("Default" in file):
                    path = chromepath + file
                    if os.path.isfile(path + "/Preferences"):
                        data = json.load(open(path + "/Preferences", "r"))
                        if data["profile"]["name"]:
                            self.profiledict["Chrome"][data["profile"]["name"]] = path
                        else:
                            self.profiledict["Chrome"][file] = path
                    else:
                        log_message(
                            "Datei: Preferences\n      nicht gefunden",
                            "debug",
                            "Datei: Preferences in Chrome "
                            + file
                            + " wurde nicht gefunden",
                        )
            if not self.profiledict["Chrome"]:
                log_message("Keine Profile für Chrome gefunden", "info")
        else:
            log_message("Chrome nicht installiert", "info")
            pass

        if os.path.exists(edgepath):
            self.profiledict["Edge"] = {}
            for file in os.listdir(edgepath):
                if ("Profile " in file) or ("Default" in file):
                    path = edgepath + file
                    if os.path.isfile(path + "/Preferences"):
                        data = json.load(open(path + "/Preferences", "r"))
                        if data["profile"]["name"]:
                            self.profiledict["Edge"][data["profile"]["name"]] = path
                        else:
                            self.profiledict["Edge"][file] = path
                    else:
                        log_message(
                            "Datei: Preferences\n      nicht gefunden",
                            "debug",
                            "Preferences-Datei in Edge "
                            + file
                            + " wurde nicht gefunden!",
                        )
            if not self.profiledict["Edge"]:
                log_message("Keine Profile für Edge gefunden", "info")
        else:
            log_message("Edge nicht installiert", "info")
            pass
        return self.profiledict
