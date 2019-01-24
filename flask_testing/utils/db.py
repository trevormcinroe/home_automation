import pandas as pd
from sqlalchemy import *
import time



def data_query():
    '''A helper function to pull in data
    Args:

    Returns:

    '''

    # Establishing a connection
    engine = create_engine('mysql+pymysql://weather_scraper:ThomasBayes69!@192.168.0.112/weather')
    con = engine.connect()

    # Pulling in live data
    live_df = pd.read_sql(sql="""SELECT * FROM dallas_weather where zipcode = \'75204\' limit 10;""", con=con)

    return live_df


#
# engine = create_engine('mysql+pymysql://weather_scraper:ThomasBayes69!@192.168.0.112/weather')
# try:
#     con = engine.connect()
# except:
#     try:
#         con = engine.connect()
#     except:
#         try:
#             con = engine.connect
#         except:
#             print('Can\'t see shit, captain...')
# # Writing
# df.to_sql(con=con, if_exists='append', name='dallas_weather', index=False)


def create_table():
    '''A helper function that creates the table for weather'''
    import mysql.connector as mariadb

    # Connecting and init cursor
    mariadb_connection = mariadb.connect(user='weather_scraper', password='ThomasBayes69!',
                                         host='192.168.0.112', port='3306', database='weather')
    cursor = mariadb_connection.cursor()

    # Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS dallas_weather(
    zipcode VARCHAR(10),
    lat VARCHAR(8),
    lon VARCHAR(8),
    status VARCHAR(30),
    temp FLOAT,
    pressure INT,
    humidity INT,
    temp_min FLOAT,
    temp_max FLOAT,
    wind FLOAT,
    this_time VARCHAR(30),
    sunrise VARCHAR(30),
    sunset VARCHAR(30),
    dte DATE
    )
    """)