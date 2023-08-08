import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
from datetime import datetime

class scrapper_class:
    def __init__(self, departement, heure):
        self.departement = departement.lower()
        self.heure = heure
        self.fichier_lat_long_par_spot = pd.read_csv('lat_long_spots.csv', index_col=False)

    def scrapper_function(self):
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
        heure = []
        qualité_des_vagues = []
        conditions = []
        level = []
        hauteur = []
        note = []

        for spot_url in spots_main_data['url'] :
            meteo_spot_web_page = requests.get(spot_url)
            soup_url = BeautifulSoup(meteo_spot_web_page.content, "html.parser")

            for i in soup_url.find_all("div", class_="detailed-report-box hidden gocenter") :
                date_url = str(re.search("box-\d+-\d+-\d+-\d+", str(i)).group(0)).replace('box-','')
                url.append(spot_url)
                date.append(date_url[0:10])
                heure.append(date_url[11:].replace('0',''))

                qualité_des_vagues_desc = str(re.search("strong>\w<span", str(i)).group(0)).replace('strong>','').replace('<span','')
                qualité_des_vagues.append(qualité_des_vagues_desc)
                level_desc = str(re.search("""metric">\d</span""", str(i)).group(0)).replace('metric">','').replace('</span','')
                level.append(level_desc)

                if qualité_des_vagues_desc == 'A' and level_desc == '3' :
                    note.append(1)
                elif qualité_des_vagues_desc == 'A' and level_desc == '2' :
                    note.append(2)
                elif qualité_des_vagues_desc == 'B' and level_desc == '3' :
                    note.append(3)
                elif qualité_des_vagues_desc == 'B' and level_desc == '2' :
                    note.append(4)
                elif qualité_des_vagues_desc == 'C' and level_desc == '3' :
                    note.append(5)
                elif qualité_des_vagues_desc == 'C' and level_desc == '2' :
                    note.append(6)
                elif qualité_des_vagues_desc == 'A' and level_desc == '1' :
                    note.append(7)
                elif qualité_des_vagues_desc == 'B' and level_desc == '1' :
                    note.append(8)
                elif qualité_des_vagues_desc == 'C' and level_desc == '1' :
                    note.append(9)
                else :
                    note.append(10)

                conditions_desc = str(re.search("conditions [a-z]+", str(i)).group(0)).replace('conditions ','')
                conditions.append(conditions_desc)

                hauteur_desc = str(re.search("\d.\d m en", str(i)).group(0)).replace(' m en','')
                hauteur.append(hauteur_desc)

        spot_attributes = pd.DataFrame()
        spot_attributes['url'] = url
        spot_attributes['date'] = date
        spot_attributes['heure'] = heure
        spot_attributes['qualité_des_vagues'] = qualité_des_vagues
        spot_attributes['conditions'] = conditions
        spot_attributes['level'] = level
        spot_attributes['hauteur'] = hauteur
        spot_attributes['note'] = note

        spots_previsions = pd.merge(left=spots_main_data, right=spot_attributes, on = 'url', how='left')
        spots_previsions = pd.merge(left=spots_previsions, right=self.fichier_lat_long_par_spot, on = 'full_name', how='left')

        if self.heure != """Je n'ai pas de contrainte de temps""" :
            top_spots = spots_previsions[(spots_previsions.heure == self.heure)].sort_values(by=['note', 'hauteur'], ascending = [True, False]).head(500)
        else :
            top_spots = spots_previsions.sort_values(by=['note', 'hauteur'], ascending = [True, False]).head(500)

        return top_spots

    def communes(self):
        df = self.scrapper_function()
        df = sorted(list(set(df['commune'])))
        return df
