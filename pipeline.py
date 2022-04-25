import logging
import subprocess
import os
import shutil
import argparse
from config.config import Configuration

from extract.extract import Extract

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = Configuration(os.environ['APP_ENVIROMENT'],'config')

def _extract(file_name):
    """
    This function extracts the data from the source.
    """
    logger.info('Extracting data')
    extract = Extract(file_name)
    extract.from_csv()
    extract.save_to_csv(config.get_config('saved_path') +'extracted_' + file_name)
    logger.info('Extracting data finished')

"""
This is the Auxiliary functions.
"""
""" Remove file """
def _remove_file(path, file):
    logger.info(f'Removing file {file}')
    os.remove(f'{path}\\{file}')

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
    print(config.get_config('saved_path'))
    main(args.file_name)