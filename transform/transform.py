from xmlrpc.client import Boolean
import pandas as pd
import numpy as np
import math
import os
import logging
import requests

from config.config import Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Configuration(os.environ['APP_ENVIROMENT'],'config')

class Transform():
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

    def from_csv(self) -> pd.DataFrame:
        """
            This function is used to extract data from a csv file.
        """
        self.data_frame = pd.read_csv(self.file_to_process, index_col = "id")
        return self.data_frame

    def verify_columns(self) -> Boolean:
        """
            This function is used to verify if the columns are correct.
        """
        logger.info('Verifying columns')
        columns_dataframe = config.get_config('columns_dataframe')
        # iterating the columns
        for col in self.data_frame.columns:
            if col not in columns_dataframe:
                raise Exception(f'The column {col} is not valid')
        return True

    def is_vehicle_id_unique(self) -> Boolean:
        """
            This function is used to verify if the vehicle id is unique.
        """
        logger.info('Checking if the vehicle id is unique')
        if len(self.data_frame.vehicle_id.unique()) != len(self.data_frame):
            return False
            # raise Exception('The vehicle id is not unique')
        return True

    def remove_duplicate_entries(self, column_name: str) -> pd.DataFrame:
        """
            This function is used to remove duplicate entries.
        """
        logger.info('Removing duplicate entries')
        self.data_frame.drop_duplicates(subset=[column_name], keep='first', inplace=True)
        return self.data_frame

    def replace_null_values(self, column_name: str, value: str) -> pd.DataFrame:
        """
            This function is used to replace null values.
        """
        logger.info(f'Replacing null values with {value} in column {column_name}')
        self.data_frame[column_name] = self.data_frame[column_name].fillna(value)
        return self.data_frame

    def replace_invalid_values(self, column_name: str, value: str) -> pd.DataFrame:
        """
            This function is used to replace invalid values.
        """
        logger.info('Replacing invalid values')
        self.data_frame[column_name] = self.data_frame[column_name].replace(value, np.nan)
        return self.data_frame

    def replace_invalid_values_with_mean(self, column_name: str) -> pd.DataFrame:
        """
            This function is used to replace invalid values with the mean.
        """
        logger.info('Replacing invalid values with the mean')
        self.data_frame[column_name] = self.data_frame[column_name].replace(np.nan, self.data_frame[column_name].mean())
        return self.data_frame

    def _is_valid_position(self, position) -> Boolean:
        """
            This function is used to verify if the position is valid.
        """
        point = np.array(position.geographic_point.split(',')).astype(float)
        return math.isclose(point[0], position.position_latitude) & math.isclose(point[1], position.position_longitude)


    def remove_invalid_geographic_coordinates(self) -> pd.DataFrame:
        """
            This function is used to remove if the geographic coordinates are invalid.
        """
        logger.info('Checking invalid geographic coordinates')
        valid_position_mask = self.data_frame.apply(lambda row: self._is_valid_position(row), axis=1)
        self.data_frame = self.data_frame[valid_position_mask]
        return self.data_frame

    def _get_county_name(self, position) -> str:
        """
            Private function is used to get the county name from api extrenal service.
        """
        url = config.get_config('api_position_stack')['host']
        url = url + "access_key=" + config.get_config('api_position_stack')['key']
        url = url + "&query=" + str(position) + "&limit=1"
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("data")[0].get("county")
        else:
            return None

    def get_county_name_from_api(self) ->pd.DataFrame:
        """
            This function is used to get the county name from api extrenal service.
        """
        logger.info('Getting county name from api')
        self.data_frame['county'] = self.data_frame["geographic_point"].apply(self._get_county_name)
        # Removing the rows with invalid county name
        return self.data_frame.drop(self.data_frame[self.data_frame["county"].isnull()].index, inplace = True)

    def filter_data_frame_by_column(self) -> pd.DataFrame:
        """
            This function is used to filter the data frame by column.
        """
        self.data_frame = self.data_frame[config.get_config('columns_dataframe')]
        return self.data_frame

    def save_data_frame_to_csv(self, file_name: str) -> Boolean:
        """
            This function is used to save the data frame to a csv file.
        """
        logger.info('Saving data frame to csv')
        self.data_frame.to_csv(file_name, index=False)
        return True