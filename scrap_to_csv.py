import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from geopy.geocoders import Nominatim
from geopy import distance
# import folium

class scrap_to_csv:
    def __init__(self, departement, jour, heure):
        self.departement = departement
        self.jour = jour
        self.heure = heure
        self.fichier_lat_long_par_spot = pd.read_csv('lat_long_spots.csv', index_col=False)

    def scrapper(self):
        response = requests.get("https://www.surf-sentinel.com/spots-de-surf/france/liste-spots-de-surf-" + self.departement)
        soup = BeautifulSoup(response.content, "html.parser")

        communes = []
        spots = []

        for i in soup.find_all("div", class_="location-content") :
            url = str(i.find("div").find("a"))
            commune_avec_slash = str(re.search(self.departement + "/[\w-]+", url).group(0)).replace(self.departement,'')
            spot_url = str(re.search(self.departement + "/[\w-]+/[\w-]+", url).group(0)).replace(commune_avec_slash,'').replace(self.departement,'').replace("/","")
            commune_url = commune_avec_slash.replace('/','')

            communes.append(commune_url)

            if spot_url == '' :
                spots.append(commune_url)
            else :
                spots.append(spot_url)

        spots_main_data = pd.DataFrame()
        spots_main_data['commune'] = communes
        spots_main_data['spot'] = spots
        spots_main_data['full_name'] = spots_main_data['commune'] + ' ' + spots_main_data['spot']
        spots_main_data['url'] = 'https://www.surf-sentinel.com/surf-report/france/' + self.departement + '/' + spots_main_data['commune'] + '/' + spots_main_data['spot']

        url = []
        date = []
        hour = []
        water_quality = []
        conditions = []
        level = []
        hauteur = []
        note = []

        for spot_url in spots_main_data['url'] :
            meteo_spot_web_page = requests.get(spot_url)
            soup_url = BeautifulSoup(meteo_spot_web_page.content, "html.parser")

            for i in soup_url.find_all("div", class_="detailed-report-box hidden gocenter") :
                datetime = str(re.search("box-\d+-\d+-\d+-\d+", str(i)).group(0)).replace('box-','')
                url.append(spot_url)
                date.append(datetime[0:10])
                hour.append(datetime[11:].replace('0',''))

                water_quality_desc = str(re.search("strong>\w<span", str(i)).group(0)).replace('strong>','').replace('<span','')
                water_quality.append(water_quality_desc)
                level_desc = str(re.search("""metric">\d</span""", str(i)).group(0)).replace('metric">','').replace('</span','')
                level.append(level_desc)

                if water_quality_desc == 'A' and level_desc == '3' :
                    note.append(1)
                elif water_quality_desc == 'A' and level_desc == '2' :
                    note.append(2)
                elif water_quality_desc == 'B' and level_desc == '3' :
                    note.append(3)
                elif water_quality_desc == 'B' and level_desc == '2' :
                    note.append(4)
                elif water_quality_desc == 'C' and level_desc == '3' :
                    note.append(5)
                elif water_quality_desc == 'C' and level_desc == '2' :
                    note.append(6)
                elif water_quality_desc == 'A' and level_desc == '1' :
                    note.append(7)
                elif water_quality_desc == 'B' and level_desc == '1' :
                    note.append(8)
                elif water_quality_desc == 'C' and level_desc == '1' :
                    note.append(9)
                else :
                    note.append(10)

            for i in soup_url.find_all("p", class_="fl-caps previ-desc") :
                try :
                    conditions = str(re.search("conditions [a-z]+", str(i)).group(0)).replace('conditions ','')
                except :
                    hauteur = str(re.search("\d.\d m en", str(i)).group(0)).replace(' m en','')

        spot_attributes = pd.DataFrame()
        spot_attributes['url'] = url
        spot_attributes['date'] = date
        spot_attributes['hour'] = hour
        spot_attributes['water_quality'] = water_quality
        spot_attributes['conditions'] = conditions
        spot_attributes['level'] = level
        spot_attributes['hauteur'] = hauteur
        spot_attributes['note'] = note

        spots_previsions = pd.merge(left=spots_main_data, right=spot_attributes, on = 'url', how='left')
        spots_previsions = pd.merge(left=spots_previsions, right=self.fichier_lat_long_par_spot, on = 'full_name', how='left')

        if self.jour :
            if self.heure :
                top_spots = spots_previsions[(spots_previsions.date == self.jour)][(spots_previsions.hour == self.heure)].sort_values(by=['note']).head(10)
            else :
                top_spots = spots_previsions[(spots_previsions.date == self.jour)].sort_values(by=['note']).head(10)
        else :
            if self.heure :
                top_spots = spots_previsions[(spots_previsions.hour == self.heure)].sort_values(by=['note']).head(10)
            else :
                top_spots = spots_previsions.sort_values(by=['note']).head(10)

        top_spots.to_csv("top_spots.txt")
