from datetime import datetime # python datetime module

# imports all chrome sub modules
from Model.ChromeModel.JSON import DataSourcesJSON
from Model.ChromeModel.SQLite import DataSourcesSQLite
from Model.ChromeModel.Cache import DataSourcesCache
from Model.ChromeModel.SQLite.history import VISITED
from Model.ChromeModel.SQLite.base import OTHER

# sends log message to log listener in controller module
from Model.util import log_message


class ChromeModel:
    """submodel class modeling the Chrome data backend"""

    def __init__(self, profile_path: str = None):
        """run __init__ section at class instantiation"""

        if profile_path is None:
            log_message("Kein gültiger Chrome Profilpfad gefunden", "error")
            return

        self.sources = {} # dict with key-value pairs

        self.sources["SQLite"] = DataSourcesSQLite(profile_path)
        self.sources["JSON"] = DataSourcesJSON(profile_path)
        self.sources["Cache"] = DataSourcesCache(profile_path)

        self.data_dict = self.get_data()
        self.save_state = {}
        for key in self.data_dict:
            self.save_state[key] = True

        # * TEST LOG MESSAGES for all defined log levels
        # log_message("This is an info message", "info")
        # log_message("This is a warning message", "warning")
        # log_message("This is a debug message", "debug")
        # log_message("This is an error message", "error")
        # log_message("This is a critical message", "critical")

    def get_unsaved_handlers(self):
        """returns a list of unsaved handlers from the list comprehension"""
        return [
            self.save_state[handler]
            for handler in self.save_state
            if self.save_state[handler] == False
        ]

    def get_saved_handlers(self):
        """returns a list of saved handlers from the list comprehension"""
        # ! - not used
        return [
            self.save_state[handler]
            for handler in self.save_state
            if self.save_state[handler] == True
        ]

    def get_data(self):
        """loads data from profile files"""
        data_dict = {}
        for source in self.sources:
            data_dict.update(self.sources[source].get_data())
        return data_dict

    def reload_data_attributes(self):
        """gets DataHandler attributes from data_dict"""

        for source in self.data_dict:
            for item in self.data_dict[source]:
                try:
                    item.reload_attributes()
                except:
                    pass

    def get_history(self):
        """builds tree view in the history content view"""

        # changed histroy_tree to history_tree in this function !
        history_tree = {}
        for entry in self.data_dict["VisitsHandler"]:
            # * initial/direct visit of an url
            if entry.from_visit == 0:
                history_tree[entry] = []
            else:
                # * visit url over a link from a other url
                for tree_entry in history_tree:
                    # * for each tracked from_visit id append to tree
                    if entry.from_visit == tree_entry.id or entry.from_visit in [
                        sube.id for sube in history_tree[tree_entry]
                    ]:
                        history_tree[tree_entry].append(entry)
        return history_tree

    def get_history_last_time(self):
        """returns timestamp when history was successfully loaded last time"""

        history_last_time = None
        try:
            last_history_item = self.data_dict["VisitsHandler"][-1]
            for attr in last_history_item.attr_list:
                if attr.name == VISITED:
                    history_last_time = attr.value
        except:
            last_history_item = datetime.now()

        return history_last_time

    def get_additional_info(self, data_type, identifier):
        """returns a dictionary containing the data for the domain view in the lower content area"""
        # data will be received by following handlers
        # CookieHandler
        # FaviconHandler
        # DownloadHandler
        # LoginHandler
        # CompromisedCredentialHandler"""

        if data_type == "history":
            data_dict = {
                "Cookies": [],
                "Favicons": [],
                "Downloads": [],
                "Logins": [],
                "CompromisedCreds": [],
            }

            try:
                for cookie in self.data_dict["CookieHandler"]:
                    if identifier in cookie.host:
                        data_dict["Cookies"].append(cookie)
            except:
                pass

            try:
                for favico in self.data_dict["FaviconHandler"]:
                    if identifier in favico.urls.url:
                        data_dict["Favicons"].append(favico)
            except:
                pass

            try:
                for downl in self.data_dict["DownloadHandler"]:
                    if identifier in downl.referrer:
                        data_dict["Downloads"].append(downl)
            except:
                pass

            try:
                for login in self.data_dict["LoginHandler"]:
                    if identifier in login.origin_url:
                        data_dict["Logins"].append(login)
            except:
                pass

            try:
                for compcred in self.data_dict["CompromisedCredentialHandler"]:
                    if identifier in compcred.date_created:
                        data_dict["CompromisedCredentialHandler"].append(compcred)
            except:
                pass

        return data_dict

    def get_addons(self):
        """returns a dictionary containing the data received by the AddonsHandler"""

        return self.data_dict["AddonsHandler"]

    def get_bookmarks(self):
        """returns a dictionary containing the data received by the BookmarkHandler"""

        return self.data_dict["BookmarkHandler"]

    def get_profile(self):
        """returns a dictionary containing the data received by the ProfileHandler"""

        return self.data_dict["ProfileHandler"]

    def get_keywords(self):
        """returns a dictionary containing the data received by the KeywordHandler"""

        return self.data_dict["KeywordHandler"]

    def get_form_history(self):
        """returns a dictionary dict containing the data received by the AutofillHandler for Chrome/Edge"""

        return self.data_dict["AutofillHandler"]

    def get_cache(self):
        """returns a dictionary containing the data received by the CacheEntryHandler"""

        return self.data_dict["CacheEntryHandler"]

    def get_specific_data(self, id):
        """returns the data dictionary containing all the data for a specific DataHandler"""

        if id in self.data_dict:
            if self.data_dict[id]:
                return self.data_dict[id]
            else:
                log_message(f"Keine Daten verfügbar\n      für {id}", "info")
                return None
        else:
            log_message(f"DataHandler unbekannt: {id}", "error")
            return None

    def edit_all_data(self, delta):
        """changes timestamps of all data via a requested delta (timeperiod)"""

        for source in self.data_dict:
            for item in self.data_dict[source]:
                item.update(delta)
        self.reload_data_attributes()
        for handler in self.save_state:
            self.save_state[handler] = False

    def edit_selected_data_delta(self, delta, selection):
        """changes timestamps of selected data via a requested delta (timeperiod)"""

        for selected in selection:
            for item in self.data_dict[selected[0]]:
                if int(item.id) == int(selected[1]):
                    item.update(delta)
                    self.save_state[selected[0]] = False
                try:
                    for other_item in self.data_dict[selected[0]]:
                        if item.place.id == other_item.place.id:
                            other_item.reload_attributes()
                except:
                    pass
            if len(selected) > 2:
                for child in selected[2]:
                    for c_item in self.data_dict[child[0]]:
                        if int(c_item.id) == int(child[1]):
                            c_item.update(delta)
                            try:
                                for other_item in self.data_dict[child[0]]:
                                    if other_item.place.id == c_item.place.id:
                                        other_item.reload_attributes()
                            except:
                                pass

    def edit_selected_data_date(self, date, selection):
        """changes timestamps of selected data via a requested specific timestamp"""

        delta = None  #
        for selected in selection:
            for item in self.data_dict[selected[0]]:
                if int(item.id) == int(selected[1]):
                    for attr in item.attr_list:
                        if attr.type != OTHER:
                            delta = attr.value.timestamp() - date.timestamp()
                            break
                    item.update(delta)
                    self.save_state[selected[0]] = False
                    try:
                        for other_item in self.data_dict[selected[0]]:
                            if item.place.id == other_item.place.id:
                                other_item.reload_attributes()
                    except:
                        pass
            if len(selected) > 2:
                for child in selected[2]:
                    for c_item in self.data_dict[child[0]]:
                        if int(c_item.id) == int(child[1]):
                            c_item.update(delta)
                            try:
                                for other_item in self.data_dict[child[0]]:
                                    if other_item.place.id == c_item.place.id:
                                        other_item.reload_attributes()
                            except:
                                pass

    def rollback(self, name: str = None):
        """initiates rollback procedure"""

        for source in self.sources:
            self.sources[source].rollback(name)
        if name:
            for item in self.data_dict[name]:
                item.is_date_changed = False
                item.init()
            self.save_state[name] = True
        else:
            for source in self.data_dict:
                for item in self.data_dict[source]:
                    item.is_date_changed = False
                    item.init()
            for handler in self.save_state:
                self.save_state[handler] = True

    def commit(self, name: str = None):
        """initiates commit procedure"""

        for source in self.sources:
            self.sources[source].commit(name)
        if name:
            for item in self.data_dict[name]:
                item.is_date_changed = False
            self.save_state[name] = True
        else:
            for source in self.data_dict:
                for item in self.data_dict[source]:
                    item.is_date_changed = False
            for handler in self.save_state:
                self.save_state[handler] = True

    def close(self):
        """closes data sources"""

        for source in self.sources:
            self.sources[source].close()
