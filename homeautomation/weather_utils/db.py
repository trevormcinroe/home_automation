from sqlalchemy import *
import pandas as pd

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
    sunrise VARCHAR(30),
    sunset VARCHAR(30)
    )
    """)

    # Closing
    cursor.close()

def delete_table():
    '''A helper function to delete the table'''
    import mysql.connector as mariadb

    # Connecting and init cursor
    mariadb_connection = mariadb.connect(user='weather_scraper', password='ThomasBayes69!',
                                         host='192.168.0.112', port='3306', database='weather')
    cursor = mariadb_connection.cursor()
    cursor.execute('''DROP TABLE dallas_weather''')
    mariadb_connection.commit()
    mariadb_connection.close()


def table_write(df):
    '''A helper function to write the data to the database
    Args:
        df: data, pandas
    Returns:
        nothing, written to the table
    '''

    # Creating the engine
    engine = create_engine('mysql+pymysql://weather_scraper:ThomasBayes69!@192.168.0.112/weather')
    try:
        con = engine.connect()
    except:
        try:
            con = engine.connect()
        except:
            try:
                con = engine.connect
            except:
                print('Can\'t see shit, captain...')
    # Writing
    df.to_sql(con=con, if_exists='append', name='dallas_weather', index=False)
