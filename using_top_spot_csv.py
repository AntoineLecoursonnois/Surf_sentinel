from scrap_to_csv import scrapper_to_csv
import pandas as pd

csv_scrapped = scrapper_to_csv

class top_spots:
    def __init__(self):
        self.jour = jour
        self.heure = heure
        self.previsions = pd.read_csv('spots_previsions.csv', index_col=False)
        self.previsions = csv_scrapped.scrap()


    def final_top_spots(self):
        if self.jour :
            if self.heure :
                top_spots = self.previsions[(self.previsions.date == self.jour)][(self.previsions.hour == self.heure)].sort_values(by=['note']).head(50)
            else :
                top_spots = self.previsions[(self.previsions.date == self.jour)].sort_values(by=['note']).head(50)
        else :
            if self.heure :
                top_spots = self.previsions[(self.previsions.hour == self.heure)].sort_values(by=['note']).head(50)
            else :
                top_spots = self.previsions.sort_values(by=['note']).head(50)

        return top_spots
