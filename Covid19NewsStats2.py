import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from datetime import date
from dateutil.relativedelta import relativedelta

def generate_maps_2():
    five_months = date.today() + relativedelta(months=-5)
    date_param='-'.join(str(five_months).split('-')[0:2])+'-01'
    resp = requests.get('https://api.covid19india.org/data.json')
    
    resp_json = resp.json()
    daily_data = resp_json['cases_time_series']
    df = pd.DataFrame(daily_data)
    df['date'] = df['date'] + '2020'
    df['date'] = pd.to_datetime(df['date'])
    df.sort_values(by='date', ascending=True, inplace=True)
    df_avg_num = df[df['date'] > date_param].copy()
    df_avg_num['date'] = df_avg_num['date'].values.astype('datetime64[M]')
    df_avg_num['dailyconfirmed'] = df_avg_num['dailyconfirmed'].astype('int')
    df_avg_num['dailyrecovered'] = df_avg_num['dailyrecovered'].astype('int')
    df_avg_num['dailydeceased'] = df_avg_num['dailydeceased'].astype('int')
    
    df_avg_num = df_avg_num.groupby('date').agg(
        {'dailyconfirmed': 'mean', 'dailyrecovered': 'mean', 'dailydeceased': 'mean'})
    df_avg_num.reset_index(level=0, inplace=True)
    
    df_monthly_num = df[df['date'] > date_param].copy()
    df_monthly_num['Startdate'] = df_monthly_num['date'].values.astype('datetime64[M]')
    df_monthly_num['totalconfirmed'] = df_monthly_num['totalconfirmed'].astype('float')
    df_monthly_num['totalrecovered'] = df_monthly_num['totalrecovered'].astype('float')
    df_monthly_num['totaldeceased'] = df_monthly_num['totaldeceased'].astype('float')
    
    max_month_date_series = df_monthly_num.groupby('Startdate')['date'].max()
    df_monthly_num = df_monthly_num[df_monthly_num['date'].isin(max_month_date_series)]
    
    sns.set(style="darkgrid")
    fig, ax = plt.subplots(1, 2, figsize=(12, 6))
    ax[0].plot(df_avg_num['date'].dt.strftime('%b %Y'), df_avg_num['dailyconfirmed'], color="black", marker='o', lw=1,
               ls='-',
               label='Confirmed')
    ax[0].plot(df_avg_num['date'].dt.strftime('%b %Y'), df_avg_num['dailydeceased'], color="red", marker='o', lw=1, ls='-',
               label='Deceased')
    ax[0].plot(df_avg_num['date'].dt.strftime('%b %Y'), df_avg_num['dailyrecovered'], color="green", marker='o', lw=1,
               ls='-',
               label='Recovered')
    ax[0].set_title('Daily average counts')
    ax[0].legend(loc='upper left', frameon=False)
    df_monthly_num.reset_index(level=0, inplace=True)
    
    ax[1].plot(df_monthly_num['date'].dt.strftime('%b %Y'), df_monthly_num['totalconfirmed'], color="black", marker='o',
               lw=1, ls='-',
               label='Confirmed')
    ax[1].plot(df_monthly_num['date'].dt.strftime('%b %Y'), df_monthly_num['totaldeceased'], color="red", marker='o', lw=1,
               ls='-',
               label='Deceased')
    ax[1].plot(df_monthly_num['date'].dt.strftime('%b %Y'), df_monthly_num['totalrecovered'], color="green", marker='o',
               lw=1, ls='-',
               label='Recovered')
    ax[1].legend(loc='upper left', frameon=False)
    
    ax[1].ticklabel_format(style='plain', axis='y')
    
    ax[1].set_title('Monthly counts')
    
    plt.savefig('IndiaCovid-19Figures.jpg')
    print('Completed execution of Covid19NewsStats-2.py')
