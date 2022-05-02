import pytest
import pandas as pd
import numpy as np
import os

import datatest as dt

from extract.extract import Extract
from config.config import Configuration
config = Configuration(os.environ['APP_ENVIROMENT'], 'config')


@dt.working_directory(__file__)
def setUpModule():
    global extract
    extract = Extract('test_data.csv')
    extract.from_csv()

 
class TestExtract(dt.DataTestCase):

    @dt.mandatory
    def test_columns(self):
        required_columns = {'id', 'date_updated', 'vehicle_id', 'vehicle_label',
                           'vehicle_current_status', 'position_latitude', 'position_longitude',
                           'geographic_point', 'position_speed', 'position_odometer',
                           'trip_schedule_relationship', 'trip_id', 'trip_start_date', 'trip_route_id'
                           }
        self.assertValid(extract.data_frame.columns, required_columns)

    def test_invalid_file_name(self):
        with self.assertRaises(Exception):
            Extract('invalid_file_name.csv').from_csv()

    def test_vehicle_id(self):
        self.assertValid(extract.data_frame.vehicle_id, int)

    def test_vehicle_label(self):
        self.assertValid(extract.data_frame.vehicle_label, int)

    def test_vehicle_current_status(self):
        self.assertValid(extract.data_frame.vehicle_current_status, int)

    def test_position_latitude(self):
        self.assertValid(extract.data_frame.position_latitude, float)

    def test_position_longitude(self):
        self.assertValid(extract.data_frame.position_longitude, float) 

    def test_geographic_point(self):
        self.assertValid(extract.data_frame.geographic_point, str)

    def test_date_updated(self):
        self.assertValid(extract.data_frame.date_updated, str)
