# import lz4  # lz4 compression library bindings - not used
import getpass  # password prompt without echoing
import platform  # providing system information
import datetime  # module for date and time object
import logging  # logging module for debugging

from pubsub import pub  # event based programming module - publish-subscribe API
from dateutil.relativedelta import *  # add time relative to a datetime timestamp
from urllib.parse import urlparse  # url manipulation module
from Config import Config  # use projects own Config paths and variable
from Controller.console import Console  # use projects Controller console component

from View import View  # use projects View components
from View.Dialogs.delta_dialog import TimedeltaDialog
from View.Dialogs.date_dialog import DateDialog
from View.Dialogs.ask_dialog import AskDialog
from View.Dialogs.debug_dialog import DebugDialog

from Model import Model  # use projects Model components
from Model.util import log_message # unifies log messages

class Controller:
    """controller class"""

    def __init__(self):
        """run __init__ section at class instantiation"""

        # * instantiate Config object
        self.config = Config()
        # * find and set username and os in Config
        self.config.set_current_username(getpass.getuser())
        self.config.set_current_os(platform.system())

        # * instantiate View object
        self.view = View(self)

        # * log numeration counter
        self.numerate = 0

        # * create event_logger
        self.event_logger = logging.getLogger("event")
        # set Log level to INFO for event_logger
        self.event_logger.setLevel(logging.INFO)
        # instantiate Console custom log handler as console_handler for sidebar gui event logger
        self.console_handler = Console(self.view.sidebar.console)
        # add custom console handler to event_logger
        self.event_logger.addHandler(self.console_handler)  # add handler object console

        # * create debug_logger
        self.debug_logger = logging.getLogger("debug")
        self.debug_logger.setLevel(logging.DEBUG)
        # define debug_logger handler type
        self.file_handler = logging.FileHandler("Core\\advanced.log")
        # format log messages of handlers
        file_format = logging.Formatter(
            "\n %(asctime)s - %(levelname)s -%(message)s", datefmt="%d.%b.%y %H:%M:%S"
        )
        self.file_handler.setFormatter(file_format)
        # store logging messages to file "advanced.log"
        self.debug_logger.addHandler(self.file_handler)

        # * instantiate Model object
        self.model = Model()

        # * subscribe to log_message function
        # ! see log_message() in Model.util
        pub.subscribe(self.log_listener, "logging")

        # * subscribe to flag publishing function
        # ! see loading_flag() in Model.util
        pub.subscribe(self.activity_listener, "activity")

        # * trigger initial browser profile overview loading
        self.view.sidebar.insert_profiles_to_treeview()

    def main(self):
        """indirect instantiate View object through root __init__.py"""

        self.view.main()

    def unify_enum(self, enum):
        """returns formatted 3 digit enumeration value"""
        if enum < 10:  # for logs 1-10
            enumeration = " 00" + str(enum) + " "
        elif enum < 100:  # for logs 11-99
            enumeration = " 0" + str(enum) + " "
        else:  # for logs > 99
            enumeration = " " + str(enum) + " "
        return enumeration

    def log_listener(self, message, lvl, debug="Keine Debugmeldung vorhanden"):
        """numerates and channels logging messages by their logging levels"""

        # * create numeration feature for logging messages from 1-999
        # at function call raise numerate counter by one
        self.numerate += 1
        # format counter to show a clean enumerator
        enum = self.unify_enum(self.numerate)

        # * log listener, which redirects all received logs to their loggers and log levels
        if lvl == "info":
            # info to custom console handler only - event_logger
            self.event_logger.info("    " + lvl.upper() + "\n" + enum + " " + message)
        elif lvl == "warning":
            # warning to custom console handler only - event_logger
            self.event_logger.warning(" " + lvl.upper() + "\n" + enum + " " + message)
        elif lvl == "debug":
            # warning + short information to event_logger and detailed log message to file handler - debug_logger
            self.event_logger.warning(
                " "
                + "WARNING"
                + "\n"
                + enum
                + " "
                + message
                + f"\n      --> siehe{enum}im Debugmodus"
            )
            self.debug_logger.debug(enum + "- " + debug)
        elif lvl == "error":
            # error hint to event_logger and detailed log message to file handler - debug_logger
            self.event_logger.error(
                "   "
                + lvl.upper()
                + "\n"
                + enum
                + " "
                + "Neue Fehlermeldung\n      --> Öffne Debugmodus"
            )
            self.debug_logger.error(enum + "- " + message)
        elif lvl == "critical":
            # critical error hint to event_logger and detailed log message to file handler - debug_logger
            self.event_logger.critical(
                lvl.upper()
                + "\n"
                + enum
                + " "
                + "Neue kritische Fehlermeldung\n      --> Öffne Debugmodus"
            )
            self.debug_logger.critical(enum + "- " + message)
        elif lvl == "delete":
            # close console and file handler for deletion of advanced.log
            self.console_handler.close()
            self.file_handler.close()
            logging.shutdown()
        else:
            # to file handler
            self.event_logger.error(
                "   "
                + lvl.upper()
                + "\n"
                + enum
                + " "
                + "Neue Fehlermeldung\n      --> Öffne Debugmodus"
            )
            self.debug_logger.error(enum + "- " + "Unbekanntes Log Level")

    def activity_listener(self, flag):
        """redirects received flag status changes to monitor_activity function"""

        self.view.toolbar.monitor_activity(flag)

    def load_profiles(self):
        """searches for browser profiles across all browser types - Firefox, Chrome and Edge"""

        profiledict = self.model.search_profiles(
            current_username=self.config.current_username,
            current_os=self.config.current_os,
        )
        return profiledict

    def load_profile(self, browser, name):
        """loads one browser profile selected by its browser type and profile name"""

        data = None
        if self.get_unsaved_handlers():
            log_message(
                "Änderungen noch nicht gespeichert!\nTrotzdem neues Profil laden?",
                "warning",
            )
            # notify that changes are not saved yet
            answer = AskDialog(
                self.view,
                self,
                "Änderungen noch nicht gespeichert!\nTrotzdem neues Profil laden?",
            ).show()
            if not answer:
                data = "keep"
                return data

        if not self.model.has_profile_loaded():
        #if self.model.first_profile_loading():
            # * load confirmation no profile has been loaded and first is about to load
            # It might seem pointless but is necessary for the activity_indicator to work
            answer = AskDialog(
                self.view, self, "Bestätigen Sie um den Ladevorgang zu starten!"
            ).show()
            if not answer:
                data = "keep"
                return data

        # changed has_profil_loaded to has_profile_loaded !
        elif self.model.has_profile_loaded():
            # * check if loaded profile should be replaced by a new profile
            answer = AskDialog(
                self.view,
                self,
                "Möchten Sie wirklich ein neues Profil laden?\nUngespeicherte Änderungen gehen verloren!",
            ).show()
            if not answer:
                data = "keep"
                return data
        data = self.model.load_profile(browser, name, self.config)  # load profile

        if browser in ["Edge", "Chrome"]:  # choose view type (chrome and edge similar)
            self.view.menu.chrome_edge_views()
        else:
            self.view.menu.firefox_views()

        return data

    def get_unsaved_handlers(self):
        """return unsaved_handlers"""

        unsaved_handlers = self.model.get_unsaved_handlers()
        return unsaved_handlers

    def get_saved_handlers(self):
        """return saved_handlers"""  # ! - not used

        saved_handlers = self.model.get_saved_handler()
        return saved_handlers

    def get_history(self):
        """obtain history data from sqlite"""

        data = self.model.get_history()
        return data

    def reload_data(self):
        """reload content "View" data"""

        self.change_data_view(self.view.content.dataview_mode)

    def change_data_view(self, data_view):
        """load specific data to content "View" with a given dataview_mode"""

        if data_view == "FormHistory":
            data = self.model.get_specific_data("FormHistoryHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Formular-Eingaben")
        elif data_view == "History":
            data = self.model.get_history()
            if data:
                # changed fillHistroyData to fillHistoryData !
                self.view.content.fillHistoryData(data)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Historie")
        elif data_view == "Addons":
            data = self.model.get_specific_data("AddonsHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Addons")
        elif data_view == "Bookmarks":
            data = self.model.get_specific_data("BookmarkHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Lesezeichen")
        elif data_view == "Extensions":
            data = self.model.get_specific_data("ExtensionsHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Erweiterungen")
        elif data_view == "Session":
            data = self.model.get_specific_data("WindowHandler")
            if data:
                self.view.content.fill_dataview(data, True)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Sessions")
        elif data_view == "Profile":
            data = self.model.get_specific_data("ProfileHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Profil")
        elif data_view == "Keywords":
            data = self.model.get_specific_data("KeywordHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Keywords")
        elif data_view == "Cache":
            data = self.model.get_specific_data("CacheEntryHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Cache")
        elif data_view == "Download":
            data = self.model.get_specific_data("DownloadHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Download")
        elif data_view == "Permission":
            data = self.model.get_specific_data("PermissionHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Berechtigungen")
        elif data_view == "Favicon":
            data = self.model.get_specific_data("FaviconHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Favicons")
        elif data_view == "Cookie":
            data = self.model.get_specific_data("CookieHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Cookies")
        elif data_view == "ContentPref":
            data = self.model.get_specific_data("ContentPrefHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Seiten-Präferenzen")
        elif data_view == "FireProfile":
            data = self.model.get_specific_data("TimesHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Profil")
        elif data_view == "Autofill":
            data = self.model.get_specific_data("AutofillHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Formular-Eingaben")
        elif data_view == "Login":
            data = self.model.get_specific_data("LoginHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Logins")
        elif data_view == "CompCred":
            data = self.model.get_specific_data("CompromisedCredentialHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Unsichere Anmeldedaten")
        elif data_view == "ExtCookies":
            data = self.model.get_specific_data("ExtensionCookieHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Erweiterungs-Cookies")
        elif data_view == "Media":
            data = self.model.get_specific_data("OriginHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Medien")

    def load_additional_info(self, a):  # a required for None object in args
        """load additional info data (lower content area)"""

        if self.view.content.dataview_mode == "History":
            # tkinter sets no focus as default behavior
            # focus function sets focus on content.dataview only
            item = self.view.content.dataview.item(self.view.content.dataview.focus())
            parsed_uri = urlparse(item["text"])
            split = parsed_uri.hostname.split(".")
            if len(split) > 2:
                sitename = split[1]
            else:
                sitename = split[0]
            # * get_additional_info history data for selected domain(sitename)
            data = self.model.get_additional_info("history", sitename)
            self.view.content.fill_info_section(data)
        elif self.view.content.dataview_mode == "Session":
            item = self.view.content.dataview.item(self.view.content.dataview.focus())
            data = self.model.get_additional_info("session", item["values"][-1])
            self.view.content.fill_info_section(data)
        elif self.view.content.dataview_mode == "Media":
            item = self.view.content.dataview.item(self.view.content.dataview.focus())
            data = self.model.get_additional_info("media", item["values"][-1])
            self.view.content.fill_info_section(data)

    def edit_all_data(self):
        """edit time information for all data"""

        # * ask for timedelta with dialog, then change all data based on this timedelta
        delta = TimedeltaDialog(self.view, self).show()
        if delta:
            now = datetime.datetime.now()
            delta = now - delta
            try:
                delta = now.timestamp() - delta.timestamp()
            except:
                log_message("Zeitdelta zu groß", "warning")
                return
        else:
            log_message("Kein Delta angegeben", "warning")
            return
        self.model.edit_all_data(delta)
        self.reload_data()

    def edit_selected_data(self, mode="delta", all=False, infoview=False):
        """edit time information for selected data"""

        # default path will be mode == delta in the first if-condition
        # and the "if not all" branch below line "selected_list = []"

        if mode == "date":
            date = DateDialog(self.view, self).show()
            if not date:
                log_message("Kein Datum angegeben", "warning")
                return
        else:  # mode == "delta"
            # * ask for timedelta with dialog, then change all data based on this timedelta
            delta = TimedeltaDialog(self.view, self).show()
            if delta:
                now = datetime.datetime.now()
                delta = now - delta
                try:
                    delta = now.timestamp() - delta.timestamp()
                except:
                    log_message("Zeitdelta zu groß", "warning")
                    return
            else:
                log_message("Kein Delta angegeben", "warning")
                return

        selected_list = []
        if not all:  # * default value: all = False
            # if not False => True, then do --> if path
            # if not True => False, then don't --> else path
            if not infoview:  # * do if infoview is False
                already_selected_list = []
                for (
                    selected
                ) in self.view.content.dataview.selection():  # get selected parent data
                    if (
                        selected in already_selected_list
                    ):  # check existing selected data in list
                        continue
                    item = self.view.content.dataview.item(selected)
                    # children data - get data which is in dependency - e.x. websites which have been opened over a link inside another website
                    children = self.view.content.dataview.get_children(selected)
                    children_list = []
                    if children:  # get children data
                        for child in children:
                            if child in already_selected_list:
                                continue
                            c_item = self.view.content.dataview.item(child)
                            children_list.append(
                                [c_item["values"][-2], c_item["values"][-1]]
                            )
                            already_selected_list.append(
                                child
                            )  # extend list of selected children
                    selected_list.append(
                        [item["values"][-2], item["values"][-1], children_list]
                    )  # extend list of selected parents
                    already_selected_list.append(selected)
            else:  # * do if infoview is switched to True
                selected_id = self.view.content.tab_control.select()
                selected_tab = self.view.content.tab_control.tab(selected_id, "text")
                for selected in self.view.content.info_views[selected_tab][
                    0
                ].selection():  # get data of selected tab
                    item = self.view.content.info_views[selected_tab][0].item(selected)
                    selected_list.append([item["values"][-2], item["values"][-1]])
        else:  # * do if all is True - get the data without worrying about selected data
            if not infoview:  # * if infoview == False
                for element in self.view.content.dataview.get_children():
                    children = self.view.content.dataview.get_children(element)
                    if children:
                        for child in children:
                            item = self.view.content.dataview.item(child)
                            selected_list.append(
                                [item["values"][-2], item["values"][-1]]
                            )
                    item = self.view.content.dataview.item(element)
                    selected_list.append([item["values"][-2], item["values"][-1]])
            else:  # * do if infoview is switched to True
                selected_id = self.view.content.tab_control.select()
                selected_tab = self.view.content.tab_control.tab(selected_id, "text")
                for element in self.view.content.info_views[selected_tab][
                    0
                ].get_children():
                    item = self.view.content.info_views[selected_tab][0].item(element)
                    selected_list.append([item["values"][-2], item["values"][-1]])

        if not selected_list:
            log_message("Keine Zeilen ausgewählt", "warning")
            return

        if mode == "date":
            # * date mode - date has been chosen by the popup window
            # * DateDialog at the beginning of this function
            try:
                self.model.edit_selected_data_date(date, selected_list)
            except:
                log_message("Fehler beim editieren", "error")
                return
        else:  # mode == "delta"
            self.model.edit_selected_data_delta(delta, selected_list)
            try:
                pass
            except:
                log_message("Fehler beim editieren", "error")
                return
        if not infoview:
            self.reload_data()
        else:
            self.load_additional_info(None)

    def commit_all_data(self):
        """commit all data"""

        self.model.commit()
        self.reload_data()

    def commit_selected_data(self, infoview=False):
        """only commit the selected data"""

        if not infoview:  # * do if infoview is False
            data_handler_name = self.view.content.selected_treeview_handler
            self.model.commit(data_handler_name)
            self.reload_data()
        else:  # * do if infoview is True
            selected_id = self.view.content.tab_control.select()
            selected_tab = self.view.content.tab_control.tab(selected_id, "text")
            data_handler_name = self.view.content.info_views[selected_tab][1]
            self.model.commit(data_handler_name)
            self.load_additional_info(None)
        pass

    def rollback_all_data(self):
        """rollback all data"""

        self.model.rollback()
        self.model.rollback_filesystem_time(self.config)
        self.reload_data()

    def rollback_selected_data(self, infoview=False):
        """only rollback the selected data"""

        if not infoview:
            data_handler_name = self.view.content.selected_treeview_handler
            self.model.rollback(data_handler_name)
            self.reload_data()
        else:
            selected_id = self.view.content.tab_control.select()
            selected_tab = self.view.content.tab_control.tab(selected_id, "text")
            data_handler_name = self.view.content.info_views[selected_tab][1]
            self.model.rollback(data_handler_name)
            self.load_additional_info(None)
        pass

    def change_filesystem_time(self):
        """edit timestamps of the profile files"""

        check = AskDialog(
            self.view,
            self,
            "Möchten Sie die Dateisystemzeit wirklich anpassen?\nDies sollte erst dann gemacht werden wenn alle anderen Änderungen vollzogen und gespeichert wurden!",
        ).show()
        if not check:
            return
        if not self.model.has_profile_loaded():
            log_message("Kein Profil geladen", "warning")
        try:
            self.model.change_filesystem_time(self.config)
            # pass
        except:
            log_message("Fehler beim Ändern der Dateisystem Zeit", "error")

    def rollback_filesystem_time(self):
        """rollback timestamps of the profile files"""

        try:
            self.model.rollback_filesystem_time(self.config)
        except:
            log_message("Fehler beim Rollback der Dateisystem Zeit", "error")
