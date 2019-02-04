from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from db import data_query
from graph_maker import temp_graph, weather_widget, driving_widget
import datetime


# The app header. Contains: image path
app = Flask(__name__, static_url_path='/imgs/weather_icons', static_folder="imgs/weather_icons")


@app.route('/')
def index():
    return 'Hello, World!'


# The dashboard process
@app.route('/bokeh')
def bokeh():

    # Init temp graph class, update with the latest data, and then hold chart in memory
    a = temp_graph(zipcode='75204')
    a.update()
    temp = a.render_graph()

    # Init driving data class, update with the latest data, and then hold info in memory
    a = driving_widget(height=310, width=580)
    a.update()
    drive = a.render_widget()

    # Init weather data class, update with the latest data, and then hold info in memory
    a = weather_widget(zipcode='75204', height=310, width=580)
    a.update()
    weather = a.render_widget()

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # Checking time for night/dark mode
    live, _ = data_query(zipcode='75204')

    # If the current time in > sunrise in data, return dark-theme HTML in dashboard_dark.html
    if datetime.datetime.strptime(datetime.datetime.now().strftime('%H:%M:%S'),'%H:%M:%S').time() >= datetime.datetime.strptime(live['sunset'].tolist()[0], '%H:%M:%S').time():
        # Grabbing the scripts and div's from each graph and sending them out to the HTML to be viewed: {{ DATA }}
        script_temp, div_temp = components(temp)
        script2, div2 = components(drive)
        script3, div3 = components(weather)
        html = render_template(
            'dashboard_dark.html',
            script_temp=script_temp,
            div_temp=div_temp,
            plot_script2=script2,
            plot_div2=div2,
            plot_script3=script3,
            plot_div3=div3,
            js_resources=js_resources,
            css_resources=css_resources,
            zipcode='75204'
        )

        # Otherwise, return dashboard_light.html
    else:
        # Grabbing the scripts and div's from each graph and sending them out to the HTML to be viewed: {{ DATA }}
        script_temp, div_temp = components(temp)
        script2, div2 = components(drive)
        script3, div3 = components(weather)
        html = render_template(
            'dashboard_light.html',
            script_temp=script_temp,
            div_temp=div_temp,
            plot_script2=script2,
            plot_div2=div2,
            plot_script3=script3,
            plot_div3=div3,
            js_resources=js_resources,
            css_resources=css_resources,
            zipcode='75204'
        )

    # Encoding this shib
    return encode_utf8(html)

@app.route('/googlemapz')
def go():
    return render_template('/googlemapz.html')

if __name__ == '__main__':
    app.run(debug=True)