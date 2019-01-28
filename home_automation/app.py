from flask import Flask, render_template
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.resources import INLINE
from bokeh.util.string import encode_utf8
from db import data_query
from graph_maker import temp_graph, weather_widget, driving_widget

app = Flask(__name__)


@app.route('/')
def index():
    return 'Hello, World!'

@app.route('/bokeh')
def bokeh():
    # x = data_query()['zipcode']
    # y = data_query()['temp']
    # # init a basic bar chart:
    # # http://bokeh.pydata.org/en/latest/docs/user_guide/plotting.html#bars
    # fig = figure(plot_width=1200, plot_height=600)
    # fig.vbar(
    #     x=[1, 2, 3, 4],
    #     width=0.5,
    #     bottom=0,
    #     top=[1.7, 2.2, 4.6, 3.9],
    #     color='navy'
    # )
    a = temp_graph(zipcode='75204', height=400, width=1100)
    a.update()
    temp = a.render_graph()

    a = driving_widget(height=310, width=580)
    a.update()
    drive = a.render_widget()

    a = weather_widget(zipcode='75204', height=310, width=580)
    a.update()
    weather = a.render_widget()

    # grab the static resources
    js_resources = INLINE.render_js()
    css_resources = INLINE.render_css()

    # render template
    script, div = components(temp)
    script2, div2 = components(drive)
    script3, div3 = components(weather)
    html = render_template(
        'index.html',
        plot_script=script,
        plot_div=div,
        plot_script2=script2,
        plot_div2=div2,
        plot_script3=script3,
        plot_div3=div3,
        js_resources=js_resources,
        css_resources=css_resources,
    )
    return encode_utf8(html)

@app.route('/googlemapz')
def go():
    render_template('googlemapz.html')
if __name__ == '__main__':
    app.run(debug=True)