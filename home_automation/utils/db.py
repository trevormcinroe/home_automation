import pandas as pd
from sqlalchemy import *
import time
import datetime



def data_query(zipcode):
    '''A helper function to pull in data
    Args:
    Returns:
    '''

    # Establishing a connection
    engine = create_engine('mysql+pymysql://weather_scraper:ThomasBayes69!@192.168.0.112/weather')
    con = engine.connect()

    # Pulling in live data
    live_df = pd.read_sql(sql="""SELECT * FROM dallas_weather where zipcode = \'%s\' and dte = \'%s\';"""%(zipcode, datetime.date.today()),
                          con=con)
    forecast_df = pd.read_sql(sql="""SELECT * FROM dallas_forecast where zipcode = \'%s\' and dte = \'%s\';"""%(zipcode, datetime.date.today()),
                              con=con)

    return live_df, forecast_df

    # This is the old version of the tempgraph div
    # <div style="width: 20%; display: inline-block; position:absolute; left:10px; top:500px;">
    #   {{ div_temp|indent(4)|safe }}
    #   {{ script_temp|indent(4)|safe }}
    # </div>