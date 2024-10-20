import os

from dotenv import load_dotenv

load_dotenv()

DB = {'drivername': os.environ.get('DB_DRIVER'),
      'username': os.environ.get('DB_USER'),
      'password': os.environ.get('DB_PASSWORD'),
      'host': os.environ.get('DB_HOST'),
      'port': os.environ.get('DB_PORT'),
      'database': os.environ.get('DB_NAME')}

DB_URL = f'''{DB['drivername']}://{DB['username']}:{DB['password']}@{DB['host']}:{DB['port']}/{DB['database']}'''
