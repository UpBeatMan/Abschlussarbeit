import getpass  # password prompt without echoing
import platform  # providing system information
import datetime  # module for date and time object
import logging  # logging module for debugging
import lz4  # lz4 compression library bindings

from pubsub import pub  # event based programming module - publish-subscribe API
from dateutil.relativedelta import *  # add time relative to a datetime timestamp
from urllib.parse import urlparse  # url manipulation module
from Config import Config  # use projects own Config paths and variable
from Controller.console import Console  # use projects Controller console component
from View import View  # use projects View components
from View.Dialogs.delta_dialog import (
    TimedeltaDialog,
)  # use projects timedelta dialog tk component
from View.Dialogs.date_dialog import DateDialog  # use projects date dialog tk component
from View.Dialogs.ask_dialog import (
    AskDialog,
)  # use projects warning dialog tk component

# ! new additions
from View.Dialogs.debug_dialog import (
    DebugDialog,
)  # use projects debug dialog tk component
from View.toolbar import Toolbar

from Model import Model  # use projects Model components


class Controller:
    def __init__(self):
        # instantiate Config object
        # find and set username and os in Config
        self.config = Config()
        self.config.set_current_username(getpass.getuser())
        self.config.set_current_os(platform.system())

        # FIXME: import relationship errors
        # self.config.set_load_activity_flag(False)

        # instantiate View object
        self.view = View(self)

        # instantiate Console object with logging handler - sidebar
        self.console = Console(self.view.sidebar.console)
        self.logger = logging.getLogger()  # create logger
        self.logger.setLevel(logging.INFO)  # INFO log level for events
        # ! TODO: Separate DEBUG, WARNING, ERROR, CRITICAL Logs in new a new tk component
        self.logger.addHandler(self.console)  # add handler object console

        # instantiate Model object
        self.model = Model()

        # subscribe to either INFO or ERROR logger
        pub.subscribe(self.log_listener, "logging")

        self.view.sidebar.insert_profiles_to_treeview()

    def main(self):
        # indirect instantiate View object through root __init__.py
        self.view.main()

    # # FIXME: Handle load_activity_flag - not working yet
    # def set_load_activity_flag(self, switch: bool):
    #     Config.set_load_activity_flag(switch)

    # def get_load_activity_flag(self):
    #     status = Config.get_load_activity_flag()
    #     return status

    # * profile handling
    def load_profiles(self):
        # search for browser profiles across all browser types - Firefox, Edge and Chrome
        profiledict = self.model.search_profiles(
            current_username=self.config.current_username,
            current_os=self.config.current_os,
        )
        return profiledict

    def load_profile(self, browser, name):
        # load one browser profile
        data = None
        if self.get_unsaved_handlers():
            # check if changes are saved
            answer = AskDialog(
                self.view,
                self,
                "Es wurden nicht alle Daten gespeichert!\n Trotzdem fortfahren?",
            ).show()
            if not answer:
                data = "keep"
                return data
        # * changed has_profil_loaded to has_profile_loaded
        if self.model.has_profile_loaded():
            # check if loaded profile should be replaced
            answer = AskDialog(
                self.view, self, "Möchten Sie das Profil wirklich wechseln?"
            ).show()
            if not answer:
                data = "keep"
                return data
        data = self.model.load_profile(browser, name, self.config)  # load profile
        if browser in ["Edge", "Chrome"]:  # choose view
            self.view.menu.chrome_edge_views()
        else:
            self.view.menu.firefox_views()
        return data

    # * getter methods for data from the "Model" component
    def get_unsaved_handlers(self):
        unsaved_handlers = self.model.get_unsaved_handlers()
        return unsaved_handlers

    def get_saved_handlers(self):
        saved_handlers = self.model.get_saved_handler()
        return saved_handlers

    # * obtain data from sqlite
    def get_history(self):
        data = self.model.get_history()
        return data

    # * "View" data
    def reload_data(self):
        self.change_data_view(self.view.content.dataview_mode)

    # * change data
    def change_data_view(self, data_view):
        if data_view == "FormHistory":
            data = self.model.get_specific_data("FormHistoryHandler")
            if data:
                self.view.content.fill_dataview(data, False)
                self.view.content.dataview_mode = data_view
                self.view.content.change_view_label("Formular-Eingaben")
        elif data_view == "History":
            data = self.model.get_history()
            if data:
                self.view.content.fillHistroyData(data)
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

    # * load data
    def load_additional_info(self, a):
        # tkinter gives no focus on default behaviour
        # focus() sets focus on content.dataview only
        if self.view.content.dataview_mode == "History":
            item = self.view.content.dataview.item(self.view.content.dataview.focus())
            parsed_uri = urlparse(item["text"])
            split = parsed_uri.hostname.split(".")
            if len(split) > 2:
                sitename = split[1]
            else:
                sitename = split[0]

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

    # * edit time information
    def edit_all_data(self):
        # Ask for timedelta with dialog, then change all data based on this timedelta
        delta = TimedeltaDialog(self.view, self).show()
        if delta:
            now = datetime.datetime.now()
            delta = now - delta
            try:
                delta = now.timestamp() - delta.timestamp()
            except:
                self.log_listener("Zeitdelta zu groß!", "error")
                return
        else:
            self.logger.error("Kein Delta angegeben!")
            return
        self.model.edit_all_data(delta)
        self.reload_data()

    def edit_selected_data(
        self, mode, all=False, infoview=False
    ):  # * default path will be the - else branches - below line "selected_list = []"
        # Ask for timedelta with dialog, then change all data based on this timedelta
        if mode == "date":
            date = DateDialog(self.view, self).show()
            if not date:
                self.logger.error("Kein Datum angegeben!")
                return
        else:
            delta = TimedeltaDialog(self.view, self).show()
            if delta:
                now = datetime.datetime.now()
                delta = now - delta
                try:
                    delta = now.timestamp() - delta.timestamp()
                except:
                    self.log_listener("Zeitdelta zu groß!", "error")
                    return
            else:
                self.logger.error("Kein Delta angegeben!")
                return
        selected_list = []
        if (
            not all
        ):  # * if all == False - 
            # * if not (all=)FALSE, then do |
            # * if not True, then don't
            if (
                not infoview
            ):  # * if infoview == False 
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
            else:  # * if infoview switched to True
                selected_id = self.view.content.tab_control.select()
                selected_tab = self.view.content.tab_control.tab(selected_id, "text")
                for selected in self.view.content.info_views[selected_tab][
                    0
                ].selection():  # get data of selected tab
                    item = self.view.content.info_views[selected_tab][0].item(selected)
                    selected_list.append([item["values"][-2], item["values"][-1]])
        else:  # * if all == True then go here - get the data without worrying about selected data
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
            else:  # * if infoview == True
                selected_id = self.view.content.tab_control.select()
                selected_tab = self.view.content.tab_control.tab(selected_id, "text")
                for element in self.view.content.info_views[selected_tab][
                    0
                ].get_children():
                    item = self.view.content.info_views[selected_tab][0].item(element)
                    selected_list.append([item["values"][-2], item["values"][-1]])

        if not selected_list:
            self.logger.info("Keine Elemente ausgewählt!")
            return

        if mode == "date":
            try:
                self.model.edit_selected_data_date(date, selected_list)
            except:
                self.logger.error("Fehler beim editieren")
                return
        else:
            self.model.edit_selected_data_delta(delta, selected_list)
            try:
                pass
            except:
                self.logger.error("Fehler beim editieren")
                return
        if not infoview:
            self.reload_data()
        else:
            self.load_additional_info(None)

    # * commit data
    def commit_all_data(self):
        # commit all data
        self.model.commit()
        self.reload_data()

    def commit_selected_data(self, infoview=False):
        # only commit the selected table
        if not infoview:  # * if infoview == False
            data_handler_name = self.view.content.selected_treeview_handler
            self.model.commit(data_handler_name)
            self.reload_data()
        else:  # * if infoview == True
            selected_id = self.view.content.tab_control.select()
            selected_tab = self.view.content.tab_control.tab(selected_id, "text")
            data_handler_name = self.view.content.info_views[selected_tab][1]
            self.model.commit(data_handler_name)
            self.load_additional_info(None)
        pass

    # * rollback data
    def rollback_all_data(self):
        # rollback all data
        self.model.rollback()
        self.model.rollback_filesystem_time(self.config)
        self.reload_data()

    def rollback_selected_data(self, infoview=False):
        # only rollback the selected table
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

    # * edit filesystem time
    def change_filesystem_time(self):
        #
        check = AskDialog(
            self.view,
            self,
            "Möchten Sie die Dateisystemzeit wirklich anpassen?\n Dies sollte erst dann gemacht werden wenn alle anderen Änderungen vollzogen und gespeichert wurden!",
        ).show()
        if not check:
            return
        if not self.model.has_profile_loaded():
            self.logger.info("Kein Profil geladen!")
        self.model.change_filesystem_time(self.config)
        try:
            # * unknown error occurred
            pass
        except:
            self.logger.error("Fehler beim ändern der Dateisystem Zeit!")

    def rollback_filesystem_time(self):
        try:
            self.model.rollback_filesystem_time(self.config)
        except:
            self.logger.error("Fehler beim Rollback der Dateisystem Zeit!")

    # * The listener for the logging event (here standard python logging - without pypubsub)
    def log_listener(self, message, lvl):
        if lvl == "info":
            self.logger.info(message)
        else:
            self.logger.error(message)

    # * neu hinzugekommen

    def open_debugwin(self):
        check = DebugDialog(self.view, self).show()
        if not check:
            return
        try:
            # * unknown error occurred
            pass
        except:
            self.logger.error("Fehler beim Öffnen des Debugfensters!")

    def query_active(self):
        check = Toolbar(self.view, self).start()
        if not check:
            return
        try:
            # * unknown error occurred
            pass
        except:
            self.logger.error("Fehler beim Aktivieren des Akitivitätsstatus!")

    def query_done(self):
        check = Toolbar(self.view, self).stop()
        if not check:
            return
        try:
            # * unknown error occurred
            pass
        except:
            self.logger.error("Fehler beim Deaktivieren des Akitivitätsstatus!")
