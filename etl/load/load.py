from .metrobus import Metrobus
from .base import Base, Session, engine
import pandas as pd
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Load():
    """
    This class is used to extract data from the database.
    """
    file_to_process = ""
    data_frame = None
    session = None

    def __init__(self, file_to_process):
        """
            Constructor
        """
        self.file_to_process = file_to_process

        logging.info('Loading data from file')
        self.from_csv()

        logging.info('Creating Data Base')
        print(engine)
        Base.metadata.create_all(engine)

        logging.info('Creating Session')
        self.session = Session()

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

    def save_to_db(self):
        """
            This function is used to save the data to a database.
        """
        for index, row in self.data_frame.iterrows():
            if self.session.query(Metrobus).filter(Metrobus.vehicle_id == row['vehicle_id']).first() is None:
                logging.info(f"Inserting the metrobus objects {row['vehicle_id']}")
                self.session.add(Metrobus(row['vehicle_id'], row['vehicle_label'], row['vehicle_current_status'],
                             row['position_latitude'], row['position_longitude'], row['county']))

        logging.info('Committing changes to the database')
        self.session.commit()
