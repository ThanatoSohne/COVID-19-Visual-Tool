import json
import os, glob
import csv
from urllib.request import Request, urlopen
from urllib.request import urlopen as req
from bs4 import BeautifulSoup as soup
from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut
import geocoder
from time import sleep
import addfips
import pandas as pd
import wikipedia
from termcolor import colored as cl

#Used to catch a time out from the Nominatim servers and continue to try
#running the code until it responds
#Information for this code and the code for the Nominatim and geopy comes 
#from their documentation: https://geopy.readthedocs.io/en/stable/#
#and from StackOverflow https://stackoverflow.com/a/48039673
def catch_TimeOut(locale):
    liegen = Nominatim(user_agent = 'combiner-atomeundwolke@gmail.com')
    try:
        return liegen.geocode(locale)
    except GeocoderTimedOut:
        return catch_TimeOut(locale)

liegen = Nominatim(user_agent = 'combiner-atomeundwolke@gmail.com')

#This module gets fips (Federal Information Processing Standards) codes for each county
#This is necessary for the building of the plotly maps that will be used in the
#web app
fips = addfips.AddFIPS()
#Constant counter to ensure that all files have been compiled before
#they are combined into one CSV
counter = 0

#Each state/ territory will have a scraper. Some will be combined
#for a more efficient or easy to view map in the web app

#A great deal of what is happening below is thanks in part to the documentation
#for BS4 found on https://www.crummy.com/software/BeautifulSoup/bs4/doc/

#I have wrapped each def in a try/except condition in order to allow
#the program to run unhindered. My reasoning for this being that even if the 
#scraper here does not work then the maps/charts in the app will still be able 
#to run even if it is data from the day before. 

def akScrape():
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        akWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Alaska'
        akClient = req(akWiki)
        site_parse = soup(akClient.read(), "lxml")
        akClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        #CSV file name and header
        csvfile = "COVID-19_cases_akWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
          
        ak = "ALASKA"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        
        for t in tables:
                pull = t.findAll('tr')
                for p in pull:
                    take = p.get_text()
                    hold.append(take)
        
        #Break the list into the separate counties (or in this case, boroughs)            
        #Aleutians East Borough
        alEast = hold[2].split('\n')
        alfips = fips.get_county_fips(alEast[1], state = ak)
        #Anchorage
        anrage = hold[3].split('\n')
        anfips = fips.get_county_fips(anrage[1], state = ak)
        #Bristol Bay Borough
        brist = hold[4].split('\n')
        brfips = fips.get_county_fips(brist[1], state = ak)
        #Denali Borough
        denali = hold[5].split('\n')
        defips = fips.get_county_fips(denali[1], state = ak)
        #Fairbanks North Star Borough
        fair = hold[6].split('\n')
        ffips = fips.get_county_fips(fair[1], state = ak)
        #Haines Borough
        haines = hold[7].split('\n')
        hafips = fips.get_county_fips(haines[1], state = ak)
        #Juneau
        juneau = hold[8].split('\n')
        jfips = fips.get_county_fips(juneau[1], state = ak)
        #Kenai Peninsula Borough
        kenai = hold[9].split('\n')
        kenfips = fips.get_county_fips(kenai[1], state = ak)
        #Ketchikan Gateway Borough
        ketch = hold[10].split('\n')
        ketfips = fips.get_county_fips(ketch[1], state = ak)
        #Kodiak Island Borough
        kodiak = hold[11].split('\n')
        kofips = fips.get_county_fips(kodiak[1], state = ak)
        #Lake and Peninsula Borough
        lake = hold[12].split('\n')
        lafips = fips.get_county_fips(lake[1], state = ak)
        #Matanuska-Susitna Borough
        matsu = hold[13].split('\n')
        matfips = fips.get_county_fips(matsu[1], state = ak)
        #North Slope Borough
        north = hold[14].split('\n')
        npfips = fips.get_county_fips(north[1], state = ak)
        #Northwest Arctic Borough
        nwest = hold[15].split('\n')
        nwfips = fips.get_county_fips(nwest[1], state = ak)
        #Petersburg Borough
        peters = hold[16].split('\n')
        pfips = fips.get_county_fips(peters[1], state = ak)
        #Sitka
        sitka = hold[17].split('\n')
        sfips = fips.get_county_fips(sitka[1], state = ak)
        #Skagway
        skway = hold[18].split('\n')
        skfips = fips.get_county_fips(skway[1], state = ak)
        #Wrangell
        wran = hold[19].split('\n')
        wfips = fips.get_county_fips(wran[1], state = ak)
        #Yakutat
        yak = hold[20].split('\n')
        yafips = fips.get_county_fips(yak[1], state = ak)
        #Aleutians West Census Area
        alWest = hold[21].split('\n')
        awfips = fips.get_county_fips(alWest[1], state = ak)
        #Bethel Census Borough
        bethel = hold[22].split('\n')
        befips = fips.get_county_fips(bethel[1], state = ak)
        #Chugach Census Area
        chugach = hold[23].split('\n')
        chfips = "02261"
        #Copper River Census Area
        copper = hold[24].split('\n')
        cufips = "0"
        #Dillingham Census Area
        dill = hold[25].split('\n')
        dfips = fips.get_county_fips(dill[1], state = ak)
        #Hoonah-Angoon Census Area
        hoon = hold[26].split('\n')
        hofips = "0"
        #Kusilvak Census Area
        kusil = hold[27].split('\n')
        kvfips = fips.get_county_fips(kusil[1], state = ak)
        #Nome Census Area
        nome = hold[28].split('\n')
        nofips = fips.get_county_fips(nome[1], state = ak)
        #Prince of Wales- Hyder Census Area
        wales = hold[29].split('\n')
        wafips = fips.get_county_fips(wales[1], state = ak)
        #Southeast Fairbanks Census Area
        seFair = hold[30].split('\n')
        sefips = fips.get_county_fips(seFair[1], state = ak)
        #Yukon-Koyukuk Census Area
        yukon = hold[31].split('\n')
        yufips = fips.get_county_fips(yukon[1], state = ak)
        
        #Place it into another list. This will make it easier to write into file
        container = []
        container = [alEast, anrage, brist, denali, fair, haines, 
                     juneau, kenai, ketch, kodiak, lake, matsu, north, 
                     nwest, peters, sitka, skway, wran, yak, alWest, 
                     bethel, chugach, copper, dill, hoon, kusil, 
                     nome, wales, seFair, yukon]
        #Place the borough names into a list 
        akCounty = []
        akCounty = [alEast[1], anrage[1], brist[1], denali[1], fair[1], haines[1], 
                     juneau[1], kenai[1], ketch[1], kodiak[1], lake[1], matsu[1], north[1], 
                     nwest[1], peters[1], sitka[1], skway[1], wran[1], yak[1], alWest[1], 
                     bethel[1], chugach[1], copper[1], dill[1], "Hoonah Angoon Census Burough", 
                     kusil[1], nome[1], wales[1], seFair[1], yukon[1]]
        #Place the attained fips codes into another list
        fipsCnt = []
        fipsCnt = [alfips, anfips, brfips, defips, ffips, hafips, jfips, 
                   kenfips, ketfips, kofips, lafips, matfips, npfips, nwfips, 
                   pfips, sfips, skfips, wfips, yafips, awfips, befips, chfips, 
                   cufips, dfips, hofips, kvfips, nofips, wafips, sefips, yufips]
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (alEast[1]) == 'Aleutians East Borough' and (yukon[1]) == 'Yukon-Koyukuk Census Area':
            
            file = open(csvfile, "w")
            file.write(headers)
            
            for n in range(0,30):
                file.write(str(akCounty[n]) + "," + ak + "," + str(fipsCnt[n]) + "," 
                           + str(geocoder.opencage(container[n][1] + ", " + ak, key='').latlng).strip('[]') + "," 
                           + str(container[n][3]) + "," + str(container[n][5]) + "," + str(container[n][7]) + "\n")
            
            file.close()
            
            counter += 1
            print("Alaska scraper complete.")
        else:
            print(cl("ERROR: Must fix Alaska scraper.", 'red'))
    
    except Exception:
        print(cl('Printed or exception raised for AK scraper.', 'green'))
        pass
    
def alScrape():
    
    try:
        #Grab and hold the information from the json inside of rJs
        aldoh = 'https://services7.arcgis.com/4RQmZZ0yaZkGR1zy/arcgis/rest/services/COV19_Public_Dashboard_ReadOnly/FeatureServer/0/query?where=1%3D1&outFields=CNTYNAME%2CCNTYFIPS%2CCONFIRMED%2CDIED&returnGeometry=false&f=pjson'
        alClient = req(aldoh).read().decode('utf-8')
        rJS = json.loads(alClient)
        
        #Grab the features portion of the json's dictionary
        attr = rJS.get('features')
        
        #CSV file name and header
        csvfile = "COVID-19_cases_aldoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        al = "ALABAMA"
        
        #Use this as a test to ensure that the information garnered is pertinent
        #Do note that as of 4/15/2020, the json continuously changes the first 
        #CNTYNAME attribute
        test = []
        if(attr[0].get('attributes').get('CNTYNAME')) == 'Blount':
            test = True
        else:
            test = False
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if test == True:
        
            file = open(csvfile, "w")
            file.write(headers)
            
            for a in attr:
                file.write(a.get('attributes').get('CNTYNAME') + "," + "ALABAMA" + "," + str(fips.get_county_fips(a.get('attributes').get('CNTYNAME'), state=al)).strip() + ","
                           + str(geocoder.opencage(a.get('attributes').get('CNTYNAME') + ", " + " ALABAMA", key='').latlng).strip('[]') + "," 
                           + str(a.get('attributes').get('CONFIRMED')) + "," + str(a.get('attributes').get('DIED')) + "\n")
            
            file.close()
            
            counter += 1
            print("Alabama scraper is complete.")
        else:
            print(cl("ERROR: Must fix Alabama scraper.", 'red'))
    
    except Exception:
        print(cl('Printed or exception raised for AL scraper.', 'green'))
        pass
    
def arScrape():
    
    try:
        #This scraper is a bit different
        #First we want to ensure that we are receiving updated information
        #so we pull the information from the page and look for the csv that is 
        #most current
        testUrl = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports'
        testClient = req(testUrl)
        site_parse = soup(testClient.read(), 'lxml')
        testClient.close()
        tables = site_parse.find("div", {"class": "Box mb-3 Box--condensed"})
        tags = tables.find('tbody')
        att = tags.findAll('tr', {"class":"js-navigation-item"})[-2]
        current = att.find('a').text
        #This is the base url sans newest csv file
        git = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
        #Concatenate the two now... Base url and latest csv 
        newUrl = git + current
        #Now we place this into a DataFrame
        df = pd.read_csv(newUrl)
        #From here this is all a matter of cleaning and grouping data by the 
        #categories needed and made into a Dataframe similar to the others in this
        #large scraper
        arDF = df.groupby('Province_State').get_group('Arkansas')
        arkie = arDF[arDF.Admin2 != 'Unassigned']
        hold = arkie.reindex(columns = ['Admin2', 'Province_State', 'FIPS', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered'])
        arHold = hold.rename(columns = {'Admin2' : 'County', 'Province_State' : 'State', 'FIPS' : 'fips', 'Lat' : 'Latitude', 'Long_' : 'Longitude', 'Confirmed'  :'Confirmed Cases', 'Recovered':'Recoveries'})
        arHold = arHold.fillna(0)
        arHold = arHold.astype({'fips':'int64'})
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if arHold.at[75, 'County'] == 'Arkansas' and len(arHold.columns) == 8:
        
            arHold.to_csv('COVID-19_cases_ardoh.csv',index=False, header=True)
            counter += 1
            print("Arkansas scraper is complete.")
        else:
            print(cl("ERROR: Must fix Arkansas scraper.", 'red'))
    
    except Exception:
        print(cl('Printed or exception raised for AR scraper.', 'green'))
        pass
        
def aSamScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        asWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_States'
        asClient = req(asWiki)
        site_parse = soup(asClient.read(), "lxml")
        asClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "mw-parser-output"}).find_all('tbody')
        
        #CSV file name and header
        csvfile = "COVID-19_cases_asWiki.csv"
        headers = "Region,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
            
        aSam = "AMERICAN SAMOA"
        
        #Uses geocode API that grabs latitude and longitude. According to API's 
        #policy, you must use a sleep function to ensure that you are giving their
        #servers enough time 
        asGeo = liegen.geocode(aSam)
        sleep(1)
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            pull = t.findAll('tr')
            for p in pull:
                take = p.get_text()
                hold.append(take)
                
        amSam = hold[122].split('\n')
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if amSam[3] == "American Samoa":
        
            file = open(csvfile, "w")
            file.write(headers)
            
            file.write(amSam[3] + "," + aSam + "," + fips.get_state_fips(aSam) + "," + str(asGeo.latitude) 
                       + "," + str(asGeo.longitude) + "," + amSam[5].replace(',','') 
                       + "," + amSam[7].replace(',','') + "," 
                       + amSam[9].replace(',','').replace('–','0') + "\n")
            
            file.close()
            
            counter += 1
            print("American Samoa scraper is complete.")
        else:
            print(cl("ERROR: Must fix American Samoa scraper.", 'red'))
    
    except Exception:
        print(cl('Printed or exception raised for AS scraper.', 'green'))
        pass
    
def azScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        azWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Arizona'
        azClient = req(azWiki)
        site_parse = soup(azClient.read(), "lxml")
        azClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        az = "ARIZONA"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_azWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            pull = t.findAll('tr')
            for p in pull:
                take = p.get_text()
                hold.append(take)
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[2].split('\n')[1]) == 'Apache' and (hold[16].split('\n')[1]) == 'Yuma':
        
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[2:17]:
                take = h.split('\n')
                file.write(take[1] + "," + az + "," 
                           + str(fips.get_county_fips(take[1], state = az)).strip() + "," 
                           + str(geocoder.opencage(take[1] + "," + az, key='').latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "," 
                           + take[5].replace(',','').replace('–','0').strip('< ') + "\n")
                    
            file.close()
            
            counter += 1
            print("Arizona scraper is complete.")
        else:
            print(cl("ERROR: Must fix Arizona scraper.", 'red')) 
    
    except Exception:
        print(cl('Printed or exception raised for AZ scraper.', 'green'))
        pass
    
def caScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        caWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_California'
        caClient = req(caWiki)
        site_parse = soup(caClient.read(), 'lxml')
        caClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).find_all('tbody')
        
        ca = "CALIFORNIA"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_caWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            pull = t.findAll('tr')
            for p in pull[2:]:
                take = p.get_text()
                hold.append(take)
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Los Angeles' and (hold[57].split('\n')[1]) == 'Sierra':
    
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[:58]:
                take = h.split('\n')
                file.write(take[1].split('[')[0] + "," + ca + "," + str(fips.get_county_fips(take[1].split('[')[0], state = ca)).strip() 
                + "," + str(geocoder.opencage(take[1].strip('[c]') + "," + ca, key='').latlng).strip('[]')  
                + "," + take[3].replace(',','') + "," + take[5].replace(',','') + "," + take[7].replace('–', '0').replace(',','') + "\n")
                        
            file.close()
            
            counter += 1
            print("California scraper is complete.")
        else:
            print(cl("ERROR: Must fix California scraper.", 'red')) 
            
    except Exception:
        print(cl('Printed or exception raised for CA scraper.', 'green'))
        pass
        
def coScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        codoh = 'https://covid19.colorado.gov/covid-19-data'
        coClient = req(codoh)
        site_parse = soup(coClient.read(), 'lxml')
        coClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        #Broken down into two separate tables because of format from parent site
        table1 = site_parse.findAll("div", {"class": "field field--name-field-card-body field--type-text-long field--label-hidden field--item"})[7]    
        #table2 = site_parse.findAll("div", {"class": "field field--name-field-card-body field--type-text-long field--label-hidden field--item"})[9]
        co = "COLORADO"
        
        #Further parse the information this time looking for the <tr> element.
        #Then put aside two variable to aid in the check later
        test1 = table1.findAll('tr')
        #test2 = table2.findAll('tr')
        adamsTest = test1[1].find('td').text
        outTest = test1[-2].find('td').text
        
        #CSV file name and header
        csvfile = "COVID-19_cases_coDOH.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended          
        if adamsTest == 'Adams' and outTest == 'Out of state':
    
            file = open(csvfile, "w")
            file.write(headers)
            
            for t in test1[1:43]:
                    pull = t.findAll('td')
                    file.write(pull[0].text + "," + co + "," + str(fips.get_county_fips(pull[0].text, state = co)).strip() + ","
                               + str(geocoder.opencage(pull[0].text + "," + co, key='').latlng).strip('[]') 
                               + "," + pull[1].text.replace(',','').strip() 
                               + "," + pull[2].text.replace(',','').strip() + "\n")
            
#            for t in test2[1:13]:
#                    pull = t.findAll('td')
#                    file.write(pull[0].text + "," + co + "," + str(fips.get_county_fips(pull[0].text, state = co)).strip() + ","
#                               + str(geocoder.opencage(pull[0].text + "," + co, key='').latlng).strip('[]') 
#                               + "," + pull[1].text.replace(',','').strip() 
#                               + "," + pull[2].text.replace(',','').strip() + "\n")
                    
            file.write(test1[43].find('td').text.replace('Philips','Phillips') + "," + co + "," 
                       + str(fips.get_county_fips(test1[43].find('td').text.replace('Philips','Phillips'),state=co)).strip() + "," 
                       + str(geocoder.opencage(test1[43].find('td').text.replace('Philips','Phillips') + ", " + co,key='').latlng).strip('[]')
                       + "," + test1[43].findAll('td')[1].text.strip().replace(',','').strip()
                       + "," + test1[43].findAll('td')[2].text.strip().replace(',','').strip() + "\n")
            
            for t in test1[44:-3]:
                    pull = t.findAll('td')
                    file.write(pull[0].text + "," + co + "," + str(fips.get_county_fips(pull[0].text, state = co)).strip() + ","
                               + str(geocoder.opencage(pull[0].text + "," + co, key='').latlng).strip('[]') 
                               + "," + pull[1].text.replace(',','').strip() 
                               + "," + pull[2].text.replace(',','').strip() + "\n")
            
            file.write(test1[-3].find('td').text + "," + co + "," + str(fips.get_state_fips(co)).strip() + "," 
                       + str(liegen.geocode(co).latitude) + "," + str(liegen.geocode(co).longitude) + "," 
                       + test1[-3].findAll('td')[1].text.strip().replace(',','').strip() + "," 
                       + test1[-3].findAll('td')[2].text.strip().replace(',','').strip() + "\n")
            sleep(1)
            file.write(test1[-2].find('td').text + "," + co + "," + str(fips.get_state_fips(co)).strip() + "," 
                       + str(liegen.geocode(co).longitude) + "," + str(liegen.geocode(co).longitude) + "," 
                       + test1[-2].findAll('td')[1].text.strip().replace(',','').strip() + "," 
                       + test1[-2].findAll('td')[2].text.strip().replace(',','').strip() + "\n")
            sleep(1)
            file.close()
            
            counter += 1
            print("Colorado scraper is complete.")
        else:
            print(cl("ERROR: Must fix Colorado scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for CO scraper.', 'green'))
        pass

def ctScrape():
    
    try:
        #Pulling information from a csv from the OpenData Connecticut DOH site
        url = 'https://data.ct.gov/api/views/bfnu-rgqt/rows.csv?accessType=DOWNLOAD'
        ctDOH = pd.read_csv(url)
        #Model the dataframe to get the latest counts and the counties needed
        nazar = ctDOH.sort_values('DateUpdated', ascending = False).head(8)
        #Insert a state column
        nazar.insert(2, 'State', 'CONNECTICUT')
        #Drop away trash columns
        eth = nazar.drop(columns=['Cnty_cod','CaseRates','DateUpdated'])
        #Add fips and geolocation to the table
        namen = eth['County']
        namen = namen.tolist()
        #Append fips and geolocation to appropriate counties
        bea = []
        for n in namen:
            locale = geocoder.opencage(n + ", " + "CONNECTICUT", key= '').latlng
            bea.append(locale)
        #Before adding them to the dataframe, we shall strip them of the brackets
        convert=[]
        for bo in bea:
            con = str(bo)
            convert.append(con.strip('[]'))
        #Split them apart now... How sad...
        lat=[]
        lon=[]
        for c in convert:
            pull=c.split(', ')
            lat.append(pull[0])
            lon.append(pull[1])
        #Insert into the dataframe
        eth.insert(1, 'Latitude', lat)
        eth.insert(2, 'Longitude', lon)
        sophia = []
        for n in namen:
            fipsCT = fips.get_county_fips(n, state = "CONNECTICUT")
            sophia.append(fipsCT)
        eth.insert(3, 'fips', sophia)
        ctTab = eth.rename(columns = {'ConfirmedCases':'Confirmed Cases',
                                      'HospitalizedCases':'Hospitalized'})
        ctCOV = ctTab.reindex(columns=['County','State','fips','Latitude',
                                       'Longitude','Confirmed Cases','Deaths',
                                       'Hospitalized'])
        ctCoV = ctCOV.reset_index().drop(columns = ['index'])
        
        #CSV file name and header
        csvfile = "COVID-19_cases_ctDOH.csv"
        
        #Check to ensure the collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if ctCoV.at[0,'County'] == 'Windham':
                        
            ctCoV.to_csv(csvfile,index=False,header=True)
            
            file.close()
            
            counter += 1
            print("Connecticut scraper is complete.")
        else:
            print(cl("ERROR: Must fix Connecticut scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for CT scraper.', 'green'))
        pass
    
def dcScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        dcWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_States'
        dcClient = req(dcWiki)   
        site_parse = soup(dcClient.read(), "lxml")
        dcClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "mw-parser-output"}).find_all('tbody')
        
        #CSV file name and header
        csvfile = "COVID-19_cases_dcWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
            
        dc = "WASHINGTON DC"
        
        #Uses geocode API that grabs latitude and longitude. According to API's 
        #policy, you must use a sleep function to ensure that you are giving their
        #servers enough time 
        dcGeo = liegen.geocode(dc)
        sleep(1)
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            pull = t.findAll('tr')
            for p in pull:
                take = p.get_text()
                hold.append(take)
    
        capital = hold[129].split('\n')
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if capital[3] == "District of Columbia":
        
            file = open(csvfile, "w")
            file.write(headers)
                
            file.write(capital[3] + "," + dc + "," 
                       + str(fips.get_county_fips("Washington", state= "DC")).strip() + "," + str(dcGeo.latitude) 
                       + "," + str(dcGeo.longitude) + "," + capital[5].replace(',','')
                       + "," + capital[7].replace(',','') + "," 
                       + capital[9].replace(',','') + "\n")
            
            file.close()
            
            counter += 1
            print("DC scraper is complete.")
        else:
            print(cl("ERROR: Must fix DC scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for DC scraper.', 'green'))
        pass
    
def deScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        deWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Delaware'
        deClient = req(deWiki)   
        site_parse = soup(deClient.read(), 'lxml')
        deClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.findAll("div", {"class":"tp-container"})[0]
        pull = tables.findAll('td')
        
        de = "DELAWARE"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_deWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Break the parse into the separate counties with its corresponding values
        #Uses geocode API that grabs latitude and longitude. According to API's 
        #policy, you must use a sleep function to ensure that you are giving their
        #servers enough time 
        kent = tables.findAll('th')[9].text.strip() + " County"
        kentC = pull[0].text.strip().replace(',','')
        kentD = pull[1].text.strip().replace(',','')
        kentR = pull[2].text.strip().replace(',','')
        kLocale = liegen.geocode(kent + "," + de)
        sleep(1)
        newCastle = tables.findAll('th')[10].text.strip() + " County"
        newC = pull[4].text.strip().replace(',','')
        newD = pull[5].text.strip().replace(',','')
        newR = pull[6].text.strip().replace(',','')
        nLocale = liegen.geocode(newCastle + "," + de)
        sleep(1)
        suss = tables.findAll('th')[11].text.strip() + " County"
        sussC = pull[8].text.strip().replace(',','')
        sussD = pull[9].text.strip().replace(',','')
        sussR = pull[10].text.strip().replace(',','')
        sLocale = liegen.geocode(suss + "," + de)
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if kent == 'Kent County' and suss == 'Sussex County':
     
            file = open(csvfile, "w")
            file.write(headers)
            
            file.write(kent + ","+ de + "," + str(fips.get_county_fips(kent, state = de)).strip() + "," 
                       + str(kLocale.latitude) + "," + str(kLocale.longitude) + "," 
                       + kentC + "," + kentD + "," + kentR + "\n")
            file.write(newCastle + ","+ de + "," + str(fips.get_county_fips(newCastle, state = de)).strip() + "," 
                       + str(nLocale.latitude) + "," + str(nLocale.longitude) + "," 
                       + newC + "," + newD + "," + newR + "\n")
            file.write(suss + ","+ de + "," + str(fips.get_county_fips(suss, state = de)).strip() + "," 
                       + str(sLocale.latitude) + "," + str(sLocale.longitude) + "," 
                       + sussC + "," + sussD + "," + sussR + "\n")
            
            file.close()
            
            counter += 1
            print("Delaware scraper is complete.")
        else:
            print(cl("ERROR: Must fix Delaware scraper.", 'red')) 

    except Exception:
        print(cl('Printed or exception raised for DE scraper.', 'green'))
        pass
        
def flScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        flWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Florida'
        flClient = req(flWiki)
        site_parse = soup(flClient.read(), "lxml")
        flClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        #CSV file name and header
        csvfile = "COVID-19_cases_flWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
            
        fl = "FLORIDA"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            pull = t.findAll('tr')
            for p in pull:
                take = p.get_text()
                hold.append(take)
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[2].split('\n')[1]) == 'Alachua' and (hold[68].split('\n')[1]) == 'Washington':
        
            file = open(csvfile, "w")
            file.write(headers)
                
            for h in hold[2:69]:
                take = h.split('\n')
                file.write(take[1] + "," + fl + "," 
                           + str(fips.get_county_fips(take[1], state = fl)).strip() + ","
                           + str(geocoder.opencage(h.split('\n')[1] + "," + fl, key='').latlng).strip('[]') + "," 
                           + take[3].replace(',','').replace('–','0') + "," 
                           + take[5].replace(',','').replace('–','0') + "," 
                           + take[7].replace(',','').replace('–','0') +"\n")
            file.write(hold[69].split('\n')[1] + "," + fl + "," 
                       + str(fips.get_state_fips(fl)).strip() + "," 
                       + str(liegen.geocode(fl).latitude) + "," 
                       + str(liegen.geocode(fl).longitude) + "," 
                       + hold[69].split('\n')[3].replace(',','').replace('–','0') + "," 
                       + hold[69].split('\n')[5].replace(',','').replace('–','0') + "," 
                       + hold[69].split('\n')[7].replace(',','').replace('–','0') +"\n")
            
            file.close()
            
            counter += 1
            print("Florida scraper is complete.")
        else:
            print(cl("ERROR: Must fix Florida scraper.", 'red'))
            
    except Exception:
        print(cl('Printed or exception raised for FL scraper.', 'green'))
        pass

def gaScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        gadoh = 'https://d20s4vd27d0hk0.cloudfront.net/?initialWidth=616&childId=covid19dashdph&parentTitle=COVID-19%20Daily%20Status%20Report%20%7C%20Georgia%20Department%20of%20Public%20Health&parentUrl=https%3A%2F%2Fdph.georgia.gov%2Fcovid-19-daily-status-report'
        gaClient = req(gadoh)
        site_parse = soup(gaClient.read(), 'lxml')
        gaClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"id": "summary"}).findAll('tr')
        
        ga = "GEORGIA"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_gadoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (tables[5].find('td').text) == 'Fulton' and (tables[164].find('td').text) == 'Unknown':
    
            file = open(csvfile, "w")
            file.write(headers)
            
            for t in tables[5:164]:
                    pull = t.findAll('td')
                    file.write(pull[0].text + ","+ ga + "," + str(fips.get_county_fips(pull[0].text, state = ga)).strip() + ","
                               + str(geocoder.opencage(pull[0].text + " County" + "," + ga, key='').latlng).strip('[]')
                               + "," + pull[1].text + "," + pull[2].text + "\n")
            
            file.write(tables[164].find('td').text + ","+ ga + "," + str(fips.get_state_fips(ga)).strip() 
                       + "," + str(liegen.geocode(ga).latitude) + "," 
                       + str(liegen.geocode(ga).longitude) + "," 
                       + tables[164].findAll('td')[1].text.strip() + "," 
                       + tables[164].findAll('td')[2].text.strip() + "\n")
            
            file.close()
            
            counter += 1
            print("Georgia scraper is complete.")
        else:
            print(cl("ERROR: Must fix Georgia scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for GA scraper.', 'green'))
        pass
        
def guScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        guWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_States'
        guClient = req(guWiki)
        site_parse = soup(guClient.read(), "lxml")
        guClient.close()
        
        #Narrow down the parse to the section that is most pertinent
        tables = site_parse.find("div", {"class": "mw-parser-output"}).find_all('tbody')
        
        #CSV file name and header
        csvfile = "COVID-19_cases_gu_mp_Wiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            pull = t.findAll('tr')
            for p in pull:
                take = p.get_text()
                hold.append(take)
    
        gu = "GUAM"
        guam = hold[132].split('\n')
        
        mp = "NORTHERN MARIANA ISLANDS"
        mariana = hold[157].split('\n')
        
        #Uses geocode API that grabs latitude and longitude. According to API's 
        #policy, you must use a sleep function to ensure that you are giving their
        #servers enough time 
        guGeo = liegen.geocode(gu)
        sleep(1)
        mpGeo = liegen.geocode(mp)
        sleep(1)
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if guam[3] == "Guam" and mariana[3] == "Northern Mariana Islands":
        
            file = open(csvfile, "w")
            file.write(headers)
                
            file.write(guam[3] + "," + gu + "," + str(fips.get_county_fips(gu, state=gu)).strip() 
                       + "," + str(guGeo.latitude) + "," + str(guGeo.longitude) + "," 
                       + guam[5].replace(',','').replace('–','0') + "," 
                       + guam[7].replace(',','').replace('–','0') + "," 
                       + guam[9].replace(',','').replace('–','0') + "\n")
        
            file.write(mariana[3] + "," + mp + "," + str(fips.get_county_fips("Rota",state=mp)).strip() 
                       + ","  + str(mpGeo.latitude) + "," + str(mpGeo.longitude) + "," 
                       + mariana[5].replace(',','').replace('–','0') + "," 
                       + mariana[7].replace(',','').replace('–','0') + "," 
                       + mariana[9].replace(',','').replace('\xa0','0').replace('–','0') + "\n")
            
            file.close()
            
            counter += 1
            print("Guam/Northern Mariana scraper is complete.")
        else:
            print(cl("ERROR: Must fix Guam/Northern Mariana scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for GU scraper.', 'green'))
        pass
    
def hiScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        hidoh = 'https://health.hawaii.gov/coronavirusdisease2019/what-you-should-know/current-situation-in-hawaii/'
        hiClient = req(hidoh)
        site_parse = soup(hiClient.read(), "lxml")
        hiClient.close()
        
        #Narrow down the parse to the section that is most pertinent
        tables = site_parse.find("div", {"class": "primary-content secondary"}).findAll("div", {"class": "wp-block-group"})    
    
        hi= "HAWAII"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_hidoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Total Cases,Deaths,Recoveries,Released from Isolation,Hospitalization,Pending\n"
        
        
        #Break the list into the separate counties and corresponding values (including fips and geolocation)
        hawaii = tables[3].find('th').text
        haLocale = str(geocoder.opencage(hawaii + "," + hi, key='').latlng).strip('[]')
        haFIPS = str(fips.get_county_fips(hawaii,state=hi)).strip()
        haTotal = tables[3].findAll('td')[1].text.split(' ')[0].strip('‡')
        haIso = tables[3].findAll('td')[3].text.split(' ')[0].strip('‡')
        haHosp = tables[3].findAll('td')[5].text.split(' ')[0].strip('‡')
        haDeaths = tables[3].findAll('td')[7].text.split(' ')[0].strip('‡')
    
        honolulu = tables[4].find('th').text
        honLocale = str(geocoder.opencage(honolulu + "," + hi, key='').latlng).strip('[]')
        honFIPS = str(fips.get_county_fips(honolulu,state=hi)).strip()
        honTotal = tables[4].findAll('td')[1].text.split(' ')[0].strip('‡')
        honIso = tables[4].findAll('td')[3].text.split(' ')[0].strip('‡')
        honHosp = tables[4].findAll('td')[5].text.split(' ')[0].strip('‡')
        honDeaths = tables[4].findAll('td')[7].text.split(' ')[0].strip('‡')
    
        kauai = tables[5].find('th').text
        kauLocale = str(geocoder.opencage(kauai + "," + hi, key='').latlng).strip('[]')
        kauFIPS = str(fips.get_county_fips(kauai,state=hi)).strip()
        kauTotal = tables[5].findAll('td')[1].text.split(' ')[0].strip('‡')
        kauIso = tables[5].findAll('td')[3].text.split(' ')[0].strip('‡')
        kauHosp = tables[5].findAll('td')[5].text.split(' ')[0].strip('‡')
        kauDeaths = tables[5].findAll('td')[7].text.split(' ')[0].strip('‡')
    
        maui = tables[6].find('th').text
        mauiLocale = str(geocoder.opencage(maui + "," + hi, key='').latlng).strip('[]')
        mauiFIPS = str(fips.get_county_fips(maui,state=hi)).strip()
        mauiTotal = tables[6].findAll('td')[1].text.split(' ')[0].strip('‡')
        mauiIso = tables[6].findAll('td')[3].text.split(' ')[0].strip('‡')
        mauiHosp = tables[6].findAll('td')[5].text.split(' ')[0].strip('‡')
        mauiDeaths = tables[6].findAll('td')[7].text.split(' ')[0].strip('‡')
    
        outliers = site_parse.find("div", {"class": "primary-content secondary"}).findAll("table", {"class": "has-fixed-layout"})
        outHI = outliers[5].findAll('th')[0].text
        outHIno = outliers[5].findAll('th')[1].text.split(' ')[0].strip('‡')
    
        pending = outliers[6].findAll('th')[0].text
        penNo = outliers[6].findAll('th')[1].text.split(' ')[0].strip('‡')
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if hawaii == 'HAWAII COUNTY' and pending == 'County Pending':
    
            file = open(csvfile, "w")
            file.write(headers)
            
            file.write(hawaii + "," + hi + "," + haFIPS + "," + haLocale + "," + haTotal + "," + haDeaths + "," + "" 
                       + "," + haIso + "," + haHosp + "," + penNo + "\n")
            
            file.write(honolulu + "," + hi + "," + honFIPS + "," + honLocale + "," + honTotal + "," + honDeaths + "," + "" 
                       + "," + honIso + "," + honHosp + "," + "" + "\n")
            
            
            file.write(kauai + "," + hi + "," + kauFIPS + "," + kauLocale + "," + kauTotal + "," + kauDeaths + "," + "" 
                       + "," + kauIso + "," + kauHosp + "," + "" + "\n")
            
            file.write(maui + "," + hi + "," + mauiFIPS + "," + mauiLocale + "," + mauiTotal + "," + mauiDeaths + "," + "" 
                       + "," + mauiIso + "," + mauiHosp + "," + "" + "\n")
            
            file.close()
        
            counter += 1
            print("Hawai'i scraper is complete.")
        else:
            print(cl("ERROR: Must fix Hawai'i scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for HI scraper.', 'green'))
        pass

def idScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        idWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Idaho'
        idClient = req(idWiki)
        site_parse = soup(idClient.read(), "lxml")
        idClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        iD = "IDAHO"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_idWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            pull = t.findAll('tr')
            for p in pull[2:]:
                take = p.get_text()
                hold.append(take)
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Ada' and (hold[43].split('\n')[1]) == 'Washington':
    
            file = open(csvfile, "w")
            file.write(headers)
                        
            for h in hold[0:43]:
                take = h.split('\n')
                file.write(take[1] + "," + iD + "," + str(fips.get_county_fips(take[1],state=iD)).strip() + "," 
                           + str(geocoder.opencage(take[1] + ", " + iD, key='').latlng).strip('[]') + "," 
                           + take[3].replace(',','').replace('–','0') + "," 
                           + take[5].replace(',','').replace('–','0') + ","
                           + take[7].replace(',','').replace('–','0') + "\n")        
            file.close()
            
            counter += 1
            print("Idaho scraper is complete.")
        else:
            print(cl("ERROR: Must fix Idaho scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for ID scraper.', 'green'))
        pass
    
def ilScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        ilWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Illinois'
        ilClient = req(ilWiki)
        site_parse = soup(ilClient.read(), "lxml")
        ilClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        il = "ILLINOIS"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_ilWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            pull = t.findAll('tr')
            for p in pull[2:]:
                take = p.get_text()
                hold.append(take)
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Adams' and (hold[96].split('\n')[1]) == 'Woodford':
        
            file = open(csvfile, "w")
            file.write(headers)
                        
            for h in hold[0:15]:
                take = h.split('\n')
                file.write(take[1] + "," + il + "," 
                           + str(fips.get_county_fips(take[1], state=il)).strip() + ","
                           + str(geocoder.opencage(h.split('\n')[1] + co + "," + il, key='').latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "," 
                           + take[5].replace(',','') + "," 
                           + take[7].replace(',','').replace('–','0') + "\n")
            #Cook County has some values that needs fixing... use split to do so
            file.write(hold[15].split('\n')[1] + "," + il + "," 
                       + str(fips.get_county_fips(hold[106].split('\n')[1], il)).strip() + "," 
                       + str(geocoder.opencage(hold[106].split('\n')[1], key='').latlng).strip('[]') + "," 
                       + hold[15].split('\n')[3].replace(',','') + "," 
                       + hold[15].split('\n')[5].replace(',','') + "," 
                       + hold[15].split('\n')[7].replace(',','').split(']')[1].split('[')[0].strip() + "\n")
            
            for h in hold[16:97]:
                take = h.split('\n')
                file.write(take[1] + "," + il + "," 
                           + str(fips.get_county_fips(take[1], state=il)).strip() + ","
                           + str(geocoder.opencage(h.split('\n')[1] + co + "," + il, key='').latlng).strip('[]') + "," 
                           + take[3].replace(',','').replace('–','0') + "," 
                           + take[5].replace(',','').replace('–','0') + "," 
                           + take[7].replace(',','').replace('–','0') + "\n")
    
            file.close()
            
            counter += 1
            print("Illinois scraper is complete.")
        else:
            print(cl("ERROR: Must fix Illinois scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for IL scraper.', 'green'))
        pass

def inScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        inWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Indiana'
        inClient = req(inWiki)
        site_parse = soup(inClient.read(), "lxml")
        inClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        inD = "INDIANA"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_inWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            pull = t.findAll('tr')
            for p in pull[2:]:
                take = p.get_text()
                hold.append(take)
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Adams' and (hold[91].split('\n')[1]) == 'Whitley':
        
            file = open(csvfile, "w")
            file.write(headers)
                
            for h in hold[0:92]:
                take = h.split('\n')
                file.write(take[1] + "," + inD + "," + str(fips.get_county_fips(take[1],state=inD)).strip() + ","
                           + str(geocoder.opencage(take[1] + co + "," + inD, key='').latlng).strip('[]') 
                           + "," + take[3].replace(',','').replace('–','0') 
                           + "," + take[5].replace(',','').replace('–','0') + "\n")        
            file.close()
            
            counter += 1
            print("Indiana scraper is complete.")
        else:
            print(cl("ERROR: Must fix Indiana scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for IN scraper.', 'green'))
        pass
    
def ioScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        ioWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Iowa'
        ioClient = req(ioWiki)
        site_parse = soup(ioClient.read(), "lxml")
        ioClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        io = "IOWA"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_ioWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
          
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
             
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended        
        if (hold[0].split('\n')[1]) == 'Adair' and (hold[-3].split('\n')[1]) == 'Wright':
    
            file = open(csvfile, "w")
            file.write(headers)
        
            for h in hold[0:99]:
                take = h.split('\n')
                file.write(take[1] + "," + io + "," + str(fips.get_county_fips(take[1],state=io)).strip() + "," 
                           + str(geocoder.opencage(take[1] + co + "," + io, key='').latlng).strip('[]') 
                           + "," + take[3].replace(',','').replace('–','0') 
                           + "," + take[5].replace(',','').replace('–','0')
                           + "," + take[7].replace(',','').replace('–','0')+ "\n")
                
            file.close()
            
            counter += 1
            print("Iowa scraper is complete.")
        else:
            print(cl("ERROR: Must fix Iowa Scraper.", 'red'))
            
    except Exception:
        print(cl('Printed or exception raised for IO scraper.', 'green'))
        pass

def kaScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        kaWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Kansas'
        kaClient = req(kaWiki)
        site_parse = soup(kaClient.read(), "lxml")
        kaClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        ka = "KANSAS"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_kaWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Allen' and (hold[-3].split('\n')[1]) == 'Wyandotte':
           
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:-2]:
                take = h.split('\n')
                file.write(take[1] + "," + ka + "," + str(fips.get_county_fips(take[1],state=ka)).strip() + ","
                           + str(geocoder.opencage(take[1] + co + "," + ka, key='').latlng).strip('[]') + "," 
                           + take[3].replace('–','0').replace(',','').split(' (')[0] + "," 
                           + take[5].replace('–','0').replace(',','').split('[')[0] + "," 
                           + take[7].replace('–','0').replace(',','').split('[')[0] + "\n")        
            file.close()
            
            counter += 1
            print("Kansas scraper is complete.")
        else:
            print(cl("ERROR: Must fix Kansas scraper.", 'red'))
            
    except Exception:
        print(cl('Printed or exception raised for KA scraper.', 'green'))
        pass
    
def kyScrape():
    
    try:
        #Grab and hold the information from the json provided
        kyJson = 'https://static01.nyt.com/newsgraphics/2020/03/16/coronavirus-maps/b2d7b66583e8633797d7334e882bb87fd854c828/data/timeseries/USA-21.json'
        kyClient = req(kyJson).read().decode('utf-8')
        kJS = json.loads(kyClient)
        
        #Get the attribute needed
        attr = kJS.get('data')
        
        #Used to help test later
        test = []
        if(attr[1].get('subregion')) == 'Fayette':
            test = True
        else:
            test = False
    
        ky = "KENTUCKY"
    
        #CSV file name and header
        csvfile = "COVID-19_cases_kyNews.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if test == True:
    
            file = open(csvfile, "w")
            file.write(headers)
                
            for a in attr[1:]:
                file.write(a.get('subregion') + "," + ky + "," + str(fips.get_county_fips(a.get('subregion'), state=ky)).strip() + ","
                           + str(geocoder.opencage(a.get('subregion') + ", " + ky, key='').latlng).strip('[]') + "," 
                           + str(a.get('cases')[-1:]).strip('[]') + "," + str(a.get('deaths')[-1:]).strip('[]')  + "\n")
                
            file.close()
            
            counter += 1
            print("Kentucky scraper is complete.")
        else:
            print(cl("ERROR: Must fix Kentucky scraper.", 'red'))
            
    except Exception:
        print(cl('Printed or exception raised for KY scraper.', 'green'))
        pass
    
def laScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        laWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Louisiana'
        laClient = req(laWiki)
        site_parse = soup(laClient.read(), "lxml")
        laClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        la = "LOUISIANA"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_laWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
        
        desoto = hold[15].split('\n')
        des_fips = '22031'
        lasalle = hold[29].split('\n')
        las_fips = '22059'
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended    
        if (hold[0].split('\n')[1]) == 'Acadia' and (hold[-3].split('\n')[1]) == 'Winn':
                
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:15]:
                take = h.split('\n')
                file.write(take[1] + "," + la + "," + str(fips.get_county_fips(take[1],state=la)).strip() + ","
                           + str(geocoder.opencage(take[1] + "," + la, key='').latlng).strip('[]') + "," 
                           + take[3].replace(',','').replace('–','0') + ","
                           + take[5].replace(',','').replace('–','0') + "," 
                           + take[7].replace(',','').replace('–','0') + "\n")
            file.write(desoto[1] + "," + la + "," + des_fips + ","
                           + str(geocoder.opencage(desoto[1] + "," + la, key='').latlng).strip('[]') + "," 
                           + desoto[3].replace(',','').replace('–','0') + ","
                           + desoto[5].replace(',','').replace('–','0') + "," 
                           + desoto[7].replace(',','').replace('–','0') + "\n")
            for h in hold[16:29]:
                take = h.split('\n')
                file.write(take[1] + "," + la + "," + str(fips.get_county_fips(take[1],state=la)).strip() + ","
                           + str(geocoder.opencage(take[1] + "," + la, key='').latlng).strip('[]') + "," 
                           + take[3].replace(',','').replace('–','0') + ","
                           + take[5].replace(',','').replace('–','0') + "," 
                           + take[7].replace(',','').replace('–','0') + "\n")
            file.write(lasalle[1] + "," + la + "," + las_fips + ","
                           + str(geocoder.opencage(lasalle[1] + "," + la, key='').latlng).strip('[]') + "," 
                           + lasalle[3].replace(',','').replace('–','0') + ","
                           + lasalle[5].replace(',','').replace('–','0') + "," 
                           + lasalle[7].replace(',','').replace('–','0') + "\n")
            for h in hold[30:-2]:
                take = h.split('\n')
                file.write(take[1] + "," + la + "," + str(fips.get_county_fips(take[1],state=la)).strip() + ","
                           + str(geocoder.opencage(take[1] + "," + la, key='').latlng).strip('[]') + "," 
                           + take[3].replace(',','').replace('–','0') + ","
                           + take[5].replace(',','').replace('–','0') + "," 
                           + take[7].replace(',','').replace('–','0') + "\n")

            file.close()
            
            counter += 1
            print("Louisiana scraper is complete.")
        else:
            print(cl("ERROR: Must fix Louisiana scraper.", 'red'))
            
    except Exception:
        print(cl('Printed or exception raised for LA scraper.', 'green'))
        pass

def maScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        maNews = 'https://www.livescience.com/massachusetts-coronavirus-updates.html'
        maClient = req(maNews)
        site_parse = soup(maClient.read(), "lxml")
        maClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"itemprop": "articleBody"}).find('ul')
        tags = tables.findAll('li')
        
        ma = "MASSACHUSETTS"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_maNews.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (tags[0].get_text().split(': ')[0]) == 'Middlesex' and (tags[14].get_text().split(': ')[0]) == 'Nantucket':
    
            file = open(csvfile, "w")
            file.write(headers)
            
            for t in range(0,15):
                locale = liegen.geocode(tags[t].get_text().split(': ')[0] + co + "," + ma)
                catch_TimeOut(tags[t].get_text().split(': ')[0] + co + "," + ma)
                file.write(tags[t].get_text().split(': ')[0] + "," + ma + "," + str(fips.get_county_fips(tags[t].get_text().split(': ')[0],state=ma)).strip() 
                           + "," + str(locale.latitude) + "," + str(locale.longitude) + ","
                           + tags[t].get_text().split(': ')[1].replace(',','') + "\n")
                sleep(1)
                    
            file.close()
             
            counter += 1
            print("Massachusetts scraper is complete.")
        else:
            print(cl("ERROR: Must fix Massachusetts scraper.", 'red'))
    except Exception:
        print(cl('Printed or exception raised for MA scraper.', 'green'))
        pass
    
def mdScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        mdWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Maryland'
        mdClient = req(mdWiki)
        site_parse = soup(mdClient.read(), "lxml")
        mdClient.close()
        #This was done in order to add DC into the map 
        dcWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_States'
        dcClient = req(dcWiki)
        site_parseDC = soup(dcClient.read(), "lxml")
        dcClient.close()
        
        #Narrow down the parse to the section that is most pertinent for both sites
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        tablesDC = site_parseDC.find("div", {"class": "mw-parser-output"}).find_all('tbody')
        
        md = "MARYLAND"
        co = ' County'    
        dc = "WASHINGTON DC"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_mdWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
    
        #Uses geocode API that grabs latitude and longitude. According to API's 
        #policy, you must use a sleep function to ensure that you are giving their
        #servers enough time 
        dcGeo = liegen.geocode(dc)
        sleep(1)
        
        #Hold all of the table's information into an easy to dissect list for both 
        #places
        hold = []
        holdDC = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
        for t in tablesDC:
            pull = t.findAll('tr')
            for p in pull:
                take = p.get_text()
                holdDC.append(take)
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Allegany' and (hold[-3].split('\n')[1]) == 'Unknown' and holdDC[129].split('\n')[3] == "District of Columbia":
                    
            file = open(csvfile, "w")
            file.write(headers)
                
            for h in hold[0:-3]:
                take = h.split('\n')
                file.write(take[1] + "," + md + "," + str(fips.get_county_fips(take[1],state=md)).strip() + ","
                           + str(geocoder.opencage(take[1] + co + "," + md, key='').latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "," 
                           + take[5].replace(',','') + "\n")
                
            file.write(hold[-3].split('\n')[1] + "," + md + "," + str(fips.get_state_fips(md)).strip() + "," + str(liegen.geocode(md).latitude) + "," 
                       + str(liegen.geocode(md).longitude) + "," 
                       + hold[-3].split('\n')[3].replace(',','') + "," 
                       + hold[-3].split('\n')[5].replace(',','') + "\n")
            
            file.write(holdDC[129].split('\n')[3] + "," + dc + "," 
                       + str(fips.get_county_fips("Washington", state= "DC")).strip() + "," 
                       + str(dcGeo.latitude) + "," + str(dcGeo.longitude) + "," 
                       + holdDC[129].split('\n')[5].replace(',','')+ "," 
                       + holdDC[129].split('\n')[7].replace(',','') + "\n")
            
            file.close()
            
            counter += 1
            print("Maryland scraper is complete.")
        else:
            print(cl("ERROR: Must fix Maryland scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for MD scraper.', 'green'))
        pass
    
def meScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        meDDS = 'https://www.maine.gov/dhhs/mecdc/infectious-disease/epi/airborne/coronavirus.shtml'
        meClient = req(meDDS)
        site_parse = soup(meClient.read(), "lxml")
        meClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"id": "Accordion1"}).findAll("td")[23:108]
        
        me = "MAINE"
        co = ' County'
           
        #CSV file name and header
        csvfile = "COVID-19_cases_meDDS.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries,,Hospitalizations\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            take = t.get_text()
            hold.append(take)
          
        #Break the list into the separate counties
        #Uses geocode API that grabs latitude and longitude. According to API's 
        #policy, you must use a sleep function to ensure that you are giving their
        #servers enough time 
        andr = hold[0:5]
        anC = andr[0]
        anCC = andr[1].replace('\xa0','')
        anR = andr[2].replace('\xa0','')
        anH = andr[3].replace('\xa0','')
        anD = andr[4].replace('\xa0','')
        anLocale = liegen.geocode(anC + co + "," + me)
        sleep(1)
        aroo = hold[5:10]
        arC = aroo[0]
        arCC = aroo[1].replace('\xa0','')
        arR = aroo[2].replace('\xa0','')
        arH = aroo[3].replace('\xa0','')
        arD = aroo[4].replace('\xa0','')
        arLocale = liegen.geocode(arC + co + "," + me)
        sleep(1)
        cumb = hold[10:15]
        cumbC = cumb[0]
        cumbCC = cumb[1].replace('\xa0','')
        cumbR = cumb[2].replace('\xa0','')
        cumbH = cumb[3].replace('\xa0','')
        cumbD = cumb[4].replace('\xa0','')
        cLocale = liegen.geocode(cumbC + co + "," + me)
        sleep(1)
        frank = hold[15:20]
        frC = frank[0]
        frCC = frank[1].replace('\xa0','')
        frR = frank[2].replace('\xa0','')
        frH = frank[3].replace('\xa0','')
        frD = frank[4].replace('\xa0','')
        fLocale = liegen.geocode(frC + co + "," + me)
        sleep(1)
        hanc = hold[20:25]
        haC = hanc[0]
        haCC = hanc[1].replace('\xa0','')
        haR = hanc[2].replace('\xa0','')
        haH = hanc[3].replace('\xa0','')
        haD = hanc[4].replace('\xa0','')
        hLocale = liegen.geocode(haC + co + "," + me)
        sleep(1)
        kenne = hold[25:30]
        keC = kenne[0]
        keCC = kenne[1].replace('\xa0','')
        keR = kenne[2].replace('\xa0','')
        keH = kenne[3].replace('\xa0','')
        keD = kenne[4].replace('\xa0','')
        keLocale = liegen.geocode(keC + co + "," + me)
        sleep(1)
        knox = hold[30:35]
        knC = knox[0]
        knCC = knox[1].replace('\xa0','')
        knR = knox[2].replace('\xa0','')
        knH = knox[3].replace('\xa0','')
        knD = knox[4].replace('\xa0','')
        knLocale = liegen.geocode(knC + co + "," + me)
        sleep(1)
        linc = hold[35:40]
        linC = linc[0]
        linCC = linc[1].replace('\xa0','')
        linR = linc[2].replace('\xa0','')
        linH = linc[3].replace('\xa0','')
        linD = linc[4].replace('\xa0','')
        lLocale = liegen.geocode(linC + co + "," + me)
        sleep(1)
        ox = hold[40:45]
        oxC = ox[0]
        oxCC = ox[1].replace('\xa0','')
        oxR = ox[2].replace('\xa0','')
        oxH = ox[3].replace('\xa0','')
        oxD = ox[4].replace('\xa0','')
        oxLocale = liegen.geocode(oxC + co + "," + me)
        sleep(1)
        peno = hold[45:50]
        penC = peno[0]
        penCC = peno[1].replace('\xa0','')
        penR = peno[2].replace('\xa0','')
        penH = peno[3].replace('\xa0','')
        penD = peno[4].replace('\xa0','')
        peLocale = liegen.geocode(penC + co + "," + me)
        sleep(1)
        pisca = hold[50:55]
        piC = pisca[0]
        piCC = pisca[1].replace('\xa0','')
        piR = pisca[2].replace('\xa0','')
        piH = pisca[3].replace('\xa0','')
        piD = pisca[4].replace('\xa0','')
        piLocale = liegen.geocode(piC + co + "," + me)
        sleep(1)
        saga = hold[55:60]
        sC = saga[0]
        sCC = saga[1].replace('\xa0','')
        sR = saga[2].replace('\xa0','')
        sH = saga[3].replace('\xa0','')
        sD = saga[4].replace('\xa0','')
        saLocale = liegen.geocode(sC + co + "," + me)
        sleep(1)
        somer = hold[60:65]
        soC = somer[0]
        soCC = somer[1].replace('\xa0','')
        soR = somer[2].replace('\xa0','')
        soH = somer[3].replace('\xa0','')
        soD = somer[4].replace('\xa0','')
        soLocale = liegen.geocode(soC + co + "," + me)
        sleep(1)
        waldo = hold[65:70]
        wdC = waldo[0]
        wdCC = waldo[1].replace('\xa0','')
        wdR = waldo[2].replace('\xa0','')
        wdH = waldo[3].replace('\xa0','')
        wdD = waldo[4].replace('\xa0','')
        wdLocale = liegen.geocode(wdC + co + "," + me)
        sleep(1)
        wash = hold[70:75]
        wsC = wash[0]
        wsCC = wash[1].replace('\xa0','')
        wsR = wash[2].replace('\xa0','')
        wsH = wash[3].replace('\xa0','')
        wsD = wash[4].replace('\xa0','')
        waLocale = liegen.geocode(wsC + co + "," + me)
        sleep(1)
        york = hold[75:80]
        yC = york[0]
        yCC = york[1].replace('\xa0','')
        yR = york[2].replace('\xa0','')
        yH = york[3].replace('\xa0','')
        yD = york[4].replace('\xa0','')
        yoLocale = liegen.geocode(yC + co + "," + me)
        sleep(1)
        unk = hold[80:85]
        uC = unk[0]
        uCC = unk[1].replace('\xa0','')
        uR = unk[2].replace('\xa0','')
        uH = unk[3].replace('\xa0','')
        uD = unk[4].replace('\xa0','')
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if anC == 'Androscoggin' and uC == 'Unknown':
           
            file = open(csvfile, "w")
            file.write(headers)
            
            file.write(anC + "," + me + "," + str(fips.get_county_fips(anC,state=me)).strip() + "," + str(anLocale.latitude) + "," 
                       + str(anLocale.longitude) + "," + anCC + "," + anD + "," + anR + "," + "" + "," + anH +"\n")
            
            file.write(arC + "," + me + "," + str(fips.get_county_fips(arC,state=me)).strip() + "," + str(arLocale.latitude) + "," 
                       + str(arLocale.longitude) + "," + arCC + "," + arD + "," + arR + "," + "" + "," + arH +"\n")
            
            file.write(cumbC + "," + me + "," + str(fips.get_county_fips(cumbC,state=me)).strip() + "," + str(cLocale.latitude) + "," 
                       + str(cLocale.longitude) + "," + cumbCC + "," + cumbD + "," + cumbR + "," + "" + "," + cumbH +"\n")
            
            file.write(frC + "," + me + "," + str(fips.get_county_fips(frC,state=me)).strip() + "," + str(fLocale.latitude) + "," 
                       + str(fLocale.longitude) + "," + frCC + "," + frD + "," + frR + "," + "" + "," + frH +"\n")
            
            file.write(haC + "," + me + "," + str(fips.get_county_fips(haC,state=me)).strip() + "," + str(hLocale.latitude) + "," 
                       + str(hLocale.longitude) + "," + haCC + "," + haD + "," + haR + "," + "" + "," + haH +"\n")
            
            file.write(keC + "," + me + "," + str(fips.get_county_fips(keC,state=me)).strip() + "," + str(keLocale.latitude) + "," 
                       + str(keLocale.longitude) + "," + keCC + "," + keD + "," + keR + "," + "" + "," + keH +"\n")
            
            file.write(knC + "," + me + "," + str(fips.get_county_fips(knC,state=me)).strip() + "," + str(knLocale.latitude) + "," 
                       + str(knLocale.longitude) + "," + knCC + "," + knD + "," + knR + "," + "" + "," + knH +"\n")
            
            file.write(linC + "," + me + "," + str(fips.get_county_fips(linC,state=me)).strip() + "," + str(lLocale.latitude) + "," 
                       + str(lLocale.longitude) + "," + linCC + "," + linD + "," + linR + "," + "" + "," + linH +"\n")
            
            file.write(oxC + "," + me + "," + str(fips.get_county_fips(oxC,state=me)).strip() + "," + str(oxLocale.latitude) + "," 
                       + str(oxLocale.longitude) + "," + oxCC + "," + oxD + "," + oxR + "," + "" + "," + oxH +"\n")
            
            file.write(penC + "," + me + "," + str(fips.get_county_fips(penC,state=me)).strip() + "," + str(peLocale.latitude) + "," 
                       + str(peLocale.longitude) + "," + penCC + "," + penD + "," + penR + "," + "" + "," + penH +"\n")
            
            file.write(piC + "," + me + "," + str(fips.get_county_fips(piC,state=me)).strip() + "," + str(piLocale.latitude) + "," 
                       + str(piLocale.longitude) + "," + piCC + "," + piD + "," + piR + "," + "" + "," + piH +"\n")
            
            file.write(sC + "," + me + "," + str(fips.get_county_fips(sC,state=me)).strip() + "," + str(saLocale.latitude) + "," 
                       + str(saLocale.longitude) + "," + sCC + "," + sD + "," + sR + "," + "" + "," + sH +"\n")
            
            file.write(soC + "," + me + "," + str(fips.get_county_fips(soC,state=me)).strip() + "," + str(soLocale.latitude) + "," 
                       + str(soLocale.longitude) + "," + soCC + "," + soD + "," + soR + "," + "" + "," + soH +"\n")
            
            file.write(wdC + "," + me + "," + str(fips.get_county_fips(wdC,state=me)).strip() + "," + str(wdLocale.latitude) + "," 
                       + str(wdLocale.longitude) + "," + wdCC + "," + wdD + "," + wdR + "," + "" + "," + wdH +"\n")
            
            file.write(wsC + "," + me + "," + str(fips.get_county_fips(wsC,state=me)).strip() + "," + str(waLocale.latitude) + "," 
                       + str(waLocale.longitude) + "," + wsCC + "," + wsD + "," + wsR + "," + "" + "," + wsH +"\n")
        
            file.write(yC + "," + me + "," + str(fips.get_county_fips(yC,state=me)).strip() + "," + str(yoLocale.latitude) + "," 
                       + str(yoLocale.longitude) + "," + yCC + "," + yD + "," + yR + "," + "" + "," + yH +"\n")
            
            file.write(uC + "," + me + "," + str(fips.get_state_fips(me)).strip() + "," + str(liegen.geocode(me).latitude) 
                       + "," + str(liegen.geocode(me).longitude) + "," + uCC + "," + uD + "," + uR + "," + "" + "," + uH +"\n")
            
            file.close()
            
            counter += 1
            print("Maine scraper is complete.")
        else:
            print(cl("ERROR: Must fix Maine scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for ME scraper.', 'green'))
        pass

def miScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        miDOH = 'https://www.michigan.gov/coronavirus/0,9753,7-406-98163_98173---,00.html'
        miClient = req(miDOH)
        site_parse = soup(miClient.read(), "lxml")
        miClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "fullContent"}).find("tbody")
        tags = tables.findAll('tr')
        
        mi = "MICHIGAN"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_midoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (tags[0].find('td').text.strip()) == 'Alcona' and (tags[83].find('td').text.strip()) == 'Out of State':
    
            file = open(csvfile, "w")
            file.write(headers)
                    
            for tag in tags[0:20]:
                pull = tag.findAll('td')
                file.write(pull[0].text + "," + mi + "," 
                           + str(fips.get_county_fips(pull[0].text,state=mi)).strip() + ","
                           + str(geocoder.opencage(pull[0].text + co + "," + mi, key='').latlng).strip('[]') 
                           + "," + pull[1].text.replace('\xa0','0') + "," + pull[2].text.replace('\xa0','0') + "\n")
                
            for tag in tags[21:73]:
                pull = tag.findAll('td')
                file.write(pull[0].text + "," + mi + "," 
                           + str(fips.get_county_fips(pull[0].text,state=mi)).strip() + ","
                           + str(geocoder.opencage(pull[0].text + co + "," + mi, key='').latlng).strip('[]') 
                           + "," + pull[1].text.replace('\xa0','0') + "," + pull[2].text.replace('\xa0','0') + "\n")
            
            #St.Clair
            file.write(tags[73].findAll('td')[0].text + "," + mi + "," + "26147" + ","
                           + str(geocoder.opencage(tags[73].findAll('td')[0].text + co + "," + mi, key='').latlng).strip('[]') + "," 
                           + tags[73].findAll('td')[1].text.replace('\xa0','0') + "," 
                           + tags[73].findAll('td')[1].text.replace('\xa0','0') + "\n")
            #St.Joseph
            file.write(tags[74].findAll('td')[0].text + "," + mi + "," + "26149" + ","
                           + str(geocoder.opencage(tags[74].findAll('td')[0].text + co + "," + mi, key='').latlng).strip('[]') + "," 
                           + tags[74].findAll('td')[1].text.replace('\xa0','0') + "," 
                           + tags[74].findAll('td')[1].text.replace('\xa0','0') + "\n")
            
            for tag in tags[75:78]:
                pull = tag.findAll('td')
                file.write(pull[0].text + "," + mi + "," 
                           + str(fips.get_county_fips(pull[0].text,state=mi)).strip() + ","
                           + str(geocoder.opencage(pull[0].text + co + "," + mi, key='').latlng).strip('[]') 
                           + "," + pull[1].text.replace('\xa0','0') + "," + pull[2].text.replace('\xa0','0') + "\n")
            
            #Detroit City merged into Wayne county data
            file.write(tags[78].findAll('td')[0].text + "," + mi + "," 
                       + str(fips.get_county_fips(tags[78].findAll('td')[0].text,state=mi)).strip() + ","
                       + str(geocoder.opencage(tags[78].findAll('td')[0].text + co + "," + mi, key='').latlng).strip('[]')+ "," 
                       + str((int(tags[20].findAll('td')[1].text)) + (int(tags[78].findAll('td')[1].text))) + ","
                       + str((int(tags[20].findAll('td')[2].text)) + (int(tags[78].findAll('td')[2].text))) + "\n")
            
            file.write(tags[79].findAll('td')[0].text + "," + mi + "," 
                       + str(fips.get_county_fips(tags[79].findAll('td')[0].text,state=mi)).strip() + ","
                       + str(geocoder.opencage(tags[79].findAll('td')[0].text + co + "," + mi, key='').latlng).strip('[]') + "," 
                       + tags[79].findAll('td')[1].text.replace('\xa0','0') + "," 
                       + tags[79].findAll('td')[1].text.replace('\xa0','0') + "\n")
            
            file.write("MI Department of Corrections" + "," + mi + "," 
                       + str(fips.get_state_fips(mi)).strip() + "," 
                       + str(liegen.geocode(mi).latitude) + "," 
                       + str(liegen.geocode(mi).longitude) + "," 
                       + tags[80].findAll('td')[1].text.strip() + "," 
                       + tags[80].findAll('td')[2].text.strip() + "\n")
            sleep(1)
            file.write("Federal Correctional Institute" + "," + mi + "," 
                       + str(fips.get_state_fips(mi)).strip() + "," 
                       + str(liegen.geocode(mi).latitude) + "," 
                       + str(liegen.geocode(mi).longitude) + "," 
                       + tags[81].findAll('td')[1].text.strip() + "," 
                       + tags[81].findAll('td')[2].text.strip() + "\n")
            sleep(1)
            file.write(tags[82].find('td').text.strip() + "," + mi + "," 
                       + str(fips.get_state_fips(mi)).strip() + "," 
                       + str(liegen.geocode(mi).latitude) + "," 
                       + str(liegen.geocode(mi).longitude) + "," 
                       + tags[82].findAll('td')[1].text.strip() + "," 
                       + tags[82].findAll('td')[2].text.strip() + "\n")
            sleep(1)
            file.write(tags[83].find('td').text.strip() + "," + mi + "," 
                       + str(fips.get_state_fips(mi)).strip() + "," 
                       + str(liegen.geocode(mi).latitude) + "," 
                       + str(liegen.geocode(mi).longitude) + "," 
                       + tags[83].findAll('td')[1].text.strip() + "," 
                       + tags[83].findAll('td')[2].text.strip() + "\n")
            
            file.close()
            
            counter += 1
            print("Michigan scraper is complete.")
        else:
            print(cl("ERROR: Must fix Michigan scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for MI scraper.', 'green'))
        pass

def mnScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        mnDOH = 'https://www.health.state.mn.us/diseases/coronavirus/situation.html'
        mnClient = req(mnDOH)
        site_parse = soup(mnClient.read(), "lxml")
        mnClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "clearfix"}).findAll("tbody")[11]
        tags = tables.findAll('td')
        
        mn = "MINNESOTA"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_mndoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for td in tags:
            take = td.get_text()
            hold.append(take)
            
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if hold[0] == 'Aitkin' and hold[249] == 'Yellow Medicine':    
            
            file = open(csvfile, "w")
            file.write(headers)
            
            file.write(hold[0] + "," + mn + "," + str(fips.get_county_fips(hold[0],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[0] + co + "," + mn, key='').latlng).strip('[]') + "," 
                       + hold[1].replace(',','') + "," + hold[2].replace(',','') + "\n")
            #sleep(1)
            file.write(hold[3] + "," + mn + "," + str(fips.get_county_fips(hold[3],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[3] + co + "," + mn, key='').latlng).strip('[]') + "," 
                       + hold[4].replace(',','') + "," + hold[5].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[6] + "," + mn + "," + str(fips.get_county_fips(hold[6],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[6] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[7].replace(',','') 
                       + "," + hold[8].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[9] + "," + mn + "," + str(fips.get_county_fips(hold[9],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[9] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[10].replace(',','') 
                       + "," + hold[11].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[12] + "," + mn + "," + str(fips.get_county_fips(hold[12],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[12] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[13].replace(',','') 
                       + "," + hold[14].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[15] + "," + mn + "," + str(fips.get_county_fips(hold[15],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[15] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[16].replace(',','') 
                       + "," + hold[17].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[18] + "," + mn + "," + str(fips.get_county_fips(hold[18],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[18] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[19].replace(',','') 
                       + "," + hold[20].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[21] + "," + mn + "," + str(fips.get_county_fips(hold[21],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[21] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[22].replace(',','') 
                       + "," + hold[23].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[24] + "," + mn + ","  + str(fips.get_county_fips(hold[24],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[24] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[25].replace(',','') 
                       + "," + hold[26].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[27] + "," + mn + "," + str(fips.get_county_fips(hold[27],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[27] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[28].replace(',','') 
                       + "," + hold[29].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[30] + "," + mn + "," + str(fips.get_county_fips(hold[30],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[30] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[31].replace(',','') 
                       + "," + hold[32].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[33] + "," + mn + "," + str(fips.get_county_fips(hold[33],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[33] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[34].replace(',','') 
                       + "," + hold[35].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[36] + "," + mn + ","  + str(fips.get_county_fips(hold[36],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[36] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[37].replace(',','') 
                       + "," + hold[38].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[39] + "," + mn + "," + str(fips.get_county_fips(hold[39],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[39] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[40].replace(',','') 
                       + "," + hold[41].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[42] + "," + mn + "," + str(fips.get_county_fips(hold[42],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[42] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[43].replace(',','') 
                       + "," + hold[44].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[45] + "," + mn + ","  + str(fips.get_county_fips(hold[45],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[45] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[46].replace(',','') 
                       + "," + hold[47].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[48] + "," + mn + "," + str(fips.get_county_fips(hold[48],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[48] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[49].replace(',','') 
                       + "," + hold[50].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[51] + "," + mn + "," + str(fips.get_county_fips(hold[51],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[51] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[52].replace(',','') 
                       + "," + hold[53].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[54] + "," + mn + ","  + str(fips.get_county_fips(hold[54],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[54] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[55].replace(',','') 
                       + "," + hold[56].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[57] + "," + mn + ","  + str(fips.get_county_fips(hold[57],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[57] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[58].replace(',','') 
                       + "," + hold[59].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[60] + "," + mn + "," + str(fips.get_county_fips(hold[60],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[60] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[61].replace(',','') 
                       + "," + hold[62].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[63] + "," + mn + "," + str(fips.get_county_fips(hold[63],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[63] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[64].replace(',','') 
                       + "," + hold[65].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[66] + "," + mn + "," + str(fips.get_county_fips(hold[66],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[66] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[67].replace(',','') 
                       + "," + hold[68] +"\n")
            #sleep(1)
            file.write(hold[69] + "," + mn + ","  + str(fips.get_county_fips(hold[69],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[69] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[70].replace(',','') 
                       + "," + hold[71].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[72] + "," + mn + "," + str(fips.get_county_fips(hold[72],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[72] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[73].replace(',','') 
                       + "," + hold[74].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[75] + "," + mn + ","  + str(fips.get_county_fips(hold[75],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[75] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[76].replace(',','') 
                       + "," + hold[77].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[78] + "," + mn + "," + str(fips.get_county_fips(hold[78],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[78] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[79].replace(',','') 
                       + "," + hold[80].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[81] + "," + mn + ","  + str(fips.get_county_fips(hold[81],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[81] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[82].replace(',','') 
                       + "," + hold[83].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[84] + "," + mn + "," + str(fips.get_county_fips(hold[84],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[84] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[85].replace(',','') 
                       + "," + hold[86].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[87] + "," + mn + "," + str(fips.get_county_fips(hold[87],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[87] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[88].replace(',','') 
                       + "," + hold[89].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[90] + "," + mn + "," + str(fips.get_county_fips(hold[90],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[90] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[91].replace(',','') 
                       + "," + hold[92].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[93] + "," + mn + "," + str(fips.get_county_fips(hold[93],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[93] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[94].replace(',','') 
                       + "," + hold[95].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[96] + "," + mn + ","  + str(fips.get_county_fips(hold[96],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[96] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[97].replace(',','') 
                       + "," + hold[98].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[99] + "," + mn + "," + str(fips.get_county_fips(hold[99],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[99] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[100].replace(',','') 
                       + "," + hold[101].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[102] + "," + mn + "," + str(fips.get_county_fips(hold[102],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[102] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[103].replace(',','') 
                       + "," + hold[104].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[105] + "," + mn + "," + str(fips.get_county_fips(hold[105],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[105] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[106].replace(',','') 
                       + "," + hold[107].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[108] + "," + mn + "," + str(fips.get_county_fips(hold[108],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[108] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[109].replace(',','') 
                       + "," + hold[110].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[111] + "," + mn + ","  + str(fips.get_county_fips(hold[111],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[111] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[112].replace(',','') 
                       + "," + hold[113].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[114] + "," + mn + ","  + str(fips.get_county_fips(hold[114],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[114] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[115].replace(',','') 
                       + "," + hold[116].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[117] + "," + mn + ","  + str(fips.get_county_fips(hold[117],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[117] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[118].replace(',','') 
                       + "," + hold[119].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[120] + "," + mn + "," + str(fips.get_county_fips(hold[120],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[120] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[121].replace(',','') 
                       + "," + hold[122].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[123] + "," + mn + "," + str(fips.get_county_fips(hold[123],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[123] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[124].replace(',','') 
                       + "," + hold[125].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[126] + "," + mn + ","  + str(fips.get_county_fips(hold[126],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[126] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[127].replace(',','') 
                       + "," + hold[128].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[129] + "," + mn + "," + str(fips.get_county_fips(hold[129],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[129] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[130].replace(',','') 
                       + "," + hold[131].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[132] + "," + mn + ","  + str(fips.get_county_fips(hold[132],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[132] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[133].replace(',','') 
                       + "," + hold[134].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[135] + "," + mn + "," + str(fips.get_county_fips(hold[135],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[135] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[136].replace(',','') 
                       + "," + hold[137].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[138] + "," + mn + ","  + str(fips.get_county_fips(hold[138],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[138] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[139].replace(',','') 
                       + "," + hold[140].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[141] + "," + mn + ","  + str(fips.get_county_fips(hold[141],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[141] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[142].replace(',','') 
                       + "," + hold[143].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[144] + "," + mn + ","  + str(fips.get_county_fips(hold[144],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[144] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[145].replace(',','') 
                       + "," + hold[146].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[147] + "," + mn + ","  + str(fips.get_county_fips(hold[147],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[147] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[148].replace(',','') 
                       + "," + hold[149].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[150] + "," + mn + ","  + str(fips.get_county_fips(hold[150],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[150] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[151].replace(',','') 
                       + "," + hold[152].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[153] + "," + mn + ","  + str(fips.get_county_fips(hold[153],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[153] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[154].replace(',','') 
                       + "," + hold[155].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[156] + "," + mn + "," + str(fips.get_county_fips(hold[156],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[156] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[157].replace(',','') 
                       + "," + hold[158].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[159] + "," + mn + ","  + str(fips.get_county_fips(hold[159],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[159] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[160].replace(',','') 
                       + "," + hold[161].replace(',','') +"\n")
            #sleep(1)
            file.write(hold[162] + "," + mn + ","  + str(fips.get_county_fips(hold[162],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[162] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[163].replace(',','') 
                       + "," + hold[164].replace(',','') +"\n")
            file.write(hold[165] + "," + mn + ","  + str(fips.get_county_fips(hold[165],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[165] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[166].replace(',','') 
                       + "," + hold[167].replace(',','') +"\n")
            file.write(hold[168] + "," + mn + "," + str(fips.get_county_fips(hold[168],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[168] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[169].replace(',','') 
                       + "," + hold[170].replace(',','') +"\n")
            file.write(hold[171] + "," + mn + "," + str(fips.get_county_fips(hold[171],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[171] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[172].replace(',','') 
                       + "," + hold[173].replace(',','') +"\n")
            file.write(hold[174] + "," + mn + "," + str(fips.get_county_fips(hold[174],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[174] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[175].replace(',','') 
                       + "," + hold[176].replace(',','') +"\n")
            file.write(hold[177] + "," + mn + "," + str(fips.get_county_fips(hold[177],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[177] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[178].replace(',','') 
                       + "," + hold[179].replace(',','') +"\n")
            file.write(hold[180] + "," + mn + "," + str(fips.get_county_fips(hold[180],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[180] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[181].replace(',','') 
                       + "," + hold[182].replace(',','') +"\n")
            file.write(hold[183] + "," + mn + ","  + str(fips.get_county_fips(hold[183],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[183] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[184].replace(',','') 
                       + "," + hold[185].replace(',','') +"\n")
            file.write(hold[186] + "," + mn + ","  + str(fips.get_county_fips(hold[186],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[186] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[187].replace(',','') 
                       + "," + hold[188].replace(',','') +"\n")
            file.write(hold[189] + "," + mn + "," + str(fips.get_county_fips(hold[189],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[189] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[190].replace(',','') 
                       + "," + hold[191].replace(',','') +"\n")
            file.write(hold[192] + "," + mn + ","  + str(fips.get_county_fips(hold[192],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[192] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[193].replace(',','') 
                       + "," + hold[194].replace(',','') +"\n")
            file.write(hold[195] + "," + mn + ","  + str(fips.get_county_fips(hold[195],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[195] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[196].replace(',','') 
                       + "," + hold[197].replace(',','') +"\n")
            file.write(hold[198] + "," + mn + ","  + str(fips.get_county_fips(hold[198],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[198] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[199].replace(',','') 
                       + "," + hold[200].replace(',','') +"\n")
            file.write(hold[201] + "," + mn + ","  + str(fips.get_county_fips(hold[201],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[201] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[202].replace(',','') 
                       + "," + hold[203].replace(',','') +"\n")
            file.write(hold[204] + "," + mn + ","  + str(fips.get_county_fips(hold[204],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[204] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[205].replace(',','') 
                       + "," + hold[206].replace(',','') +"\n")
            file.write(hold[207] + "," + mn + ","  + str(fips.get_county_fips(hold[207],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[207] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[208].replace(',','') 
                       + "," + hold[209].replace(',','') +"\n")
            file.write(hold[210] + "," + mn + ","  + str(fips.get_county_fips(hold[210],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[210] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[211].replace(',','') 
                       + "," + hold[212].replace(',','') +"\n")
            file.write(hold[213] + "," + mn + ","  + str(fips.get_county_fips(hold[213],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[213] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[214].replace(',','') 
                       + "," + hold[215].replace(',','') +"\n")
            file.write(hold[216] + "," + mn + ","  + str(fips.get_county_fips(hold[216],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[216] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[217].replace(',','') 
                       + "," + hold[218].replace(',','') +"\n")
            file.write(hold[219] + "," + mn + ","  + str(fips.get_county_fips(hold[219],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[219] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[220].replace(',','') 
                       + "," + hold[221].replace(',','') +"\n")
            file.write(hold[222] + "," + mn + ","  + str(fips.get_county_fips(hold[222],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[222] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[223].replace(',','') 
                       + "," + hold[224].replace(',','') +"\n")
            file.write(hold[225] + "," + mn + ","  + str(fips.get_county_fips(hold[225],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[225] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[226].replace(',','') 
                       + "," + hold[227].replace(',','') +"\n")
            file.write(hold[228] + "," + mn + ","  + str(fips.get_county_fips(hold[228],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[228] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[229].replace(',','') 
                       + "," + hold[230].replace(',','') +"\n")
            file.write(hold[231] + "," + mn + ","  + str(fips.get_county_fips(hold[231],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[231] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[232].replace(',','') 
                       + "," + hold[233].replace(',','') +"\n")
            file.write(hold[234] + "," + mn + ","  + str(fips.get_county_fips(hold[234],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[234] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[235].replace(',','') 
                       + "," + hold[236].replace(',','') +"\n")
            file.write(hold[237] + "," + mn + ","  + str(fips.get_county_fips(hold[237],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[237] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[238].replace(',','') 
                       + "," + hold[239].replace(',','') +"\n")
            file.write(hold[240] + "," + mn + ","  + str(fips.get_county_fips(hold[240],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[240] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[241].replace(',','') 
                       + "," + hold[242].replace(',','') +"\n")
            file.write(hold[243] + "," + mn + ","  + str(fips.get_county_fips(hold[243],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[243] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[244].replace(',','') 
                       + "," + hold[245].replace(',','') +"\n")
            file.write(hold[246] + "," + mn + ","  + str(fips.get_county_fips(hold[246],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[246] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[247].replace(',','') 
                       + "," + hold[248].replace(',','') +"\n")
            file.write(hold[249] + "," + mn + ","  + str(fips.get_county_fips(hold[249],state=mn)).strip() + ","
                       + str(geocoder.opencage(hold[249] + co + "," + mn, key='').latlng).strip('[]') + "," + hold[250].replace(',','') 
                       + "," + hold[251].replace(',','') +"\n")
            
            file.close()
            
            counter += 1
            print("Minnesota scraper is complete.")
        else:
            print(cl("ERROR: Must fix Minnesota scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for MN scraper.', 'green'))
        pass
    
def moScrape():
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        moDOH = 'https://health.mo.gov/living/healthcondiseases/communicable/novel-coronavirus/results.php'
        moClient = req(moDOH)
        site_parse = soup(moClient.read(), "lxml")
        moClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "panel-group"}).findAll('tr')
    
        mo = "MISSOURI"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_modoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (tables[1].find('td').text) == 'Adair' and (tables[170].find('td').text) == 'TBD':
        
            file = open(csvfile, "w")
            file.write(headers)
            
            #Pull from the county case table
            for t in tables[1:118]:
                pull = t.findAll('td')
                locale = geocoder.opencage(pull[0].text + co + "," + mo, key='')
                file.write(pull[0].text + "," + mo + "," + str(fips.get_county_fips(pull[0].text, state=mo)).strip() + "," + str(locale.latlng).strip('[]')
                            + "," + pull[1].text + "," + "" + "\n")
                
            file.write(tables[118].findAll('td')[0].text + "," + mo + "," + str(fips.get_state_fips(mo)).strip() + "," + str(geocoder.opencage(mo, key='').latlng).strip('[]')
                       + "," + tables[118].findAll('td')[1].text + "," + "" + "\n")
            
            #Pull from the county death table
            for t in tables[138:170]:
                pull = t.findAll('td')
                locale = geocoder.opencage(pull[0].text + co + "," + mo, key='')
                file.write(pull[0].text + "," + mo + "," + str(fips.get_county_fips(pull[0].text,state=mo)).strip() + "," + str(locale.latlng).strip('[]')
                           + "," + "" + "," + pull[1].text + "\n")
                
    #        file.write(tables[164].findAll('td')[0].text + "," + mo + "," + str(fips.get_state_fips(mo)).strip() + "," + str(geocoder.opencage(mo, key='').latlng).strip('[]')
    #                   + "," + "" + "," + tables[164].findAll('td')[1].text + "\n")
            
            file.close()
            
            counter += 1
            print("Missouri scraper is complete.")
        else:
            print(cl("ERROR: Must fix Missouri scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for MO scraper.', 'green'))
        pass
    
def mpScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        mpWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_the_United_States'
        mpClient = req(mpWiki)
        site_parse = soup(mpClient.read(), "lxml")
        mpClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "mw-parser-output"}).find_all('tbody')
        
        #CSV file name and header
        csvfile = "COVID-19_cases_mpWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
            
        mp = "NORTHERN MARIANA ISLANDS"
        
        #Uses geocode API that grabs latitude and longitude. According to API's 
        #policy, you must use a sleep function to ensure that you are giving their
        #servers enough time 
        mpGeo = liegen.geocode(mp)
        sleep(1)
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull:
                    take = p.get_text()
                    hold.append(take)
    
        nmp = hold[157].split('\n')
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if nmp[3] == "Northern Mariana Islands":
    
            file = open(csvfile, "w")
            file.write(headers)
            
            file.write(nmp[3] + "," + mp + "," + str(fips.get_county_fips("Rota",state=mp)).strip() + ","  + str(mpGeo.latitude) 
                       + "," + str(mpGeo.longitude) + "," + nmp[5].replace(',','') 
                       + "," + nmp[7].replace(',','') + "," 
                       + nmp[9].replace(',','') + "\n")
            
            file.close()
            
            counter += 1
            print("Northern Mariana Islands scraper is complete.")
        else:
            print(cl("ERROR: Must fix Northern Mariana Islands scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for MP scraper.', 'green'))
        pass
    
def msScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        msDOH = 'https://msdh.ms.gov/msdhsite/_static/14,0,420.html'
        msClient = req(msDOH)
        site_parse = soup(msClient.read(), "lxml")
        msClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("table", {"id": "msdhTotalCovid-19Cases"}).find("tbody").findAll('tr')
        
        ms = "MISSISSIPPI"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_msdoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (tables[0].find('td').text) == 'Adams' and (tables[80].find('td').text) == 'Yazoo':
        
            file = open(csvfile, "w")
            file.write(headers)
            
            for t in tables[:81]:
                pull = t.findAll('td')
                locale = geocoder.opencage(pull[0].text + co + "," + ms, key='')
                file.write(pull[0].text + "," + ms + "," + str(fips.get_county_fips(pull[0].text, state=ms)).strip() + "," + str(locale.latlng).strip('[]') + "," 
                           + pull[1].text.replace(' ','0') + "," + pull[2].text.replace(' ','0') + "\n")
            
            file.close()
            
            counter += 1
            print("Mississippi scraper is complete.")
        else:
            print(cl("ERROR: Must fix Mississippi scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for MS scraper.', 'green'))
        pass
    
def mtScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        mtDOH = 'https://dphhs.mt.gov/publichealth/cdepi/diseases/coronavirusmt/demographics'
        mtClient = req(mtDOH)
        site_parse = soup(mtClient.read(), "lxml")
        mtClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"id": "dnn_ctr93751_HtmlModule_lblContent"}).findAll("table")[1].find("tbody")
        tags = tables.findAll("tr")
        
        mt = "MONTANA"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_mtdoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if tags[0].find('td').text == 'Beaverhead' and tags[30].find('td').text == 'Total':
        
            file = open(csvfile, "w")
            file.write(headers)
            
            for t in tags[:30]:
                pull = t.findAll("td")
                locale = geocoder.opencage(pull[0].text + co + "," + mt, key='')
                file.write(pull[0].text + "," + mt + "," 
                           + str(fips.get_county_fips(pull[0].text, state=mt)).strip() 
                           + "," + str(locale.latlng).strip('[]') + "," 
                           + pull[1].text + "," + pull[2].text.strip() + "\n")
                
            file.close()
            
            counter += 1
            print("Montana scraper is complete.")
        else:
            print(cl("ERROR: Must fix Montana scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for MT scraper.', 'green'))
        pass
    
def ncScrape():
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        ncDOH = 'https://www.ncdhhs.gov/covid-19-case-count-nc#nc-counties-with-cases'
        ncClient = req(ncDOH)
        site_parse = soup(ncClient.read(), 'lxml')
        ncClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.findAll("tbody")[3]
        tags = tables.findAll('tr')
        
        nc = "NORTH CAROLINA"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_ncdoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (tags[0].find('td').text.strip('\n')) == 'Alamance County' and (tags[97].find('td').text.strip('\n')) == 'Yadkin County':
        
            file = open(csvfile, "w")
            file.write(headers)
            
            for tag in tags:
                pull = tag.findAll('td')
                locale = geocoder.opencage(pull[0].text.strip('\n') + "," + nc, key='')
                file.write(pull[0].text.strip('\n') + "," + nc + "," 
                           + str(fips.get_county_fips(pull[0].text.strip('\n'), state = nc)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + pull[1].text.replace(',','').strip('\n') + "," 
                           + pull[2].text.replace(',','').strip('\n') + "\n")
            
            file.close()
        
            counter += 1
            print("North Carolina scraper is complete.")
        else:
            print(cl("ERROR: Must fix North Carolina scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for NC scraper.', 'green'))
        pass
    
def ndScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        ndWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_North_Dakota'
        ndClient = req(ndWiki)
        site_parse = soup(ndClient.read(), "lxml")
        ndClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
    
        nd = "NORTH DAKOTA"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_ndWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if hold[0].split('\n')[1] == 'Adams' and hold[-3].split('\n')[1] == 'Williams':
    
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:-2]:
                locale = geocoder.opencage(h.split('\n')[1] + co + "," + nd, key='')
                take = h.split('\n')
                file.write(take[1] + "," + nd + "," 
                           + str(fips.get_county_fips(take[1],state=nd)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','').replace('–','0') + ","
                           + take[5].replace(',','').replace('–','0') + ","
                           + take[7].replace(',','').replace('–','0') + "\n")
            
            file.close()
            
            counter += 1
            print("North Dakota scraper is complete.")
        else:
            print(cl("ERROR: Must fix North Dakota Scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for ND scraper.', 'green'))
        pass
    
def neScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        neWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Nebraska'
        neClient = req(neWiki)
        site_parse = soup(neClient.read(), "lxml")
        neClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        ne = "NEBRASKA"
        co = ' County'
    
        #CSV file name and header
        csvfile = "COVID-19_cases_neWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
    
        #Hold all of the table's information into an easy to dissect list
        hold = []    
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Adams' and (hold[-3].split('\n')[1]) == 'York':
                                
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:-2]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + co + "," + ne, key='')
                file.write(take[1] + "," + ne + "," 
                           + str(fips.get_county_fips(take[1],state=ne)).strip() 
                           + "," + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','').replace('–','0') + "," 
                           + take[5].replace(',','').replace('–','0') + "\n")
            
#            file.write(hold[130].split('\n')[1] + "," + ne + "," 
#                       + str(fips.get_state_fips(ne)).strip() 
#                       + "," + str(liegen.geocode(ne).latitude)
#                       + "," + str(liegen.geocode(ne).longitude) + "," 
#                       + hold[130].split('\n')[3] + "," 
#                       + hold[130].split('\n')[5] + "\n")
            
            file.close()
            
            counter += 1
            print("Nebraska scraper is complete.")
        else:
            print(cl("ERROR: Must fix Nebraska scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for NE scraper.', 'green'))
        pass
        
def nhScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        nhNews = 'https://www.livescience.com/new-hampshire-coronavirus-updates.html'
        nhClient = req(nhNews)
        site_parse = soup(nhClient.read(), "lxml")
        nhClient.close()
        
        #Narrow down the parse to the section that is most pertinent
        tables = site_parse.find("article", {"class":"news-article"}).find("div", {"itemprop": "articleBody"}).find('ul')
        tags = tables.findAll('li')
        
        nh = "NEW HAMPSHIRE"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_nhNews.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (tags[0].get_text().split(' ')[0]) == 'Belknap' and (tags[11].get_text().split(' ')[0]) == 'Sullivan':
    
            file = open(csvfile, "w")
            file.write(headers)
                
            for t in range(0,5):
                locale = liegen.geocode(tags[t].get_text().split(' ')[0] + "," + nh)
                catch_TimeOut(tags[t].get_text().split(' ')[0])
                file.write(tags[t].get_text().split(' ')[0] + "," + nh + "," 
                           + str(fips.get_county_fips(tags[t].get_text().split(' ')[0],state=nh)).strip() + "," + str(locale.latitude) 
                           + "," + str(locale.longitude) + "," + tags[t].get_text().split(' ')[1] + "\n")
                sleep(1)
            localeH = liegen.geocode("Hillsborough, New Hampshire")
            file.write("Hillsborough" + "," + nh + "," 
                           + str(fips.get_county_fips("Hillsborough",state=nh)).strip() + "," + str(localeH.latitude) 
                           + "," + str(localeH.longitude) + "," 
                           + str(int(tags[5].get_text().split(' – ')[1].split(' ')[1]) 
                           + int(tags[6].get_text().split(' – ')[1].split(' ')[1]) 
                           + int(tags[7].get_text().split(' – ')[1].split(' ')[1])) + "\n")
            for t in range(8,len(tags)):
                locale = liegen.geocode(tags[t].get_text().split(' ')[0] + "," + nh)
                catch_TimeOut(tags[t].get_text().split(' ')[0])
                file.write(tags[t].get_text().split(' ')[0] + "," + nh + "," 
                           + str(fips.get_county_fips(tags[t].get_text().split(' ')[0],state=nh)).strip() + "," + str(locale.latitude) 
                           + "," + str(locale.longitude) + "," + tags[t].get_text().split(' ')[1] + "\n")
                sleep(1)
            
                
            file.close()
             
            counter += 1
            print("New Hampshire scraper is complete.")
        else:
            print(cl("ERROR: Must fix New Hampshire scraper.", 'red'))
    
    except Exception:
        print(cl('Printed or exception raised for NH scraper.', 'green'))
        pass
    
def njScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        njWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_New_Jersey'
        njClient = req(njWiki)
        site_parse = soup(njClient.read(), "lxml")
        njClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        nj = "NEW JERSEY"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_njWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
         
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended       
        if (hold[0].split('\n')[1]) == 'Atlantic' and (hold[-3].split('\n')[1]) == 'Unassigned':
                
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:-3]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + co + "," + nj, key='')
                file.write(take[1] + "," + nj + "," + str(fips.get_county_fips(take[1], state=nj)).strip() + "," + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','').replace('–','0') + "," 
                           + take[5].replace(',','').replace('–','0') + "," 
                           + take[7].replace(',','').replace('–','0') + "\n")
            
#            file.write(hold[101].split('\n')[1] + "," + nj + "," + str(fips.get_state_fips(nj)).strip() + "," + str(liegen.geocode(nj).latitude) + "," 
#                       + str(liegen.geocode(nj).longitude) + "," 
#                       + hold[101].split('\n')[3].replace(',','') + "," 
#                       + hold[101].split('\n')[5].replace(',','') + "," 
#                       + hold[101].split('\n')[7].replace(',','') + "\n")
            
            file.close()
            
            counter += 1
            print("New Jersey scraper is complete.")
        else:
            print(cl("ERROR: Must fix New Jersey scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for NJ scraper.', 'green'))
        pass
    
def nmScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        nmWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_New_Mexico'
        nmClient = req(nmWiki)
        site_parse = soup(nmClient.read(), "lxml")
        nmClient.close()
        
        #Narrow down the parse to the section that is most pertinent
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        nm = "NEW MEXICO"
    
        #Hold all of the table's information into an easy to dissect list
        hold = []    
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)    
        
        #CSV file name and header
        csvfile = "COVID-19_cases_nmWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Bernalillo' and (hold[-3].split('\n')[1]) == 'Valencia':
    
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:7]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + nm, key='')
                file.write(take[1] + "," + nm + "," + str(fips.get_county_fips(take[1],state=nm)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "," 
                           + take[5].replace(',','') + "\n")
                
            file.write("Dona Ana" + "," + nm + "," + "35013" 
                       + "," + str(geocoder.opencage("Dona Ana County" + ", " + nm, key='').latlng).strip('[]') + "," 
                       + hold[7].split('\n')[3].replace(',','') + "," 
                       + hold[7].split('\n')[5].replace(',','') + "\n")
            
            for h in hold[8:-2]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + nm, key='')
                file.write(take[1] + "," + nm + "," + str(fips.get_county_fips(take[1],state=nm)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "," 
                           + take[5].replace(',','') + "\n")
            
            file.close()
            
            counter += 1
            print("New Mexico scraper is complete.")
        else:
            print(cl("ERROR: Must fix New Mexico scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for NM scraper.', 'green'))
        pass
def nvScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        nvNews = 'https://www.livescience.com/nevada-coronavirus-updates.html'
        nvClient = req(nvNews)
        site_parse = soup(nvClient.read(), "lxml")
        nvClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"itemprop": "articleBody"}).find('ul')
        tags = tables.findAll('li')
        
        nv = "NEVADA"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_nvNews.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (tags[0].get_text().split(' ')[1].strip()) == 'Clark':
    
            file = open(csvfile, "w")
            file.write(headers)
            
            for t in range(0,(len(tags)-1)):
                locale = liegen.geocode(tags[t].get_text().split(' ')[1].strip() + co + "," + nv)
                catch_TimeOut(tags[t].get_text().split(' ')[1].strip() + co + "," + nv)
                file.write(tags[t].get_text().split(' ')[1].strip() + "," + nv + "," 
                           + str(fips.get_county_fips(tags[t].get_text().split(' ')[1].strip(),state=nv)).strip() + "," 
                           + str(locale.latitude) + "," + str(locale.longitude) + ","
                           + tags[t].get_text().split(' ')[0].strip().replace(',','') + "\n")
                sleep(1)
            file.write("White Pine" + "," + nv + "," 
                       + str(fips.get_county_fips("White Pine",state=nv)).strip() + "," 
                       + str(liegen.geocode("White Pine" + co + ", " + nv).latitude) + "," 
                       + str(liegen.geocode("White Pine" + co + ", " + nv).longitude) + ","
                       + tags[-1].get_text().split(' ')[0].strip().replace(',','') + "\n")
            
            file.close()
             
            counter += 1
            print("Nevada scraper is complete.")
        else:
            print(cl("ERROR: Must fix Nevada scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for NV scraper.', 'green'))
        pass

def nyScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        nyWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_New_York_(state)'
        nyClient = req(nyWiki)
        site_parse = soup(nyClient.read(), "lxml")
        nyClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        ny = "NEW YORK"
        co = ' County'
        
        #Pull dataset from github repo that documents the numbers pertaining to NYC boroughs
        nycDF = pd.read_csv('https://raw.githubusercontent.com/nychealth/coronavirus-data/master/boro.csv')
        nycDF.head()
        nycBo = nycDF['BOROUGH_GROUP'].tolist()
        nycCase = nycDF['COVID_CASE_COUNT'].tolist()
        brnx = nycBo[0].strip('The ')
        brnxNo = nycCase[0]
        brook = nycBo[1]
        brookNo = nycCase[1] 
        manh = nycBo[2]
        manNo = nycCase[2]
        queens = nycBo[3]
        queensNo = nycCase[3]
        staten = nycBo[4]
        statenNo = nycCase[4]
        
        #CSV file name and header
        csvfile = "COVID-19_cases_nydoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
         
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended       
        if (hold[0].split('\n')[1].split('[')[0]) == 'Albany' and (hold[-3].split('\n')[1]) == 'Yates' and staten == 'Staten Island':
                    
            file = open(csvfile, "w", encoding = 'utf-8')
            file.write(headers)
            
            for h in hold[0:-2]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1].split('[')[0] + co + "," + ny, key='')
                file.write(take[1].split('[')[0] + "," + ny + "," 
                           + str(fips.get_county_fips(take[1].split('[')[0],state=ny)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].split('[')[0].replace(',','').replace('–','0') + "," 
                           + take[5].replace(',','').replace('–','0') + "," 
                           + take[7].replace(',','').replace('–','0') + "\n")
                
            bronx = liegen.geocode(brnx + "," + ny)
            file.write(brnx + "," + ny + "," + str(fips.get_county_fips(brnx,state=ny)).strip() + "," + str(bronx.latitude)
                       + "," + str(bronx.longitude) + "," + str(brnxNo) + "," + ""  + "," + ""  + "\n")    
            
            brooklyn = liegen.geocode(brook + "," + ny)
            file.write(brook + "," + ny + "," + str(fips.get_county_fips(brook,state=ny)).strip() + "," + str(brooklyn.latitude)
                       + "," + str(brooklyn.longitude) + "," + str(brookNo) + "," + ""  + "," + ""  + "\n")    
            
            hattan = liegen.geocode(manh + "," + ny)
            file.write(manh + "," + ny + "," + str(fips.get_county_fips(manh,state=ny)).strip() + "," + str(hattan.latitude)
                       + "," + str(hattan.longitude) + "," + str(manNo) + "," + ""  + "," + ""  + "\n")  
            
            queen = liegen.geocode(queens + "," + ny)
            file.write(queens + "," + ny + "," + str(fips.get_county_fips(queens,state=ny)).strip() + "," + str(queen.latitude)
                       + "," + str(queen.longitude) + "," + str(queensNo) + "," + ""  + "," + ""  + "\n")
            
            island = liegen.geocode(staten + "," + ny)
            file.write(staten + "," + ny + "," + str(fips.get_county_fips(staten,state=ny)).strip() + "," + str(island.latitude)
                       + "," + str(island.longitude) + "," + str(statenNo) + "," + ""  + "," + ""  + "\n")
            
            file.close()
        
            counter += 1
            print("New York scraper is complete.")
        else:
            print(cl("ERROR: Must fix New York scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for NY scraper.', 'green'))
        pass

def ohScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        ohWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Ohio'
        ohClient = req(ohWiki)
        site_parse = soup(ohClient.read(), "lxml")
        ohClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        oh = "OHIO"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_ohWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Adams' and (hold[-3].split('\n')[1]) == 'Wyandot':
                    
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:-2]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + co + "," + oh, key='')
                file.write(take[1].split('[')[0] + "," + oh + "," + str(fips.get_county_fips(take[1],state=oh)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "," + take[5].replace(',','') + "\n")
            
            file.close()
            
            counter += 1
            print("Ohio scraper is complete.")
        else:
            print(cl("ERROR: Must fix Ohio scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for OH scraper.', 'green'))
        pass
    
def okScrape():
    
    try:
        #This scraper is a bit different
        #First we want to ensure that we are receiving updated information
        #so we pull the information from the page and look for the csv that is 
        #most current
        testUrl = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports'
        testClient = req(testUrl)
        site_parse = soup(testClient.read(), 'lxml')
        testClient.close()
        tables = site_parse.find("div", {"class": "Box mb-3 Box--condensed"})
        tags = tables.find('tbody')
        att = tags.findAll('tr', {"class":"js-navigation-item"})[-2]
        current = att.find('a').text
        #This is the base url sans newest csv file
        git = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
        #Concatenate the two now... Base url and latest csv 
        newUrl = git + current
        #Now we place this into a DataFrame
        df = pd.read_csv(newUrl)
        #From here this is all a matter of cleaning and grouping data by the 
        #categories needed and made into a Dataframe similar to the others in this
        #large scraper
        okDF = df.groupby('Province_State').get_group('Oklahoma')
        okie = okDF[okDF.Admin2 != 'Unassigned']
        hold = okie.reindex(columns = ['Admin2', 'Province_State', 'FIPS', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered'])
        newHold = hold.rename(columns = {'Admin2' : 'County', 'Province_State' : 'State', 'FIPS' : 'fips', 'Lat' : 'Latitude', 'Long_' : 'Longitude', 'Confirmed'  :'Confirmed Cases', 'Recovered':'Recoveries'})
        newHold = newHold.fillna(0)
        newHold = newHold.astype({'fips':'int64'})
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if newHold.at[7, 'County'] == 'Adair' and len(newHold.columns) == 8:
        
            newHold.to_csv('COVID-19_cases_okdoh.csv',index=False, header=True)
            counter += 1
            print("Oklahoma scraper is complete.")
        else:
            print(cl("ERROR: Must fix Oklahoma scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for OK scraper.', 'green'))
        pass
    
def orScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        orDOH = 'https://govstatus.egov.com/OR-OHA-COVID-19'
        orClient = req(orDOH)
        site_parse = soup(orClient.read(), "lxml")
        orClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"id": "collapseDemographics"}).find("tbody")
        tags = tables.findAll('tr')
        
        orG = "OREGON"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_ordoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (tags[0].find('td').text) == 'Baker' and (tags[36].find('td').text) == 'Total':
        
            file = open(csvfile, "w")
            file.write(headers)
            
            for tag in tags[:36]:
                pull = tag.findAll('td')
                locale = geocoder.opencage(pull[0].text.strip() + co + "," + orG, key='')
                file.write(pull[0].text.strip() + "," + orG + "," + str(fips.get_county_fips(pull[0].text,state=orG)).strip() + "," 
                           + str(locale.latlng).strip('[]') + ","
                           + pull[1].text.strip() + "," + pull[2].text.strip() + "\n")
            
            file.close()
            
            counter += 1
            print("Oregon scraper is complete.")
        else:
            print(cl("ERROR: Must fix Oregon scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for OR scraper.', 'green'))
        pass

def paScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        paDOH = 'https://www.health.pa.gov/topics/disease/coronavirus/Pages/Cases.aspx'
        paClient = req(paDOH)
        site_parse = soup(paClient.read(), "lxml")
        paClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "ms-rtestate-field","style": "display:inline"}).find("div", {"style": "text-align:center;"}).find("table", {"class": "ms-rteTable-default"})
        tags = tables.findAll('tr')
        
        pa = "PENNSYLVANIA"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_padoh.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (tags[1].find('td').text) == 'Adams' and (tags[67].find('td').text.strip()) == 'York':
        
            file = open(csvfile, "w")
            file.write(headers)
            
            for tag in tags[1:]:
                pull = tag.findAll('td')
                locale = geocoder.opencage(pull[0].text.strip() + co + "," + pa, key='')
                file.write(pull[0].text.strip() + "," + pa + "," + str(fips.get_county_fips(pull[0].text.strip(),state=pa)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + pull[1].text + "," + pull[3].text + "\n")
            
            file.close()
            
            counter += 1
            print("Pennsylvania scraper is complete.")
        else:
            print(cl("ERROR: Must fix Pennsylvania scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for PA scraper.', 'green'))
        pass

def prScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        prWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Puerto_Rico'
        prClient = req(prWiki)
        site_parse = soup(prClient.read(), "lxml")
        prClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        pr = "PUERTO RICO"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_prWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
        
#        #Break the list into the separate regions of Puerto Rico
#        arec =      hold[70].split('\n')
#        baya =      hold[71].split('\n')
#        caguas =    hold[72].split('\n')
#        faja =      hold[73].split('\n')
#        maya =      hold[74].split('\n')
#        metro =     hold[75].split('\n')
#        ponce =     hold[76].split('\n')
#        usa =       hold[77].split('\n')
#        na =        hold[78].split('\n')
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if hold[0].split('\n')[1] == 'Adjuntas' and hold[-4].split('\n')[1] == 'Unknown':
                    
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:5]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n")
            #Anasco Mun.
            file.write("Anasco" + "," + pr + "," + "72011" + "," 
                       + str(geocoder.opencage(hold[5].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[5].split('\n')[3].replace(',','') + "\n")
            for h in hold[6:16]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            #Catano Mun.
            file.write("Catano" + "," + pr + "," + "72033" + "," 
                       + str(geocoder.opencage(hold[16].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[16].split('\n')[3].replace(',','') + "\n")
            for h in hold[17:22]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            #Comerio Mun.
            file.write("Comerio" + "," + pr + "," + "72045" + "," 
                       + str(geocoder.opencage(hold[22].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[22].split('\n')[3].replace(',','') + "\n")
            for h in hold[23:28]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            #Guanica Mun.
            file.write("Guanica" + "," + pr + "," + "72055" + "," 
                       + str(geocoder.opencage(hold[28].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[28].split('\n')[3].replace(',','') + "\n")
            for h in hold[29:38]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            #Juana Diaz Mun.
            file.write("Juana Diaz" + "," + pr + "," + "72075" + "," 
                       + str(geocoder.opencage(hold[38].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[38].split('\n')[3].replace(',','') + "\n")
            for h in hold[39:42]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            #Las Maria Mun.
            file.write("Las Marias" + "," + pr + "," + "72083" + "," 
                       + str(geocoder.opencage(hold[42].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[42].split('\n')[3].replace(',','') + "\n")
            file.write(hold[43].split('\n')[1] + "," + pr + "," 
                       + str(fips.get_county_fips(hold[43].split('\n')[1],state=pr)).strip() + "," 
                       + str(geocoder.opencage(hold[43].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[43].split('\n')[3].replace(',','') + "\n")
            file.write("Loiza" + "," + pr + "," + "72087" + "," 
                       + str(geocoder.opencage(hold[44].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[44].split('\n')[3].replace(',','') + "\n")
            file.write(hold[45].split('\n')[1] + "," + pr + "," 
                       + str(fips.get_county_fips(hold[45].split('\n')[1],state=pr)).strip() + "," 
                       + str(geocoder.opencage(hold[45].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[45].split('\n')[3].replace(',','') + "\n")
            file.write("Manati" + "," + pr + "," + "72091" + "," 
                       + str(geocoder.opencage(hold[46].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[46].split('\n')[3].replace(',','') + "\n")
            for h in hold[47:49]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            file.write("Mayaguez" + "," + pr + "," + "72097" + "," 
                       + str(geocoder.opencage(hold[49].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[49].split('\n')[3].replace(',','') + "\n")
            for h in hold[50:56]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            file.write("Penuelas" + "," + pr + "," + "72111" + "," 
                       + str(geocoder.opencage(hold[56].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[56].split('\n')[3].replace(',','') + "\n")
            for h in hold[57:60]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            file.write("Rio Grande" + "," + pr + "," + "72119" + "," 
                       + str(geocoder.opencage(hold[60].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[60].split('\n')[3].replace(',','') + "\n")
            for h in hold[61:63]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            file.write("San German" + "," + pr + "," + "72125" + "," 
                       + str(geocoder.opencage(hold[63].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[63].split('\n')[3].replace(',','') + "\n")
            for h in hold[64:66]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            file.write("San Sebastian" + "," + pr + "," + "72131" + "," 
                       + str(geocoder.opencage(hold[66].split('\n')[1] + "," + pr, key='').latlng).strip('[]') + "," 
                       + hold[66].split('\n')[3].replace(',','') + "\n")
            for h in hold[67:-4]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + pr, key='')
                file.write(take[1] + "," + pr + "," + str(fips.get_county_fips(take[1],state=pr)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "\n") 
            file.close()
            
            counter += 1
            print("Puerto Rico scraper is complete.")
        else:
            print(cl("ERROR: Must fix Puerto Rico scraper.", 'red'))
    
    except Exception:
        print(cl('Printed or exception raised for PR scraper.', 'green'))
        pass
    
def riScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        riNews = 'https://www.nytimes.com/interactive/2020/us/rhode-island-coronavirus-cases.html'
        riClient = req(riNews)
        site_parse = soup(riClient.read(), "lxml")
        riClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.findAll("div", {"class": "g-svelte"})[9]
        tags = tables.findAll('td')
        
        ri = "RHODE ISLAND"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_riNews.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tags[6:]:
            take = t.text.split('\n')[1].strip()
            hold.append(take)
        
        #Break the list into the separate counties
        #Uses geocode API that grabs latitude and longitude. According to API's 
        #policy, you must use a sleep function to ensure that you are giving their
        #servers enough time 
        prov = hold[0]
        provL = liegen.geocode(prov + co + "," + ri)
        sleep(1)
        provC = hold[1].replace(',','').replace('—','0')
        provD = hold[3].replace(',','').replace('—','0') 
        
        kent = hold[12]
        kentL = liegen.geocode(kent + co + "," + ri)
        sleep(1)
        kentC = hold[13].replace(',','').replace('—','0')
        kentD = hold[15].replace(',','').replace('—','0')
        
        wash = hold[18]
        washL = liegen.geocode(wash + co + "," + ri)
        sleep(1)
        washC = hold[19].replace(',','').replace('—','0')
        washD = hold[21].replace(',','').replace('—','0')
        
        new = hold[24]
        newL = liegen.geocode(new + co + "," + ri)
        sleep(1)
        newC = hold[25].replace(',','').replace('—','0')
        newD = hold[27].replace(',','').replace('—','0')
        
        brist = hold[30]
        bristL = liegen.geocode(brist + co + "," + ri)
        sleep(1)
        bristC = hold[31].replace(',','').replace('—','0')
        bristD = hold[33].replace(',','').replace('—','0')
        
        unkn = hold[6]
        unkC = hold[7].replace(',','').replace('—','0')
        unkD = hold[9].replace(',','').replace('—','0')
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if prov == "Providence" and unkn == "Unknown":
      
            file = open(csvfile, "w")
            file.write(headers)
            
            file.write(prov + "," + ri + "," + str(fips.get_county_fips(prov,state=ri)).strip() 
                       + "," + str(provL.latitude) + "," 
                       + str(provL.longitude) + "," + provC + "," + provD + "\n")
            
            file.write(kent + "," + ri + "," + str(fips.get_county_fips(kent,state=ri)).strip()
                       + "," + str(kentL.latitude) + "," 
                       + str(kentL.longitude) + "," + kentC + "," + kentD + "\n")
            
            file.write(wash + "," + ri + "," + str(fips.get_county_fips(wash,state=ri)).strip() 
                       + "," + str(washL.latitude) + "," 
                       + str(washL.longitude) + "," + washC + "," + washD + "\n")
            
            file.write(new + "," + ri + "," + str(fips.get_county_fips(new,state=ri)).strip() 
                       + "," + str(newL.latitude) + "," 
                       + str(newL.longitude) + "," + newC + "," + newD + "\n")
            
            file.write(brist + "," + ri + "," + str(fips.get_county_fips(brist,state=ri)).strip() 
                       + "," + str(bristL.latitude) + "," 
                       + str(bristL.longitude) + "," + bristC + "," + bristD + "\n")
            
            file.write(unkn + "," + ri + "," + str(fips.get_state_fips(ri)).strip() +"," 
                       + "" + "," + "" + "," + unkC + "," + unkD + "\n")
            
            file.close()
            
            counter += 1
            print("Rhode Island scraper is complete.")
        else:
            print(cl("ERROR: Must fix Rhode Island scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for RI scraper.', 'green'))
        pass

def scScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        scWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_South_Carolina'
        scClient = req(scWiki)
        site_parse = soup(scClient.read(), "lxml")
        scClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        sc = "SOUTH CAROLINA"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_scWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
              
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Abbeville' and (hold[-3].split('\n')[1]) == 'York':
                    
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:-2]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + co + "," + sc, key='')
                file.write(take[1] + "," + sc + "," + str(fips.get_county_fips(take[1],state=sc)).strip() 
                           + "," + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "," 
                           + take[5].replace(',','') + "\n")
            
            file.close()
            
            counter += 1
            print("South Carolina scraper is complete.")
        else:
            print(cl("ERROR: Must fix South Carolina scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for SC scraper.', 'green'))
        pass

def sdScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        sdWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_South_Dakota'
        sdClient = req(sdWiki)
        site_parse = soup(sdClient.read(), "lxml")
        sdClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        sd = "SOUTH DAKOTA"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_sdWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
            pull = t.findAll('tr')
            for p in pull[2:]:
                take = p.get_text()
                hold.append(take)
           
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended     
        if (hold[0].split('\n')[1]) == 'Aurora' and (hold[-3].split('\n')[1]) == 'Ziebach':
                    
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:-2]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + co + "," + sd, key='')
                file.write(take[1] + "," + sd + "," + str(fips.get_county_fips(take[1],state=sd)).strip() 
                           + "," + str(locale.latlng).strip('[]') + "," 
                           + take[3].replace(',','') + "," 
                           + take[5].replace(',','') + "," 
                           + take[7].replace(',','') + "\n")
            
            file.close()
            
            counter += 1
            print("South Dakota scraper is complete.")
        else:
            print(cl("ERROR: Must fix South Dakota scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for SD scraper.', 'green'))
        pass
    
def tnScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        tnWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Tennessee'
        tnClient = req(tnWiki)
        site_parse = soup(tnClient.read(), "lxml")
        tnClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        #CSV file name and header
        csvfile = "COVID-19_cases_tnWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        tn = "TENNESSEE"
        co = ' County'
        
        #Hold all of the table's information into an easy to dissect list
        hold = []    
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)    
          
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended          
        if (hold[0].split('\n')[1]) == 'Anderson' and (hold[-3].split('\n')[1]) == 'Pending':
            
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:-4]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1].split('[')[0] + co + "," + tn, key='')
                file.write(take[1].split('[')[0] + "," + tn + "," + str(fips.get_county_fips(take[1].split('[')[0],state=tn)).strip() + "," 
                           + str(locale.latlng).strip('[]') +  "," 
                           + take[3].split('[')[0].replace(',','').replace('–','0') + "," 
                           + take[5].split('[')[0].replace(',','').replace('–','0') + "," 
                           + take[7].split('[')[0].replace(',','').replace('–','0') +"\n")
            
            file.write(hold[-4].split('\n')[1].split('[')[0] + "," + tn +  "," 
                       + str(fips.get_state_fips(tn)).strip() + ","  
                       + str(geocoder.opencage(tn, key='').latlng).strip('[]') +","
                       + hold[-4].split('\n')[3].replace(',','').replace('–','0') + "," 
                       + hold[-4].split('\n')[5].replace(',','').replace('–','0') + "," 
                       + hold[-4].split('\n')[7].replace(',','').replace('–','0') +"\n")
            file.write(hold[-3].split('\n')[1].split('[')[0] + "," + tn +  "," 
                       + str(fips.get_state_fips(tn)).strip() + ","
                       + str(geocoder.opencage(tn, key='').latlng).strip('[]') +","
                       + hold[-3].split('\n')[3].replace(',','').replace('–','0') + "," 
                       + hold[-3].split('\n')[5].replace(',','').replace('–','0') + "," 
                       + hold[-3].split('\n')[7].replace(',','').replace('–','0') +"\n")
                
            file.close()
            
            counter += 1
            print("Tennessee scaper is complete.")
        else:
            print(cl("ERROR: Must fix Tennessee scraper.", 'red'))
    
    except Exception:
        print(cl('Printed or exception raised for TN scraper.', 'green'))
        pass

def txScrape():
    
    try:
        #First we want to ensure that we are receiving updated information
        #so we pull the information from the page and look for the csv that is 
        #most current
        txUrl = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports'
        txClient = req(txUrl)
        site_parse = soup(txClient.read(), 'lxml')
        txClient.close()
        tables = site_parse.find("div", {"class": "Box mb-3 Box--condensed"})
        tags = tables.find('tbody')
        att = tags.findAll('tr', {"class":"js-navigation-item"})[-2]
        current = att.find('a').text
        
        #This is the base url sans newest csv file
        git = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
        #Concatenate the two now... Base url and latest csv        
        newUrl = git + current
        #Now we place this into a DataFrame
        txdf = pd.read_csv(newUrl)
        #From here this is all a matter of cleaning and grouping data by the 
        #categories needed and made into a Dataframe similar to the others in this
        #large scraper
        hold = []
        newHold = []
            
        txDF = txdf.groupby('Province_State').get_group('Texas')
        tex = txDF[txDF.Admin2 != 'Unassigned']
        hold = tex.reindex(columns = ['Admin2', 'Province_State', 'FIPS', 'Lat', 'Long_', 'Confirmed', 'Deaths', 'Recovered'])
        newHold = hold.rename(columns = {'Admin2' : 'County', 'Province_State' : 'State', 'FIPS' : 'fips', 'Lat' : 'Latitude', 'Long_' : 'Longitude', 'Confirmed'  :'Confirmed Cases', 'Recovered':'Recoveries'})
        newHold = newHold.fillna(0)
        newHold = newHold.astype({'fips':'int64'})
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if newHold.at[57, 'County'] == 'Anderson':
            newHold.to_csv('COVID-19_cases_txgit.csv',index=False, header=True)
            counter += 1
            print("Texas scraper is complete.")
        else:
            print(cl("ERROR: Must fix Texas scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for TX scraper.', 'green'))
        pass

def utScrape():
    
    #The Utah scraper is built from smaller scrapers pulling information
    #from multiple sites (DOH and Wiki)
    
    try:
        #Central Utah Health District broken into separate counties
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        cenUT = 'https://centralutahpublichealth.org/'
        utClient = req(cenUT)
        site_parse = soup(utClient.read(), 'lxml')
        utClient.close()
        
        #Narrow down the parse to the section that is most pertinent based on counties
        juab = site_parse.find("div", {"class":"n2-ss-layer n2-ow"}).findAll("div", {"class":"n2-ss-layer n2-ow"})[9]
        juabCo = "Juab COunty"
        juabCase = str([int(n) for n in (juab.findAll('p')[0].text.split()) if n.isdigit()][0])
        juabHosp = str([int(n) for n in (juab.findAll('p')[0].text.split()) if n.isdigit()][1])
        juabMort = str([int(n) for n in (juab.findAll('p')[0].text.split()) if n.isdigit()][2])
        juabHope = str([int(n) for n in (juab.findAll('p')[0].text.split()) if n.isdigit()][3])
        millard = site_parse.find("div", {"class":"n2-ss-layer n2-ow"}).findAll("div", {"class":"n2-ss-layer n2-ow"})[11]
        millCo = "Millard County"
        millCase = str([int(n) for n in (millard.findAll('p')[0].text.split()) if n.isdigit()][0])
        millHosp = str([int(n) for n in (millard.findAll('p')[0].text.split()) if n.isdigit()][1])
        millMort = str([int(n) for n in (millard.findAll('p')[0].text.split()) if n.isdigit()][2])
        millHope = str([int(n) for n in (millard.findAll('p')[0].text.split()) if n.isdigit()][3])
        piute = site_parse.find("div", {"class":"n2-ss-layer n2-ow"}).findAll("div", {"class":"n2-ss-layer n2-ow"})[13]
        piuteCo = "Piute County"
        piuteCase = str([int(n) for n in (piute.findAll('p')[0].text.split()) if n.isdigit()][0])
        piuteHosp = str([int(n) for n in (piute.findAll('p')[0].text.split()) if n.isdigit()][1])
        piuteMort = str([int(n) for n in (piute.findAll('p')[0].text.split()) if n.isdigit()][2])
        piuteHope = str([int(n) for n in (piute.findAll('p')[0].text.split()) if n.isdigit()][3])
        sanpete = site_parse.find("div", {"class":"n2-ss-layer n2-ow"}).findAll("div", {"class":"n2-ss-layer n2-ow"})[15]
        sanpeteCo = "Sanpete County"
        speteCase = str([int(n) for n in (sanpete.findAll('p')[0].text.split()) if n.isdigit()][0])
        speteHosp = str([int(n) for n in (sanpete.findAll('p')[0].text.split()) if n.isdigit()][1])
        speteMort = str([int(n) for n in (sanpete.findAll('p')[0].text.split()) if n.isdigit()][2])
        speteHope = str([int(n) for n in (sanpete.findAll('p')[0].text.split()) if n.isdigit()][3])
        sevier = site_parse.find("div", {"class":"n2-ss-layer n2-ow"}).findAll("div", {"class":"n2-ss-layer n2-ow"})[17]
        sevCo = "Sevier County"
        sevCase = str([int(n) for n in (sevier.findAll('p')[0].text.split()) if n.isdigit()][0])
        sevHosp = str([int(n) for n in (sevier.findAll('p')[0].text.split()) if n.isdigit()][1])
        sevMort = str([int(n) for n in (sevier.findAll('p')[0].text.split()) if n.isdigit()][2])
        sevHope = str([int(n) for n in (sevier.findAll('p')[0].text.split()) if n.isdigit()][3])
        wayne = site_parse.find("div", {"class":"n2-ss-layer n2-ow"}).findAll("div", {"class":"n2-ss-layer n2-ow"})[19]
        wayCo = "Wayne County"
        wayCase = str([int(n) for n in (wayne.findAll('p')[0].text.split()) if n.isdigit()][0])
        wayHosp = str([int(n) for n in (wayne.findAll('p')[0].text.split()) if n.isdigit()][1])
        wayMort = str([int(n) for n in (wayne.findAll('p')[0].text.split()) if n.isdigit()][2])
        wayHope = str([int(n) for n in (wayne.findAll('p')[0].text.split()) if n.isdigit()][3])
        
        #Bear River Health District broken into counties
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        bearRiv = 'https://brhd.org/coronavirus/'
        utClient1 = req(bearRiv)
        site_parse1 = soup(utClient1.read(), 'lxml')
        utClient1.close()
        
        #Narrow down the parse to the section that is most pertinent 
        bearTab = site_parse1.findAll("div", {"class":"et_pb_text_inner"})        
        
        #Broken into counties in lists
        counties = []
        for t in bearTab[3:6]:
            take = t.text
            counties.append(take)
        cases = []
        for t in bearTab[8:11]:
            take = t.text
            cases.append(take)
        khaus  = []
        for t in bearTab[13:16]:
            take = t.text
            khaus.append(take)
        recov = []
        for t in bearTab[18:21]:
            take = t.text
            recov.append(take)
        mort = []
        for t in bearTab[23:26]:
            take = t.text
            mort.append(take)
        
        #Zip them all into one list again
        bearRiver = list(zip(counties, cases, khaus, recov, mort))
        
        boxElder = bearRiver[0]
        boxCo = boxElder[0]
        boxCase = boxElder[1]
        boxKhaus = boxElder[2]
        boxRec = boxElder[3]
        boxMort = boxElder[4]
    
        cache = bearRiver[1]
        cacheCo = cache[0]
        cacheCase = cache[1]
        cacheKhaus = cache[2]
        cacheRec = cache[3]
        cacheMort = cache[4]
        
        rich = bearRiver[2]
        richCo = rich[0]
        richCase = rich[1]
        richKhaus = rich[2]
        richRec = rich[3]
        richMort = rich[4]
        
        #Davis County
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        davisCounty = 'http://www.daviscountyutah.gov/health/covid-19'
        utClient2 = req(davisCounty)
        site_parse2 = soup(utClient2.read(), 'lxml')
        utClient2.close()
        
        #Narrow down the parse to the section that is most pertinent 
        davTab = site_parse2.find("section", {"class":"pv-15 stats fixed-bg default-bg hovered"})
        stats = davTab.findAll('span')
        davCo = "Davis County"
        davCases = stats[1].text
        davKhaus = stats[3].text
        davMort = stats[5].text
        
        #Salt lake County
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        saltWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Utah'
        utClient3 = req(saltWiki)
        site_parse3 = soup(utClient3.read(), 'lxml')
        utClient3.close()
        
        #Narrow down the parse to the section that is most pertinent 
        saltTab = site_parse3.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in saltTab:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
        
        #Salt Lake County
        salt = hold[17].split('\n')
        saltLake = salt[1]
        saltCase = salt[3].replace('–','0')
        saltMort = salt[5].replace('–','0')
        saltRec = salt[7].replace('–','0')
        
        #San Juan County
        sanjuan = hold[18].split('\n')
        sanJ = sanjuan[1]
        sanCases = sanjuan[3].replace('–','0')
        sanMort = sanjuan[5].replace('–','0')
        sanRec = sanjuan[7].replace('–','0')
        
        #Southeast Utah Health District broken into counties
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        seUtah = 'https://www.seuhealth.com/covid-19'
        utClient4 = req(seUtah)
        site_parse4 = soup(utClient4.read(), 'lxml')
        utClient4.close()
        
        #Narrow down the parse to the section that is most pertinent 
        seTab = site_parse4.find("div", {"id": "comp-k9lpzm1j1inlineContent-gridContainer"}).findAll("h3", {"class":"font_3"})    
        carbon = seTab[2].text
        carCase = seTab[3].text.strip("*")
        emery = seTab[4].text
        emCase = seTab[5].text.strip("*")
        grand = seTab[6].text
        grCase = seTab[7].text.strip("*")
        
        #Southwest Utah Health District 
        beaver = "Beaver County"
        bevCase = hold[0].split('\n')[3].replace('–','0')
        bevMort = hold[0].split('\n')[5].replace('–','0')
        bevRec = hold[0].split('\n')[7].replace('–','0')

        
        garfield = "Garfield County"
        garCase = hold[8].split('\n')[3].replace('–','0')
        garMort = hold[8].split('\n')[5].replace('–','0')
        garRec = hold[8].split('\n')[7].replace('–','0')
        
        iron = "Iron County"
        feCase = hold[10].split('\n')[3].replace('–','0')
        feMort = hold[10].split('\n')[5].replace('–','0')
        feRec = hold[10].split('\n')[7].replace('–','0')

        
        kane = "Kane County"
        kaneCase = hold[12].split('\n')[3].replace('–','0')
        kaneMort = hold[12].split('\n')[5].replace('–','0')
        kaneRec = hold[12].split('\n')[7].replace('–','0')

        
        washC = "Washington County"
        washCase = hold[26].split('\n')[3].replace('–','0')
        washMort = hold[26].split('\n')[5].replace('–','0')
        washRec = hold[26].split('\n')[7].replace('–','0')

        
        #Summit County 
        summit = hold[21].split('\n')
        sumCo = summit[1] + " County"
        sumCase = summit[3].replace('–','0')
        sumMort = summit[5].replace('–','0')
        sumRec = summit[7].replace('–','0')
        
        #Tooele County
        tooele = hold[22].split('\n')
        toolCo = tooele[1] + " County"
        toolCase = tooele[3].replace('–','0')
        toolMort = tooele[5].replace('–','0')
        toolRec = tooele[7].replace('–','0')
        
        #TriCounty Health District broken into counties
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        triUT = 'https://tricountyhealth.com/local-covid-19-situational-update/'
        utClient5 = req(triUT)
        site_parse5 = soup(utClient5.read(), 'lxml')
        utClient5.close()
        
        #Narrow down the parse to the section that is most pertinent 
        triTab = site_parse5.find("div", {"class": "et_pb_row et_pb_row_3"}).findAll("div", {"class": "et_pb_text_inner"})    
        uintah = triTab[0].text.split('\n')
        uintahCo = "Uintah County"
        uintahCase = uintah[1].split(": ")[1]
        uintahKhaus = uintah[2].split(": ")[1]
        
        duchesne = triTab[1].text.split('\n')
        duchCo = "Duchesne County"
        duchCase = duchesne[1].split(": ")[1]
        duchKhaus = duchesne[2].split(": ")[1]
        
        daggett = triTab[2].text.split('\n')
        daggCo = "Daggett County"
        daggCase = daggett[1].split(": ")[1]
        daggKhaus = daggett[2].split(": ")[1]
    
        #Utah County
        utah = hold[24].split('\n')
        utahCo = utah[1]
        utahCase = utah[3].replace('–','0')
        utahMort = utah[5].replace('–','0')
        utahRec = utah[7].replace('–','0')
        
        #Wasatch County
        wasa = hold[25].split('\n')
        wasaCo = wasa[1] + ' County'
        wasaCase = wasa[3].replace('–','0')
        wasaMort = wasa[5].replace('–','0')
        wasaRec = wasa[7].replace('–','0')
        
        #Weber-Morgan Health District
        weber = hold[28].split('\n')
        webCo = weber[1] + ' County'
        webCase = weber[3].replace('–','0')
        webMort = weber[5].replace('–','0')
        webRec = weber[7].replace('–','0')
        webFips = "49057"
        
        ut = "UTAH"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_utNews.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries,,Hospitalizations\n"
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if  boxCo == 'Box Elder' and saltLake == 'Salt Lake' and uintah[0] == 'UINTAH COUNTY':
        
            file = open(csvfile, "w")
            file.write(headers)
            
            file.write(juabCo + "," + ut + "," + str(fips.get_county_fips(juabCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(juabCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + juabCase + "," + juabMort + "," + juabHope + "," + "" + "," + juabHosp + "\n")
            file.write(millCo + "," + ut + "," + str(fips.get_county_fips(millCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(millCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + millCase + "," + millMort + "," + millHope + "," + "" + "," + millHosp + "\n")
            file.write(piuteCo + "," + ut + "," + str(fips.get_county_fips(piuteCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(piuteCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + piuteCase + "," + piuteMort + "," + piuteHope + "," + "" + "," + piuteHosp + "\n")
            file.write(sanpeteCo + "," + ut + "," + str(fips.get_county_fips(sanpeteCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(sanpeteCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + speteCase + "," + speteMort + "," + speteHope + "," + "" + "," + speteHosp + "\n")
            file.write(sevCo + "," + ut + "," + str(fips.get_county_fips(sevCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(sevCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + sevCase + "," + sevMort + "," + sevHope + "," + "" + "," + sevHosp + "\n")
            file.write(wayCo + "," + ut + "," + str(fips.get_county_fips(wayCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(wayCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + wayCase + "," + wayMort + "," + wayHope + "," + "" + "," + wayHosp + "\n")
            file.write(boxCo + "," + ut + "," + str(fips.get_county_fips(boxCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(boxCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + boxCase + "," + boxMort + "," + boxRec + "," + "" + "," + boxKhaus + "\n")
            file.write(cacheCo + "," + ut + "," + str(fips.get_county_fips(cacheCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(cacheCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + cacheCase + "," + cacheMort + "," + cacheRec + "," + "" + "," + cacheKhaus + "\n")
            file.write(richCo + "," + ut + "," + str(fips.get_county_fips(richCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(richCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + richCase + "," + richMort + "," + richRec + "," + "" + "," + richKhaus + "\n")
            file.write(davCo + "," + ut + "," + str(fips.get_county_fips(davCo,state=ut)).strip()
                       + "," + str(geocoder.opencage(davCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + davCases + "," + davMort + "," + "" + "," + "" + "," + davKhaus + "\n")
            file.write(saltLake + "," + ut + "," + str(fips.get_county_fips(saltLake,state=ut)).strip() 
                       + "," + str(geocoder.opencage(saltLake + ", " + ut,key='').latlng).strip('[]')
                       + "," + saltCase.replace(',','') + "," + saltMort.replace(',','') + "," + saltRec.replace(',','') + "," + "" + "," + "" + "\n")
            file.write(sanJ + "," + ut + "," + str(fips.get_county_fips(sanJ,state=ut)).strip() 
                       + "," + str(geocoder.opencage(sanJ + ", " + ut,key='').latlng).strip('[]')
                       + "," + sanCases + "," + sanMort + "," + sanRec + "," + "" + "," + "" + "\n")
            file.write(carbon + "," + ut + "," + str(fips.get_county_fips(carbon,state=ut)).strip() 
                       + "," + str(geocoder.opencage(carbon + ", " + ut,key='').latlng).strip('[]')
                       + "," + carCase + "," + "" + "," + "" + "," + "" + "," + "" + "\n")
            file.write(emery + "," + ut + "," + str(fips.get_county_fips(emery,state=ut)).strip() 
                       + "," + str(geocoder.opencage(emery + ", " + ut,key='').latlng).strip('[]')
                       + "," + emCase + "," + "" + "," + "" + "," + "" + "," + "" + "\n")
            file.write(grand + "," + ut + "," + str(fips.get_county_fips(grand,state=ut)).strip() 
                       + "," + str(geocoder.opencage(grand + ", " + ut,key='').latlng).strip('[]')
                       + "," + grCase + "," + "" + "," + "" + "," + "" + "," + "" + "\n")
            file.write(beaver + "," + ut + "," + str(fips.get_county_fips(beaver,state=ut)).strip() 
                       + "," + str(geocoder.opencage(beaver + ", " + ut,key='').latlng).strip('[]')
                       + "," + bevCase + "," + bevMort + "," + bevRec + "," + "" + "," + "" + "\n")
            file.write(garfield + "," + ut + "," + str(fips.get_county_fips(garfield,state=ut)).strip() 
                       + "," + str(geocoder.opencage(garfield + ", " + ut,key='').latlng).strip('[]')
                       + "," + garCase + "," + garMort + "," + "" + "," + "" + "," + "" + "\n")
            file.write(iron + "," + ut + "," + str(fips.get_county_fips(iron,state=ut)).strip() 
                       + "," + str(geocoder.opencage(iron + ", " + ut,key='').latlng).strip('[]')
                       + "," + feCase + "," + feMort + "," + feRec + "," + "" + "," + "" + "\n")
            file.write(kane + "," + ut + "," + str(fips.get_county_fips(kane,state=ut)).strip() 
                       + "," + str(geocoder.opencage(kane + ", " + ut,key='').latlng).strip('[]')
                       + "," + kaneCase + "," + kaneMort + "," + kaneRec + "," + "" + "," + "" + "\n")
            file.write(washC + "," + ut + "," + str(fips.get_county_fips(washC,state=ut)).strip() 
                       + "," + str(geocoder.opencage(washC + ", " + ut,key='').latlng).strip('[]')
                       + "," + washCase + "," + washMort + "," + washRec + "," + "" + "," + "" + "\n")
            file.write(sumCo + "," + ut + "," + str(fips.get_county_fips(sumCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(sumCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + sumCase + "," + sumMort + "," + sumRec + "," + "" + "," + "" + "\n")
            file.write(toolCo + "," + ut + "," + str(fips.get_county_fips(toolCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(toolCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + toolCase + "," + toolMort + "," + toolRec + "," + "" + "," + "" + "\n")
            file.write(uintahCo + "," + ut + "," + str(fips.get_county_fips(uintahCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(uintahCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + uintahCase + "," + "" + "," + "" + "," + "" + "," + uintahKhaus + "\n")
            file.write(duchCo + "," + ut + "," + str(fips.get_county_fips(duchCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(duchCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + duchCase + "," + "" + "," + "" + "," + "" + "," + duchKhaus + "\n")
            file.write(daggCo + "," + ut + "," + str(fips.get_county_fips(daggCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(daggCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + daggCase + "," + "" + "," + "" + "," + "" + "," + daggKhaus + "\n")
            file.write(utahCo + "," + ut + "," + str(fips.get_county_fips(utahCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(utahCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + utahCase + "," + utahMort + "," + utahRec + "," + "" + "," + "" + "\n")
            file.write(wasaCo + "," + ut + "," + str(fips.get_county_fips(wasaCo,state=ut)).strip() 
                       + "," + str(geocoder.opencage(wasaCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + wasaCase + "," + wasaMort + "," + wasaRec + "," + "" + "," + "" + "\n")
            file.write(webCo + "," + ut + "," + webFips 
                       + "," + str(geocoder.opencage(webCo + ", " + ut,key='').latlng).strip('[]')
                       + "," + webCase + "," + webMort + "," + webRec + "," + "" + "," + "" + "\n")
            file.close()
            
            counter += 1
            print("Utah scraper is complete.")
        else:
            print(cl('ERROR: Must fix Utah scraper.', 'red'))

    except Exception:
        print(cl('Printed or exception raised for UT scraper.', 'green'))
        pass
    
def vaScrape():
    
    try:
        #Tested out the wikipedia api with this scraper
        #This first line surpresses the SettingwithCopyWarning
        #Got the info from: https://www.dataquest.io/blog/settingwithcopywarning/
        pd.set_option('mode.chained_assignment', None)
        #Search for pages with this criteria
        check = wikipedia.search('Virginia Coronavirus')[0]
        #Pull contents of page
        covVA = wikipedia.page(check).html().encode('UTF-8')
        #Read html of this specific table dealing with the case load in VA based on counties
        countyTab = pd.read_html(covVA)[3]
        #Place the column names in a list format
        head = list(countyTab.columns)
        cnty = head[0]
        case = head[1]
        mort = head[2]
        hosp = head[3]
        #Subset table with necessary columns
        newTab = countyTab[[cnty, case, mort, hosp]]
        #Drop level 0 from table
        newTab.columns = newTab.columns.droplevel(1)
        #Add state column
        newTab.loc[:,'State'] = "VIRGINIA"
        #Rename the columns for easier use and proper format for header in csv
        nameTab = newTab.rename(columns = {newTab.columns[0]: 'County',
                                           newTab.columns[1]: 'Confirmed Cases',
                                           newTab.columns[2]: 'Deaths',
                                           newTab.columns[3]: 'Hospitalizations'})
        #Drop last two rows
        nameTab.drop(nameTab.tail(2).index, inplace=True)
        #Add fips and geolocation to the table
        namen = nameTab['County']
        namen = namen.tolist()
            #Append fips and geolocation to appropriate counties
        bea = []
        for n in namen:
            locale = geocoder.opencage(n + ", " + "VIRGINIA", key= '').latlng
            bea.append(locale)
        #Before adding them to the dataframe, we shall strip them of the brackets
        convert=[]
        for bo in bea:
            con = str(bo)
            convert.append(con.strip('[]'))
        #Split them apart now... How sad...
        lat=[]
        lon=[]
        for c in convert:
            pull=c.split(', ')
            lat.append(pull[0])
            lon.append(pull[1])
        #Insert into the dataframe
        nameTab.insert(1, 'Latitude', lat)
        nameTab.insert(2, 'Longitude', lon)
        sophia = []
        for n in namen:
            fipsVA = fips.get_county_fips(n, state = "VIRGINIA")
            sophia.append(fipsVA)
        nameTab['fips'] = sophia
        
        #Reindex columns in table to be a proper format 
        vaTab = nameTab.reindex(columns = ['County','State','fips','Latitude', 'Longitude',
                                           'Confirmed Cases','Deaths','Hospitalizations'])
        
        #FIPS Codes not included in table    
        #Alexandria (city)
        vaTab.loc[vaTab['County'] == 'Alexandria[c]', 'fips'] = "51510"
        #Bristol 
        vaTab.loc[vaTab['County'] == 'Bristol[c]', 'fips'] = "51520"
        #Buena Vista
        vaTab.loc[vaTab['County'] == 'Buena Vista[c]', 'fips'] = "51530"
        #Charlottesville
        vaTab.loc[vaTab['County'] == 'Charlottesville[c]', 'fips'] = "51540"
        #Chesapeake (city)
        vaTab.loc[vaTab['County'] == 'Chesapeake[c]', 'fips'] = "51550"
        #Colonial Heights (city)
        vaTab.loc[vaTab['County'] == 'Colonial Heights[c]', 'fips'] = "51570"
        #Covington (city)
        vaTab.loc[vaTab['County'] == 'Covington[c]', 'fips'] = "51580"
        #Danville
        vaTab.loc[vaTab['County'] == 'Danville[c]', 'fips'] = "51590"
        #Emporia
        vaTab.loc[vaTab['County'] == 'Emporia[c]', 'fips'] = "51595"
        #Fairfax (city)
        vaTab.loc[vaTab['County'] == 'Fairfax[c]', 'fips'] = "51600"
        #Falls Church
        vaTab.loc[vaTab['County'] == 'Falls Church[c]', 'fips'] = "51610"
        #Franklin
        vaTab.loc[vaTab['County'] == 'Franklin[c]', 'fips'] = "51620"
        #Fredericksburg
        vaTab.loc[vaTab['County'] == 'Fredericksburg[c]', 'fips'] = "51630"
        #Galax
        vaTab.loc[vaTab['County'] == 'Galax[c]', 'fips'] = "51640"
        #Hampton
        vaTab.loc[vaTab['County'] == 'Hampton[c]', 'fips'] = "51650"
        #Harrisonburg
        vaTab.loc[vaTab['County'] == 'Harrisonburg[c]', 'fips'] = "51660"
        #Hopewell
        vaTab.loc[vaTab['County'] == 'Hopewell[c]', 'fips'] = "51670"
        #Lexington
        vaTab.loc[vaTab['County'] == 'Lexington[c]', 'fips'] = "51678"
        #Lynchburg
        vaTab.loc[vaTab['County'] == 'Lynchburg[c]', 'fips'] = "51680"
        #Manassas 
        vaTab.loc[vaTab['County'] == 'Manassas[c]', 'fips'] = "51683"
        #Manassas Park
        vaTab.loc[vaTab['County'] == 'Manassas Park[c]', 'fips'] = "51685"
        #Newport News
        vaTab.loc[vaTab['County'] == 'Newport News[c]', 'fips'] = "51700"
        #Norfolk
        vaTab.loc[vaTab['County'] == 'Norfolk[c]', 'fips'] = "51710"
        #Norton
        vaTab.loc[vaTab['County'] == 'Norton[c]', 'fips'] = "51720"
        #Petersburg
        vaTab.loc[vaTab['County'] == 'Petersburg[c]', 'fips'] = "51730"
        #Poquoson
        vaTab.loc[vaTab['County'] == 'Poquoson[c]', 'fips'] = "51735"
        #Portsmouth
        vaTab.loc[vaTab['County'] == 'Portsmouth[c]', 'fips'] = "51740"
        #Radford
        vaTab.loc[vaTab['County'] == 'Radford[c]', 'fips'] = "51750"
        #Richmond
        vaTab.loc[vaTab['County'] == 'Richmond[c]', 'fips'] = "51760"
        #Roanoke
        vaTab.loc[vaTab['County'] == 'Roanoke[c]', 'fips'] = "51770"
        #Salem
        vaTab.loc[vaTab['County'] == 'Salem[c]', 'fips'] = "51775"
        #Stauton
        vaTab.loc[vaTab['County'] == 'Staunton[c]', 'fips'] = "51790"
        #Suffolk
        vaTab.loc[vaTab['County'] == 'Suffolk[c]', 'fips'] = "51800"
        #Virginia Beach
        vaTab.loc[vaTab['County'] == 'Virginia Beach[c]', 'fips'] = "51810"
        #Waynesboro
        vaTab.loc[vaTab['County'] == 'Waynesboro[c]', 'fips'] = "51820"
        #Williamsburg
        vaTab.loc[vaTab['County'] == 'Williamsburg[c]', 'fips'] = "51830"
        #Winchester
        vaTab.loc[vaTab['County'] == 'Winchester[c]', 'fips'] = "51840"
        
        #Clean up any 'None' data
        vaTab = vaTab.fillna(0)
        #Remove the last row as this contains total 
        #vaTab.drop(vaTab.tail(1).index, inplace = True)
        
        #Now place all this into csv 
        #Create a check 
        if len(head) == 6 and cnty[0].strip(' [a]') == 'County' and vaTab.at[0, 'County'] == 'Accomack':
            vaTab.to_csv('COVID-19_cases_vaWiki.csv', index = False, header = True)
            counter += 1
            print("Virginia scraper is complete.")
        else:
            print(cl("ERROR: Must fix Virginia scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for VA scraper.', 'green'))
        pass
        
def viScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        viDOH = 'https://www.covid19usvi.com/?utm_source=doh&utm_medium=web&utm_campaign=covid19usvi'
        viClient = req(viDOH)
        site_parse = soup(viClient.read(), "lxml")
        viClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class":"views-element-container block block-views block-views-blockcovid-19-epi-summary-block-1"}).find("div", {"class":"view-content"})
        tags = tables.findAll("div", {"class":"field-content"})
        checks = tables.findAll('span')
        
        vi = "US VIRGIN ISLANDS"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_vidoh.csv"
        headers = "State/Territory,State/Territory,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recovered\n"
        
        #Break the list into confirmed cases, recoveries, deaths
        posNo = tags[0].text
        
        recNo = tags[6].text.split('/')[0]
            
        mortNo = tags[4].text
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (checks[0].text == 'Positive') and (checks[2].text == 'Pending'):
        
            file = open(csvfile, "w")
            file.write(headers)
            
            locale = liegen.geocode(vi)
            sleep(1)
            file.write(vi + "," + vi + "," + str(fips.get_state_fips("Virgin Islands")) 
                       + "," + str(locale.latitude) + "," 
                       + str(locale.longitude) + "," + posNo + "," + mortNo + "," 
                       + recNo + "," + "" + "," + "" + "," + "" + "\n")
            
            file.close()
            
            counter += 1
            print("US Virgin Islands scraper is complete.")
        else:
            print(cl("ERROR: Must fix US Virgin Islands scraper.", 'red'))
            
    except Exception:
        print(cl('Printed or exception raised for VI scraper.', 'green'))
        pass

def vtScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        vtWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Vermont'
        vtClient = req(vtWiki)
        site_parse = soup(vtClient.read(), "lxml")
        vtClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        vt = "VERMONT"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_vtWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
         
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended       
        if (hold[0].split('\n')[1]) == 'Addison' and (hold[-3].split('\n')[1]) == 'Unassigned':
    
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:-3]:
                take = h.split('\n')
                locale = liegen.geocode(take[1] + co + "," + vt)
                catch_TimeOut(take[1] + co + "," + vt)
                file.write(take[1] + "," + vt + "," + str(fips.get_county_fips(take[1],state=vt)).strip() 
                           + "," + str(locale.latitude) + ","
                           + str(locale.longitude) + "," 
                           + take[3].replace(',','').replace('–','0') + "," 
                           + take[5].replace(',','').replace('–','0') + ","
                           + take[7].replace(',','').replace('–','0') + "\n")
                sleep(1.1)
            
            file.write(hold[-3].split('\n')[1] + "," + vt + "," 
                       + str(fips.get_state_fips(vt)).strip() + "," 
                       + str(liegen.geocode(vt).latitude) + ","
                       + str(liegen.geocode(vt).longitude) + "," 
                       + hold[-3].split('\n')[3].replace(',','') + "," 
                       + hold[-3].split('\n')[5].replace(',','') + "," 
                       + hold[-3].split('\n')[7].replace(',','').replace('n/a','') + "\n")
            
            file.close()
        
            counter += 1
            print("Vermont scraper is complete.")
        else:
            print(cl("ERROR: Must fix Vermont scraper.", 'red'))
            
    except Exception:
        print(cl('Printed or exception raised for VT scraper.', 'green'))
        pass
    
def waScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        waWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Washington_(state)'
        waClient = req(waWiki)
        site_parse = soup(waClient.read(), "lxml")
        waClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        wa = "WASHINGTON"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_waWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Adams' and (hold[-3].split('\n')[1]) == 'Unassigned':
        
            file = open(csvfile, "w")
            file.write(headers)    
        
            for h in hold[0:-3]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + co + "," + wa, key='')
                file.write(take[1] + "," + wa + "," + str(fips.get_county_fips(take[1],state=wa)).strip() + "," 
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].split('[')[0].replace(',','') 
                           + "," + take[5].split('[')[0].replace(',','') + "\n")
                
            file.write(hold[-3].split('\n')[1] + "," + wa + "," 
                       + str(fips.get_state_fips(wa)).strip() + "," 
                       + str(liegen.geocode(wa).latitude) + "," 
                       + str(liegen.geocode(wa).longitude) + "," 
                       + hold[-3].split('\n')[3].split('[')[0].replace(',','') + "," 
                       + hold[-3].split('\n')[5].split('[')[0].replace(',','') + "\n")
            
            file.close()
            
            counter += 1
            print("Washington scraper is complete.")
        else:
            print(cl("ERROR: Must fix Washington scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for WA scraper.', 'green'))
        pass
    
def wiScrape():
    
    try:    
        #Data pulled from Wisconsin's DOH open data source
        widoh = pd.read_csv('https://opendata.arcgis.com/datasets/9d0cb9329d5745cfbf6ce91fa9835c6e_1.csv')
        #Select columns needed
        widoh = widoh[['NAME', 'POSITIVE', 'DEATHS','GEOID']]
        #Add state to the dataframe
        widoh.loc[:,'State'] = "WISCONSIN"
        #Add lat, long to the dataframe
        county = widoh['NAME']
        county = county.tolist()
        rose = []
        for c in county:
            locale = geocoder.opencage(c + ", " + "WISCONSIN", key= '').latlng
            rose.append(locale)
            #Before adding them to the dataframe, we shall strip them of the brackets
        convert=[]
        for ro in rose:
            con = str(ro)
            convert.append(con.strip('[]'))
        #Split them apart now... How sad...
        lat=[]
        lon=[]
        for c in convert:
            pull=c.split(', ')
            lat.append(pull[0])
            lon.append(pull[1])
        #Insert into the dataframe
        widoh.insert(1, 'Latitude', lat)
        widoh.insert(2, 'Longitude', lon)
    
        #Fix column locations
        lund = widoh.reindex(columns = ['NAME','State','GEOID','Latitude','Longitude','POSITIVE','DEATHS'])
        #Change column names
        nylund = lund.rename(columns = {'NAME': 'County', 'GEOID':'fips', 'POSITIVE':'Confirmed Cases', 'DEATHS':'Deaths'})
        nylund = nylund.fillna(0)
        
        
        if nylund.at[0,'County'] == 'Sauk':
            
            nylund.to_csv('COVID-19_cases_widoh.csv', index = False, header = True)
            counter += 1
            print("Wisconsin scraper is complete.")
        
        else:
            print(cl("ERROR: Must fix Wisconsin scraper.", 'red'))
            
    except Exception:
        print(cl('Printed or exception raised for WI scraper.', 'green'))
        pass
    
def wvScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        wvWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_West_Virginia'
        wvClient = req(wvWiki)
        site_parse = soup(wvClient.read(), "lxml")
        wvClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "mw-parser-output"}).find_all('tbody')
        
        wv = "WEST VIRGINIA"
        
        #CSV file name and header
        csvfile = "COVID-19_cases_wvWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull:
                    take = p.get_text()
                    hold.append(take)
        
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if hold[141].split('\n')[1] == 'Barbour' and hold[195].split('\n')[1] == 'Wyoming':
        
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[141:196]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + "," + wv, key='')
                file.write(take[1] + "," + wv + "," + str(fips.get_county_fips(take[1],state=wv)).strip() + ","
                           + str(locale.latlng).strip('[]') + ","
                           + take[3] + "," + take[5].split('[')[0] + "\n")
                #sleep(1)
            
            file.close()
            
            counter += 1
            print("West Virginia scraper is complete.")
        else:
            print(cl("ERROR: Must fix West Virginia scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for WV scraper.', 'green'))
        pass

def wyScrape():
    
    try:
        #Grab and hold the information from the html inside of site_parse (making sure
        #to close the request from the page)
        wyWiki = 'https://en.wikipedia.org/wiki/2020_coronavirus_pandemic_in_Wyoming'
        wyClient = req(wyWiki)
        site_parse = soup(wyClient.read(), "lxml")
        wyClient.close()
        
        #Narrow down the parse to the section that is most pertinent 
        tables = site_parse.find("div", {"class": "tp-container"}).findAll('tbody')        
        
        wy = "WYOMING"
        co = ' County'
        
        #CSV file name and header
        csvfile = "COVID-19_cases_wyWiki.csv"
        headers = "County,State,fips,Latitude,Longitude,Confirmed Cases,Deaths,Recoveries\n"
        
        #Hold all of the table's information into an easy to dissect list
        hold = []
        for t in tables:
                pull = t.findAll('tr')
                for p in pull[2:]:
                    take = p.get_text()
                    hold.append(take)
    
        #Check to ensure the parsed and collected information is correct/ pertient.
        #If it is, then print to the CSV file whose name was created earlier
        #If not, then print out an error message so that the scraper can be mended
        if (hold[0].split('\n')[1]) == 'Albany' and (hold[-3].split('\n')[1]) == 'Weston':
                    
            file = open(csvfile, "w")
            file.write(headers)
            
            for h in hold[0:-2]:
                take = h.split('\n')
                locale = geocoder.opencage(take[1] + co + "," + wy, key='')
                file.write(take[1] + "," + wy + "," 
                           + str(fips.get_county_fips(take[1],state=wy)).strip() + ","
                           + str(locale.latlng).strip('[]') + "," 
                           + take[3].strip() + ","
                           + take[5].strip() + ","
                           + take[7].strip() + "\n")
            
            file.close()
        
            counter += 1
            print("Wyoming scraper is complete.")
        else:
            print(cl("ERROR: Must fix Wyoming scraper.", 'red'))

    except Exception:
        print(cl('Printed or exception raised for WY scraper.', 'green'))
        pass

def main():
    
    path = ""
    os.chdir(path)
    
    #Runs this on a 24 hour basis... Just comment out if running manually
    while True:
        
        akScrape()
        alScrape()
        arScrape()
        aSamScrape()
        azScrape()
        caScrape()
        coScrape()
        ctScrape()
        dcScrape()
        deScrape()
        flScrape()
        gaScrape()
        guScrape()
        hiScrape()
        idScrape()
        ilScrape()
        inScrape()
        ioScrape()
        kaScrape()
        kyScrape()
        laScrape()
        maScrape()
        mdScrape()
        meScrape()
        miScrape()
        mnScrape()
        moScrape()
        mpScrape()
        msScrape()
        mtScrape()
        ncScrape()
        ndScrape()
        neScrape()
        nhScrape()
        njScrape()
        nmScrape()
        nvScrape()
        nyScrape()
        ohScrape()
        okScrape()
        orScrape()
        paScrape()
        prScrape()
        riScrape()
        scScrape()
        sdScrape()
        tnScrape()
        txScrape()
        utScrape()
        vaScrape()
        viScrape()
        vtScrape()
        waScrape()
        wiScrape()
        wvScrape()
        wyScrape()
        
        if counter == 56:
            
            csvFile = "csv"
            
            alles_COVID = []
            
            alles_COVID = [i for i in glob.glob('COVID-19_*.{}'.format(csvFile))]
            
            hold = []
            
            for i in alles_COVID:
                reader = list(csv.reader(open(i)))
                hold.append(reader)
            
            
            headers = ['County', 'State', 'fips', 'Latitude', 'Longitude', 
                       'Confirmed Cases', 'Deaths', 'Recoveries', 'Released from Isolation',
                       'Hospitalized']
            
            f = open("combined.csv","w")
            writer = csv.writer(f)
            writer.writerow(headers)
            
            for col in hold:
                writer.writerows(col[1:])
        
            f.close()
        else:
            print(cl('Not all scrapers compiled properly. Please fix and run again.', 'red'))
        
        #24 hours in seconds
        sleep(86400)
    
if __name__ == "__main__":
    main()
