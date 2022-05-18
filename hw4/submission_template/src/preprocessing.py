import os.path as osp
import pandas as pd
import os
import calendar

def format_data(file):
    # format created date and closed data
    # parse_dates=['created_date','closed_date'])
    columns = ['created_date','closed_date','incident_zip']
    df = pd.read_csv(file,low_memory=False, usecols=[1,2,8], names=columns)
    df.dropna(inplace=True)
    # map_month = {'01':'Jan','02':'Feb','03':'Mar','04':'Apr','05':'May','06':'June','07':'July','08':'Aug','09':'Sep'}
    # df['month'] = df['month'].map(map_month)
    # df['month'] = pd.to_numeric(df['month'], errors='coerce')
    # df['month'] = df['month'].apply(lambda x: calendar.month_abbr[x])
    df['month']=df['closed_date'].str.slice(0,2)
    df['created_date'] = pd.to_datetime(df['created_date'], format='%m/%d/%Y %I:%M:%S %p')
    df['closed_date'] = pd.to_datetime(df['closed_date'], format='%m/%d/%Y %I:%M:%S %p')
    df['response_time'] = (df['closed_date'] - df['created_date']) / pd.Timedelta(hours=1)
    # df['month'] = df['closed_date'].dt.strftime('%b')
    # df['month'] = df['month'].astype(str)
    df = df[df['response_time']>=0]

    return df

def year_avg(data):
    df = data.copy()
    df['month'] = df['month'].astype(int)
    df['incident_zip'] = df['incident_zip'].astype(int)
    year_df = df.drop(['incident_zip'],axis=1)
    year_df = year_df.groupby(['month']).mean().reset_index()
    return year_df

def zip_avg(data):
    df = data.copy()
    df['month'] = df['month'].astype(int)
    df['incident_zip'] = df['incident_zip'].astype(int)
    zip_df = df.groupby(['month','incident_zip']).mean().reset_index()
    return zip_df