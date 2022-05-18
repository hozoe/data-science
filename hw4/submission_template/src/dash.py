from preprocessing import *
from bokeh.models.sources import ColumnDataSource
from bokeh.models import Dropdown, Select, tickers, FixedTicker, MonthsTicker
from bokeh.plotting import figure,curdoc
from bokeh.layouts import column

csv_file = "nyc_2020.csv"
curr_dir = osp.dirname(__file__)
path = osp.join(curr_dir,"..","data")
file_path = osp.join(path,csv_file)

df = format_data(file_path)
zip_list = df['incident_zip'].unique().astype(int).tolist()
zip_list = sorted(zip_list)
zip_list = list(map(str,zip_list))
zip_int = sorted(df['incident_zip'].unique().astype(int).tolist())
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep']

year_df = year_avg(df)
year_source = ColumnDataSource(year_df)

zip_df = zip_avg(df)
zip1 = {'month': [0], 'response_time': [0]}
zip2 = {'month': [0], 'response_time': [0]}
zip1_source = ColumnDataSource(data={'month': [0], 'response_time': [0]})
zip2_source = ColumnDataSource(data={'month': [0], 'response_time': [0]})

def callback1(attr,old,new):
    zip1_filter = zip_df[zip_df['incident_zip']== int(select_1.value)]
    zip1_source.data = {
        'month':zip1_filter['month'],
        'response_time':zip1_filter['response_time']
    }
    

def callback2(attr,old,new):
    zip2_filter = zip_df[zip_df['incident_zip']== int(select_2.value)]
    zip2_source.data = {
        'month':zip2_filter['month'],
        'response_time':zip2_filter['response_time']
    }
    

select_1 = Select(title="Zip code 1", options = zip_list, value = None)
select_2 = Select(title="Zip code 2", options = zip_list, value = None)

select_1.on_change('value',callback1)
select_2.on_change('value',callback2)

p = figure(
    title="Monthly average incident create-to-closed time (in hours)",
    title_location="above",
    x_axis_label="Month",x_axis_type="month",
    y_axis_label="Average response time")

p.xaxis.ticker = FixedTicker(ticks=list(range(1,13)))
p.title.align = 'center'
p.line('month','response_time',legend_label="all 2020 data",source=year_source,line_color="red",line_width=2)
p.line('month','response_time',legend_label="zip code 1",source=zip1_source,line_color="blue",line_width=2)
p.line('month','response_time',legend_label="zip code 2",source=zip2_source,line_color="yellow",line_width=2)

curdoc().add_root(column(select_1,select_2,p))