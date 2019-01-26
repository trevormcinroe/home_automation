import pandas as pd
from bokeh.plotting import figure, output_file, show
import datetime
from db import data_query
import numpy as np


class temp_graph():
    '''
    A class to make temperature graphs
    '''
    def __init__(self, live, forecast):
        self.live = live
        self.forecast = forecast
        self.zipcode = self.forecast['zipcode']
        self.today = datetime.date.today()

    def data_arrange(self):
        '''A function to rearrange the data in order to
        '''



live, forecast = data_query(zipcode=75204)
print(forecast)
a = temp_graph(live=live, forecast=forecast)
# a.data_arrange()
# print(a.forecast)