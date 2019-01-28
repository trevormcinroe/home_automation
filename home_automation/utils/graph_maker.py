import pandas as pd
from bokeh.plotting import figure, output_file, show, ColumnDataSource
from bokeh.models import Band, grids
from bokeh.models.glyphs import Text
import datetime
from db import data_query
import numpy as np
from bokeh.models.widgets import DataTable, DateFormatter, TableColumn
from bokeh.layouts import widgetbox
from googlemaps.googlemaps_api import get_distance



class temp_graph():
    '''
    A class to make temperature graphs
    '''
    def __init__(self, zipcode, width, height):
        self.live = None
        self.forecast = None
        self.zipcode = zipcode
        self.today = datetime.date.today()
        self.xaxis_live = None
        self.xaxis_forecast = None
        self.live_temp = None
        self.forecat_high = None
        self.forecast_low = None
        self.forecast_df = None
        self.width = width
        self.height = height
        self.mode = None
        self.current_time = datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M:%S'),'%H:%M:%S').time()

    def update(self):
        '''A function to rearrange the data in order to
        '''
        # Querying the data
        self.live, self.forecast = data_query(zipcode=self.zipcode)
        # Setting the xaxis
        temp_today = datetime.datetime.strptime(datetime.date.today().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
        l = [temp_today]
        for n in range(146):
            temp_today += datetime.timedelta(minutes=10)
            l.append(temp_today)
        self.xaxis_live = l

        temp_today = datetime.datetime.strptime(datetime.date.today().strftime('%Y-%m-%d %H:%M'), '%Y-%m-%d %H:%M')
        l2 = [temp_today]
        for n in range(7):
            temp_today += datetime.timedelta(hours=3)
            l2.append(temp_today)
        self.xaxis_forecast = l2[3:]

        # Setting temperatures
        self.live_temp = self.live['temp'].tolist()
        self.forecast_df = pd.DataFrame({'low': self.forecast['temp_min'].tolist(),
                                      'high': self.forecast['temp_max'].tolist()})
        self.forecat_high = self.forecast['temp_max'].tolist()
        self.forecast_low = self.forecast['temp_min'].tolist()

        # Setting mode
        if self.current_time >= datetime.datetime.strptime(self.live['sunset'].tolist()[0],'%H:%M:%S').time() or self.current_time >= datetime.datetime.strptime(self.live['sunset'].tolist()[0], '%H:%M:%S').time():
            self.mode = 'night'
        else:
            self.mode = 'day'


    def render_graph(self):
        '''A function that outputs the graph
        '''
        p = figure(
            plot_width = self.width,
            plot_height = self.height,
            y_range=[np.min([np.min(self.forecast_low), np.min(self.live_temp)]) - 1,
                            np.max([np.max(self.live_temp), np.max(self.forecat_high)]) + 1],
            # title='Temperature for %s' % self.zipcode,
            # x_axis_label='time',
            # y_axis_label='temperature (F)',
            x_axis_type='datetime'
        )

        # p.title.text_font_size = '25pt'
        # p.title.text_color = "olive"
        # p.title.text_font = "roboto"
        # p.title.text_font_style = "italic"

        # Light mode vs dark mode
        if self.mode == 'night':

            # === TEMPERATURE PLOT DARK/NIGHT MODE === #
            # Data (live, high, low)
            p.line(x=self.xaxis_live, y=self.live_temp, line_color='#e4c46d', line_cap='round', line_width=9,
                   line_alpha=1, line_join='round')
            # p.circle(x=self.xaxis_live, y=self.live_temp,
            #          fill_color='#937cb3', line_color=None, size=4, alpha=1)

            p.circle(x=self.xaxis_live[len(self.live_temp)-1],
                     y=self.live_temp[len(self.live_temp)-1],
                     fill_color='#191970', line_color=None, size=8, alpha=0.65)

            p.circle(x=self.xaxis_forecast, y=self.forecat_high, fill_color='#aa4926',
                     size=16, line_color=None, alpha=1)

            p.circle(x=self.xaxis_forecast, y=self.forecast_low, fill_color='#6797bb',
                     size=14, line_color=None, alpha=1)

            # Text
            source = ColumnDataSource(dict(x=[self.xaxis_live[len(self.live_temp) - 1]],
                                           y=[self.live_temp[len(self.live_temp) - 1]],
                                           text=[str(self.live_temp[len(self.live_temp) - 1])]))
            glyph = Text(x="x", y="y", text="text", angle=0, text_color="#e4c46d", text_font_size='14pt')
            p.add_glyph(source, glyph)

            # Axes (x, y)
            p.xaxis.axis_line_width = 0
            p.xaxis.axis_label_text_font_size = '15pt'
            p.xaxis.major_label_text_font_size = '13pt'
            p.xaxis.major_label_text_color = "#6a8759"

            p.yaxis.axis_line_width = 0
            p.yaxis.axis_label_text_font_size = '15pt'
            p.yaxis.major_label_text_font_size = '13pt'
            p.yaxis.major_label_text_color = "#6a8759"

            # Gridlines
            p.xgrid.grid_line_color = '#515658'
            p.ygrid.grid_line_color = '#515658'

            p.xgrid.grid_line_width = 3
            p.ygrid.grid_line_width = 3

            # Background
            p.background_fill_color = '#313335'
            p.background_fill_alpha = 0.95

            # Border
            p.outline_line_width = 10
            p.outline_line_alpha = 1
            p.outline_line_color = "#515658"
            p.border_fill_color = "#2b2b2b"

            # Misc
            p.toolbar.logo = None
            p.toolbar_location = None

            p.min_border_left = 23
            p.min_border_right = 23
            p.min_border_top = 23

            return p

        else:

            # === TEMPERATURE PLOT LIGHT MODE === #
            # Data (live, high, low)
            p.line(x=self.xaxis_live, y=self.live_temp, line_color='#4ABDAC', line_cap='round', line_width=6,
                   line_alpha=0.65, line_join='round')

            p.circle(x=self.xaxis_live, y=self.live_temp,
                     fill_color='#111e6c', line_color=None, size=4, alpha=0.65)

            p.circle(x=self.xaxis_live[len(self.live_temp)-1],
                     y=self.live_temp[len(self.live_temp)-1],
                     fill_color='#111e6c', line_color=None, size=8, alpha=0.65)

            # Text
            source = ColumnDataSource(dict(x=[self.xaxis_live[len(self.live_temp)-1]],
                                           y=[self.live_temp[len(self.live_temp)-1]],
                                           text=[str(self.live_temp[len(self.live_temp)-1])]))
            glyph = Text(x="x", y="y", text="text", angle=0, text_color="#000000", text_font_size='14pt')
            p.add_glyph(source, glyph)


            p.circle(x=self.xaxis_forecast, y=self.forecat_high,
                     fill_color='#e0474c', size=16, line_color=None, alpha=0.85)

            p.circle(x=self.xaxis_forecast, y=self.forecast_low,
                     fill_color='#7acfd6', size=14, line_color=None, alpha=0.85)


            # Axes (x, y)
            p.xaxis.axis_line_width = 0
            p.xaxis.axis_label_text_font_size = '15pt'
            p.xaxis.major_label_text_font_size = '13pt'

            p.yaxis.axis_line_width = 0
            p.yaxis.axis_label_text_font_size = '15pt'
            p.yaxis.major_label_text_font_size = '13pt'

            # Gridlines
            p.xgrid.grid_line_color = '#ffffff'
            p.ygrid.grid_line_color = '#ffffff'

            p.xgrid.grid_line_width = 3
            p.ygrid.grid_line_width = 3

            # Background
            p.background_fill_color = '#DFDCE3'
            p.background_fill_alpha = 0.95

            # Border
            p.outline_line_width = 10
            p.outline_line_alpha = 0.85
            p.outline_line_color = "#00303F"

            # Misc
            p.toolbar.logo = None
            p.toolbar_location = None

            return p


class weather_widget():
    '''A class for the weather summary
    '''

    def __init__(self, zipcode, width, height):
        self.width = width
        self.height = height
        self.zipcode = zipcode
        self.status = None
        self.live = None
        self.humidity = None
        self.wind = None

    def update(self):
        '''

        :return:
        '''
        self.live, _ = data_query(zipcode=self.zipcode)
        self.status = self.live['status'].tolist()[len(self.live)-1]
        self.humidity = self.live['humidity'].tolist()[len(self.live)-1]
        self.wind = self.live['wind'].tolist()[len(self.live)-1]
    def render_widget(self):
        # p = figure(
        #     plot_width=self.width,
        #     plot_height=self.height,
        #     y_range=[0, 10]
        #     # title='Temperature for %s' % self.zipcode,
        #     # x_axis_label='time',
        #     # y_axis_label='temperature (F)',
        #     # x_axis_type='datetime'
        # )
        # # Text
        # source = ColumnDataSource(dict(x=[10],
        #                                    y=[8],
        #                                    text=[self.status]))
        # glyph = Text(x="x", y="y", text="text", angle=0, text_color="#000000", text_font_size='12pt')
        # p.add_glyph(source, glyph)
        #
        #
        # # Axes
        # p.axis.visible = False
        #
        # # Grids
        # p.grid.visible = False
        #
        # # Border
        # p.outline_line_width = 10
        # p.outline_line_alpha = 0.85
        # p.outline_line_color = "#00303F"
        #
        # # Misc
        # p.toolbar.logo = None
        # p.toolbar_location = None

        data = dict(
            Status=[self.status],
            Wind=[self.wind],
            Humidity=[self.humidity]
        )
        source = ColumnDataSource(data)

        columns = [
            TableColumn(field="Status", title="Status"),
            TableColumn(field="Wind", title="Wind"),
            TableColumn(field='Humidity', title='Humidity')
        ]
        data_table = DataTable(source=source, columns=columns, width=400, height=280)

        return widgetbox(data_table)

class driving_widget():
    '''

    '''
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.distance = None
        self.duration = None
        self.home = {'lat': 32.8089545, 'lon':-96.7971913}
        self.kelly_work = {'lat': 32.7638607, 'lon': -97.8018728}
        self.current_time = datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M:%S'), '%H:%M:%S').time()

    def update(self):
        '''A function to update the driving widget data
        '''

        # Morning vs night traffic:
        # Setting mode
        if self.current_time <= datetime.datetime.strptime('15:30:00', '%H:%M:%S').time():

            self.distance = get_distance(origin=self.home, destination=self.kelly_work)['distance']
            self.duration = get_distance(origin=self.home, destination=self.kelly_work)['duration']

        else:

            self.distance = get_distance(origin=self.kelly_work, destination=self.home)['distance']
            self.duration = get_distance(origin=self.kelly_work, destination=self.home)['duration']

    def render_widget(self):
        '''A function to render the table information
        '''
        data = dict(
            Distance=[self.distance],
            Duration=[self.duration]
        )
        source = ColumnDataSource(data)

        columns = [
            TableColumn(field="Distance", title="Distance"),
            TableColumn(field="Duration", title="Duration")
        ]
        data_table = DataTable(source=source, columns=columns, width=400, height=280)

        return widgetbox(data_table)

class gmap():
    '''
    '''

    def __init__(self):
        pass

    def map(self):
        pass