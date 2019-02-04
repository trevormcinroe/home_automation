from googlemaps.googlemaps_api import get_distance
import datetime
from db import data_query
# print(datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M:%S'),'%H:%M:%S').time())

live, _ = data_query(zipcode='75204')

print(datetime.datetime.strptime(live['sunset'].tolist()[0], '%H:%M:%S').time()
      )



