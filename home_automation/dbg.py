from db import data_query


live, _ = data_query(zipcode='75204')

print(live['status'].tolist()[len()])