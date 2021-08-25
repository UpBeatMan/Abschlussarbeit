# Sets the current
# config paths,
# user variables,
# and system variables
class Config:
    def __init__(
        self,
        profile_path=None,
        cache_path=None,
        current_username=None,
        current_os=None,
        current_browser=None,
        startup_history_last_time=None,
        file_system_rollback_delta=None,
    ):
        self.profile_path = profile_path
        self.cache_path = cache_path
        self.current_username = current_username
        self.current_os = current_os
        self.current_browser = current_browser
        self.startup_history_last_time = startup_history_last_time
        self.file_system_rollback_delta = file_system_rollback_delta

    # * setter methods - Config
    # profile, cache, username, os, browser, last history startup, file system rollback timedelta
    # # #######################

    def set_profile_path(self, path: str):
        self.profile_path = path

    def set_cache_path(self, path: str):
        self.cache_path = path

    def set_current_username(self, username: str):
        self.current_username = username

    def set_current_os(self, current_os: str):
        self.current_os = current_os

    def set_current_browser(self, current_browser: str):
        self.current_browser = current_browser

    # sets the timestamp when a browserprofile has been successfully loaded
    def set_startup_history_last_time(self, startup_history_last_time):
        self.startup_history_last_time = startup_history_last_time

    # sets the time period between startup_history_last_time and the rollback action
    def set_file_system_rollback_delta(self, file_system_rollback_delta):
        self.file_system_rollback_delta = file_system_rollback_delta
