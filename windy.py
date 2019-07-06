from yr.libyr import Yr
import json
import urllib.request
from bs4 import BeautifulSoup
import datetime
import re

DEBUG = True
MPS_TO_KTS = 1.9438445
KTS_TO_MPS = 0.5144444

class Forcast:
    def __init__(self, date='', hour='', comb_date='', temp=0, wind_dir='', wind_speed_kts=0, wind_speed_mps=0, prec=0):
        self.date = date
        self.hour = hour
        self.comb_date = date +' '+ hour
        self.temp = temp
        self.wind_dir = wind_dir
        self.wind_speed_kts = wind_speed_kts
        self.wind_speed_mps = wind_speed_mps
        self.prec = prec

def yrno(location):
    locs = {'Chałupy':'Poland/Pomerania/Chałupy/', 'Jastarnia':'Poland/Pomerania/Jastarnia/', 
            'Jurata':'Poland/Pomerania/Jurata/', 'Kadyny':'Poland/Warmia-Masuria/Kadyny/',
            'Kuźnica':'Poland/Pomerania/Kuźnica/', 'Rewa':'Poland/Pomerania/Rewa/'}
    
    weather = Yr(location_name = locs[location])
    forecasts = []
    
    for fcast in weather.forecast():
        date = fcast['@from'].replace('T', ' ')[0:-3]
        temp = int(fcast['temperature']['@value'])
        wind_dir = fcast['windDirection']['@code']
        wind_speed_mps = int(float(fcast['windSpeed']['@mps']))
        wind_speed_kts = int(wind_speed_mps * KTS_TO_MPS)
        prec = float(fcast['precipitation']['@value'])

        pretty_date = re.search(r'\d{4}-(\d{2})-(\d{2}) (\d{2})', date)
        date = (pretty_date.group(2)+'.'+pretty_date.group(1))
        hour = pretty_date.group(3)+':00'

        forecast = Forcast(date = date, hour = hour, temp = temp, wind_dir = wind_dir,
                            wind_speed_kts = wind_speed_kts, wind_speed_mps = wind_speed_mps, prec = prec)
        forecasts.append(forecast)

    return forecasts
    

def wfinder(location):
    locs = {'Chałupy':'hel_chalupy', 'Jastarnia':'jastarnia',
            'Jurata':'jurata_hel', 'Kadyny':'kadyny',
            'Kuźnica':'jastarnia', 'Rewa':'cypel'}
    months = {'Jan':'01', 'Feb':'02', 'Mar':'03', 'Apr':'04', 'May':'05', 'Jun':'06', 
              'Jul':'07', 'Aug':'08', 'Sep':'09', 'Oct':'10', 'Nov':'11', 'Dec':'12'}

    if DEBUG:
        with open('pogoda.html', 'r') as file:
            html = file.read()
    else:
        with urllib.request.urlopen('https://www.windfinder.com/forecast/'+locs[location]) as www:
            html = www.read().decode('utf-8')
            with open('pogoda.html', 'w') as file:
                file.write(html)

    soup = BeautifulSoup(html, 'html.parser')
    days_data = soup.find_all(class_='weathertable')

    forecasts = []
    t = int(datetime.datetime.now().strftime('%H'))

    for day in days_data:
        time_rows = day.select('.data-time > span')
        temperature = day.find_all(class_='units-at')
        wind_direction = day.find_all(class_='units-wd-dir')
        wind_speed = day.find_all(class_='units-ws')
        precipitation = day.select('div.data-rain.data--minor.weathertable__cell')
        prec_table = []
        
        for p in precipitation:
            r = p.select('span.units-pr')
            if r:
                value = r[0].get_text()
            else:
                value = '0'
            prec_table.append(value)

        for i in range(len(time_rows)):
            date = day.h4.get_text().strip() + ' ' + time_rows[i].get_text()
            temp = int(temperature[i].get_text())
            wind_dir = wind_direction[i].get_text().replace(' ', '').replace('\n', '')
            wind_speed_kts = int(wind_speed[i].get_text().replace('\n', ''))
            wind_speed_mps = int(wind_speed_kts * MPS_TO_KTS)
            prec = int(prec_table[i])

            pretty_date = re.search(r'\w+, (\w+) (\d{2}) (\d{2})', date)
            m = months[pretty_date.group(1)]
            date = (pretty_date.group(2)+'.'+str(m))
            hour = pretty_date.group(3)+':00'

            forecast = Forcast(date = date, hour = hour, temp = temp, wind_dir = wind_dir,
                                wind_speed_kts = wind_speed_kts, wind_speed_mps = wind_speed_mps, prec = prec)
            forecasts.append(forecast)
    
    return forecasts[0::2]
