import tweepy
import random
import facebook
import schedule
import time
from datetime import datetime, timedelta
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd
import csv


def job():
    API_KEY = 'wwODKxfY1CmoRk5NeJVR8oxo5'
    API_SECRET_KEY = 'WRgxU0EzUledE4ljKaLFNMlmM7UTh5TjShyHZrVXCBUHyAmmCT'
    ACCESS_TOKEN = '1355379833900052480-0Suq6KPBPFbkcloD2U3qeJBshxbCIX'
    ACCESS_SECRET_TOKEN = 'avIjdZ60hCsJwtZJAsbNBsEe3HYRV7TSgWPsz7wPwuh8e'
    FACEBOOK_TOKEN = 'EAAnN4OmB3G4BAKjgSj0ZCz9Qm1wHoRmtAAsAi9P33bPa7RabN1ujNJTMkXr1hiiz4QYvVldOdeMbuaJpyQOjBJgLleGEVrv' \
                 'pJMt1jp97Gc9ZCFI46lOf9KG4VL9eRsNw2O91nkOBiSySoUE3yB93GZAU8OzhYi8bpgiolcEigZDZD'


    auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET_TOKEN)
    api = tweepy.API(auth)

    temp = 'Close'
    name = ''
    message = ''
    while temp == 'Close':
        lines = open('constituents_csv.csv').read().splitlines()
        stock = random.choice(lines)
        split = stock.split('\t')
        stock = split[0]
        name = split[1]
        tdf = yf.Ticker(stock)
        tickerDf = tdf.history(period='1d', start=(datetime.today() - timedelta(14)).strftime('%Y-%m-%d'))
        tickerDf.to_csv('out.csv')
        with open('out.csv', "r") as f1:
            last_line = f1.readlines()[-1]
            split = last_line.split(',')
            temp = split[4]

    seed = random.randint(0, 3)
    multiplier = 0
    exInfo = ''
    color = '#006400'

    if seed == 0:  # big up
        multiplier = random.uniform(3, 7)
        exInfo = 'is rocketing!'
        lines = open('rocket.txt').read().splitlines()
        message = message + random.choice(lines) + '\n'
    elif seed == 1:  # small up
        multiplier = random.uniform(1.1, 1.2)
        exInfo = 'is on the rise.'
        lines = open('rise.txt').read().splitlines()
        message = message + random.choice(lines) + '\n'
    elif seed == 2:  # small down
        multiplier = random.uniform(.7, .8)
        exInfo = 'is falling.'
        lines = open('bear.txt').read().splitlines()
        message = message + random.choice(lines) + '\n'
    elif seed == 3:  # big down
        multiplier = random.uniform(.1, .4)
        exInfo = 'is collapsing!'
        lines = open('collapse.txt').read().splitlines()
        message = message + random.choice(lines) + '\n'
    exInfo = name + ' ' + exInfo

    if random.randint(1, 10) < 3:
        lines = open('celebs.txt').read().splitlines()
        message = message + random.choice(lines) + '\n'

    if random.randint(1, 10) < 3:
        lines = open('coinq.txt').read().splitlines()
        message = message + random.choice(lines)
        lines = open('coins.txt').read().splitlines()
        message = message + random.choice(lines) + '\n'

    if seed > 1:
        color = "#FF0000"

    finalPrice = 0
    with open('out.csv', "r") as f1:
        last_line = f1.readlines()[-1]
        split = last_line.split(',')
        finalPrice = split[4]


    with open('out.csv', 'a') as stock:
        writer = csv.writer(stock, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        nextdate = datetime.today() + timedelta(1)
        newdays = 0
        while newdays < 1:
            if nextdate.weekday() < 5:
                if seed == 1:
                    writer.writerow([nextdate.strftime('%Y-%m-%d'), 100, 100, 100,
                                     float(finalPrice) + (random.uniform(.3, .6) * float(multiplier)), 100, 100, 100])
                elif seed < 2:
                    writer.writerow([nextdate.strftime('%Y-%m-%d'), 100, 100, 100,
                                     float(finalPrice) * (random.uniform(.3, .6) * float(multiplier)), 100, 100, 100])
                else:
                    writer.writerow([nextdate.strftime('%Y-%m-%d'), 100, 100, 100,
                                     float(finalPrice) * (random.uniform(1.1, 1.2) * float(multiplier)), 100, 100, 100])
                newdays = newdays + 1
            nextdate = nextdate + timedelta(1)
        while newdays < 2:
            if nextdate.weekday() < 5:
                writer.writerow([nextdate.strftime('%Y-%m-%d'), 100, 100, 100,
                                 float(finalPrice) * float(multiplier), 100, 100, 100])
                newdays = newdays + 1
            nextdate = nextdate + timedelta(1)

    tickerDf = pd.read_csv('out.csv')

    trace1 = {
        'x': tickerDf.Date,
        'y': tickerDf.Close,
        'type': 'scatter',
        'name': str(stock),
        'line_color': str(color),
        'showlegend': False
    }

    data = [trace1]
    # Config graph layout
    layout = go.Layout({
        'title': {
            'text': str(exInfo),
            'font': {
                'size': 15
            }
        }
    })
    fig = go.Figure(data=data, layout=layout)
    fig.write_image("fig.png")
    filename = 'fig.png'
    api.update_with_media(filename, message)
    graph = facebook.GraphAPI(FACEBOOK_TOKEN)
    post_id = graph.put_photo(image=open('fig.png', 'rb'), message=message)["post_id"]


schedule.every(30).minutes.do(job)
while True:
    schedule.run_pending()
    time.sleep(1)