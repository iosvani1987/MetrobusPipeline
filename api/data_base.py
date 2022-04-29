from flask_mysqldb import MySQL
import os


class DataBase():
    def __init__(self, app):
        self.app = app
        # MySQL configurations
        self.app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
        self.app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
        self.app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
        self.app.config['MYSQL_DB'] = 'metrobus_db'
        self.app.config['MYSQL_PORT'] = 33066
        self.mysql = MySQL(app)
        with self.app.app_context():
            self.cur = self.mysql.connection.cursor()
            # self.cur.execute('''CREATE TABLE IF NOT EXISTS metrobus (
            #                     vehicle_id INT NOT NULL AUTO_INCREMENT,
            #                     name VARCHAR(255) NOT NULL,
            #                     PRIMARY KEY (vehicle_id)
            #                 )''')         # Create table if not exists
            
    def init_data_base(self):
        """
            This function is used to initialize the database.        """

        self.mysql = MySQL(self.app)
        with self.app.app_context():
            self.cur = self.mysql.connection.cursor()

    def close(self):
        """
            This function is used to close the connection.
        """
        self.cur.close()

    def get_metrobuses(self):
        """
            This function is used to get the metrobuses.
        """
        self.cur.execute('''SELECT * FROM metrobus''')
        rv = self.cur.fetchall()
        return rv

    def get_metrobuses_by_vehicle_id(self, vehicle_id):
        """
            This function is used to get the metrobuses by vehicle_id.
        """
        self.cur.execute('''SELECT * FROM metrobus WHERE vehicle_id = %s''', (vehicle_id,))
        rv = self.cur.fetchall()
        return rv

    def get_available_county(self):
        """
            This function is used to get the available counties.
        """
        self.cur.execute('''SELECT DISTINCT county FROM metrobus''')
        rv = self.cur.fetchall()
        return rv

    def get_metrobuses_by_county(self, county):
        """
            This function is used to get the metrobuses by county.
        """
        self.cur.execute('''SELECT * FROM metrobus WHERE county = %s''', (county,))
        rv = self.cur.fetchall()
        return rv

    def query(self, query):
        """
            This function is used to query the database.
        """
        self.cur.execute(query)
        rv = self.cur.fetchall()
        return rv



    