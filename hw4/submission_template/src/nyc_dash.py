from preprocessing import *
from bokeh.models.sources import ColumnDataSource
from bokeh.models import Dropdown, Select
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
months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

year_df = year_avg(df)
year_source = ColumnDataSource(year_df)

zip_df = zip_avg(df)
zip1 = zip_df[zip_df['incident_zip']==zip_int[0]] #83
zip2 = zip_df[zip_df['incident_zip']==zip_int[1]] #10000
zip1_source = ColumnDataSource(zip1)
zip2_source = ColumnDataSource(zip2)

menu_1 = Dropdown(label="Zip code 1", button_type="default", menu=zip_list)
menu_2 = Dropdown(label="Zip code 2", button_type="default", menu=zip_list)


def callback1(event):
    zip1_filter = zip_df[zip_df['incident_zip']== int(event.item)]
    zip1_source.data = zip1_filter
    print(f'zip code 1: {event.item}')

menu_1.on_click(callback1)

def callback2(event):
    zip2_filter = zip_df[zip_df['incident_zip']== int(event.item)]
    zip2_source.data = zip2_filter
    print(f'zip code 2: {event.item}')
    
menu_2.on_click(callback2)

p = figure(
    title="Monthly average incident create-to-closed time (in hours)",
    title_location="right",
    x_axis_label="Month",x_range=months,
    y_axis_label="Average response time")
p.title.align = 'center'
p.line(x="month",y="response_time",legend_label="all 2020 data",source=year_source,line_color="red",line_width=2)
p.line(x="month",y="response_time",legend_label="zip code 1",source=zip1_source,line_color="blue",line_width=2)
p.line(x="month",y="response_time",legend_label="zip code 2",source=zip2_source,line_color="yellow",line_width=2)

curdoc().add_root(column(menu_1,menu_2,p))