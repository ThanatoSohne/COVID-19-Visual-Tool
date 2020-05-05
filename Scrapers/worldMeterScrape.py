import bs4
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup as soup
import pandas as pd

gebMeter = 'https://www.worldometers.info/coronavirus/'
bypass = {'User-Agent': 'Mozilla/5.0'}
gebClient = Request(gebMeter, headers=bypass)
gebPage = urlopen(gebClient)

site_parse = soup(gebPage, 'lxml')
gebPage.close()

ctry = site_parse.find("div", {"id":"nav-today"}).find('tbody').findAll('a')
tables = site_parse.find("div", {"id":"nav-today"}).find('tbody').findAll('tr')

countryCont = []
for c in ctry:
    pull = c.text
    countryCont.append(pull)

dataCont = []
for t in tables:
    take = t.text
    dataCont.append(take)
    
csvfile = "COVID-19_cases_worldMeters.csv"
headers = "Country,Total Cases,New Cases,Total Deaths,New Deaths,Total Recovered,Active Cases,Serious/Critical,Total Tested\n"

file = open(csvfile, "w", encoding='Latin-1')
file.write(headers)

for d in dataCont[8:]:
    zbornak = d.split('\n')
    file.write(zbornak[1] + "," + zbornak[2].replace(',','') + "," 
               + zbornak[3].replace(',','').strip('+') + "," 
               + zbornak[4].replace(',','') + "," 
               + zbornak[5].replace(',','').strip('+') + "," 
               + zbornak[6].replace(',','') + "," 
               + zbornak[7].replace(',','') + "," 
               + zbornak[8].replace(',','') + "," 
               + zbornak[11].replace(',','') + "\n")
    
file.close()

