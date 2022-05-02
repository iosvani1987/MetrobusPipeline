import pandas as pd
import os

class Extract():
    """
    This class is used to extract data from the database.
    """
    file_to_process = ""
    data_frame = None

    def __init__(self, file_to_process):
        """
            Constructor
        """
        self.file_to_process = file_to_process

    def from_csv(self):
        """
            This function is used to extract data from a csv file.
        """
        self.data_frame = pd.read_csv(self.file_to_process)
        return self.data_frame

    def from_json(self):
        """
            This function is used to extract data from a json file.
        """
        self.data_frame = pd.read_json(self.file_to_process)
        return self.data_frame

    def save_to_csv(self, file_name):
        """
            This function is used to save the data to a csv file.
        """
        self.data_frame.to_csv(file_name)
