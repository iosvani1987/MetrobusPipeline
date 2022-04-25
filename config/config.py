import json
import string
import pathlib


class Configuration:
    """
        Class to get the configuration from the json file
    """
    file_config_proxy = ""

    def __init__(self, environment: string, file_json: string):
        """
            Constructor
        """
        file_path = pathlib.Path().absolute()
        self.file_config_proxy = json.load(
            open(str(file_path) + "/config/" +environment + '/' + file_json + '.json'))

    def get_config(self, key: string):
        """
            Get the configuration from the json file
        """
        return self.file_config_proxy[key]