from weather_utils.openweather import data_get
from weather_utils.db import table_write
import pandas as pd

dallas_df = pd.read_csv('dallas_zips.csv')
dallas_zips = [str(x) for x in dallas_df['Key']]
key = '350abb3d7ac6d44ef002e103621f1052'

if __name__ == '__main__':

    # Looping through the zipcodes
    for zipcode in dallas_zips:

        # Grabbing data
        dallas_weather = data_get(zipcode=zipcode,
                                  key=key)
        # Writing data
        table_write(df=dallas_weather)
