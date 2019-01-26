import pandas as pd
from sqlalchemy import *
import time
import matplotlib.pyplot as plt
from matplotlib import style
from bokeh.plotting import figure, output_file, show
import datetime
now = datetime.datetime.now
#
# x = [1, 2, 3, 4, 5]
# y = [6, 7, 8, 7, 3]
#
# # output_file("multiple.html")
#
# p = figure(plot_width=400, plot_height=400)
#
# # add both a line and circles on the same plot
# p.line(x, y, line_width=2)
# p.circle(x, y, fill_color="white", size=8)
#
# show(p)

def temp_graph(xdata, ydata, w, h):
    '''A helper function to plot data
    Args
    Returns
    '''
    plt = figure(plot_width=w, plot_height=h)
    plt.line(xdata, ydata, line_width=2)
    plt.circle(xdata, ydata, fill_color="white", size=8)
    return plt

# from db import data_query
# live, forecast = data_query()
# # print(data_query())
h = 'hi'
print('''THIS %s'''%h)