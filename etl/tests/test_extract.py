import pytest
import pandas as pd
import numpy as np
import os
import extract.extract as Extract
from config.config import Configuration
config = Configuration(os.environ['APP_ENVIROMENT'],'config')

def test_extract():
    extract = Extract('test_data.csv')
    extract.from_csv()
    assert extract.data_frame.columns == config.get_config('columns_dataframe')


