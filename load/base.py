from requests import Session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# engine = create_engine('mysql://root:Lucyaily*17@localhost/proyectoflask')
# engine = create_engine('mysql://root:root@localhost:33066/metrobus_db?unix_socket=/run/mysqld/mysqld.sock')
engine = create_engine('mysql://root:root1@192.168.1.115:33066/metrobus_db')

# engine = create_engine('sqlite:///metrobus.db')
Session = sessionmaker(bind=engine)

Base = declarative_base()