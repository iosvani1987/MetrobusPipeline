import logging
import subprocess
import os
import shutil
import argparse
from config.config import Configuration

from extract.extract import Extract
from transform.transform import Transform

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Configuration(os.environ['APP_ENVIROMENT'],'config')

def _extract(file_name):
    """
    This function extracts the data from the source.
    """
    logger.info('Extracting data')
    # Verify if the file exists
    extract = Extract(file_name)
    extract.from_csv()

    #Moving file to the transformed folder
    # _move_file(config.get_config('root_path') + file_name, config.get_config('transform_path') + file_name)
    extract.save_to_csv(config.get_config('transform_path') + file_name)
    logger.info('Extracting data finished')

def _transform(file_name):
    logger.info('Starting transform process')

    transform = Transform(file_name)
    transform.from_csv()

    # Verify if the columns are correct
    transform.verify_columns()

    # Verify if the vehicle id is unique
    if not transform.is_vehicle_id_unique():
        logger.warning('The vehicle id is not unique')
        transform.remove_duplicate_entries('vehicle_id')
    
    # Replacing the values
    transform.replace_null_values('trip_id', 0)
    transform.replace_null_values('trip_route_id', 0)
    transform.replace_null_values('trip_start_date', '1900-01-01')

    # Removing invalid geolocation
    transform.remove_invalid_geographic_coordinates()

    # Getting the county from the geolocation
    transform.get_county_name_from_api()

    # Filtering the column data
    transform.filter_data_frame_by_column()

    # Saving the dataframe to csv and removing the input file
    transform.save_data_frame_to_csv(config.get_config('load_path') + "clean_" + file_name)
    _remove_file(config.get_config('transform_path'), file_name)

    logger.info('Transform process finished')


"""
This is the Auxiliary functions.
"""
""" Remove file """
def _remove_file(path, file):
    logger.info(f'Removing file {file}')
    os.remove(f'{path}{file}')

""" Searching the file in the path. """
def _search_file(path, file_match):
    logger.info('Searching file')
    for rutas in list(os.walk(path))[0]:
        if len(rutas) > 1:
            for file in rutas:
                if file_match in file:
                    return file
    return None

""" Move the file to the destination """
def _move_file(origen, destination):
    logger.info('Moving file')
    shutil.move(origen, destination)

""" End of Auxiliary functions """


def main(file_name):
    """
    This is the main function.
    """
    try:
        logger.info('Starting ETL process')
        _extract(file_name)
        _transform(file_name)
        logger.info('ETL process finished')
    except FileNotFoundError as err:
        logger.warning(str(err))
    except Exception as e:
        logger.warning('Process Error')
        logger.warning(str(e))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Input the filename path')
    parser.add_argument('file_name', help='The input file.', type=str)
    args = parser.parse_args()
    main(args.file_name)