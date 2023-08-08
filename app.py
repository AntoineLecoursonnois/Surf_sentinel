import streamlit as st
import pandas as pd
from datetime import date, timedelta
from scrap_to_csv import scrapper_class

def main():
    # liste des départements disponibles
    departement = st.selectbox("""Dans quel département souhaites tu surfer ? \n""", ['Morbihan', 'Cotes-darmor', 'Finsitere', 'Ille-et-vilaine'])

    # liste des jours de aujourd'hui à J+6
    datelist = [x.date() for x in pd.date_range(date.today(), periods=7).tolist()]
                # if x > (date.today() + timedelta(days=1))]

    # Si l'utilisateur veut surfer un jour en particulier il peut le préciser dans une checkbox
    filter_day = st.checkbox('Je veux surfer un jour en particulier.')

    # Si l'utilisateur veut surfer un jour en particulier il peut le préciser dans une checkbox
    filter_hour = st.checkbox('Je veux surfer à une heure précise.')

    st.write("""S'il est toujours mentionné "RUNNING..." en haut à droite de la page alors merci de patienter le temps de récupérer les informations en temps réel.""")

    if filter_day :
        # Sélectionner le jour en particulier
        jour = st.selectbox("Quel jour souhaites tu surfer ?", datelist)

        if filter_hour :
            # liste des heures
            heure = st.selectbox("""A quelle heure souhaites tu surfer ?\n""", ['6','9','12','15','18','21'])

            # scrapping sur le departement, le jour et l'heure si sélectionnée
            scrap = scrapper_class(departement, heure)
            # Crée un dataframe à partir du scrapping
            top_10_spots = scrap.scrapper_function()

            # Convertie les dates de l'url en format date pour matcher ensuite le souhait de surfer un jour en particulier de l'utilisateur
            top_10_spots['date'] = [x.date() for x in pd.to_datetime(top_10_spots["date"])]
            # On passe le jour sélectionné en colonne pour ensuite faire le match
            top_10_spots['jour'] = jour

            # On filtre le df sur le jour sélectionné
            top_10_spots = top_10_spots[top_10_spots['date'] == top_10_spots['jour']]

            # On montre les résultats
            st.dataframe(top_10_spots[['commune','spot', 'date', 'heure','qualité_des_vagues','level','conditions','hauteur','note','url']].reset_index().drop(columns=['index']))
        else :
            heure = """Je n'ai pas de contrainte de temps"""
            # scrapping sur le departement, le jour et l'heure si sélectionnée
            scrap = scrapper_class(departement, heure)
            # Crée un dataframe à partir du scrapping
            top_10_spots = scrap.scrapper_function()

            # Convertie les dates de l'url en format date pour matcher ensuite le souhait de surfer un jour en particulier de l'utilisateur
            top_10_spots['date'] = [x.date() for x in pd.to_datetime(top_10_spots["date"])]
            # On passe le jour sélectionné en colonne pour ensuite faire le match
            top_10_spots['jour'] = jour

            # On filtre le df sur le jour sélectionné
            top_10_spots = top_10_spots[top_10_spots['date'] == top_10_spots['jour']]

            # On montre les résultats
            st.dataframe(top_10_spots[['commune','spot', 'date', 'heure','qualité_des_vagues','level','conditions','hauteur','note','url']].reset_index().drop(columns=['index']))


            # # On passe le jour sélectionné en colonne pour ensuite faire le match
            # top_10_spots['jour'] = jour

            # top_10_spots = top_10_spots[top_10_spots['date'] == top_10_spots['jour']]
            # st.dataframe(top_10_spots[['commune','spot', 'date', 'heure','qualité_des_vagues','level','conditions','hauteur','note','url']].reset_index().drop(columns=['index']))
    else :
        if filter_hour :
            # liste des heures
            heure = st.selectbox("""A quelle heure souhaites tu surfer ?\n""", ['6','9','12','15','18','21'])

            # scrapping sur le departement, le jour et l'heure si sélectionnée
            scrap = scrapper_class(departement, heure)
            # Crée un dataframe à partir du scrapping
            top_10_spots = scrap.scrapper_function()

            # On montre les résultats
            st.dataframe(top_10_spots[['commune','spot', 'date', 'heure','qualité_des_vagues','level','conditions','hauteur','note','url']].reset_index().drop(columns=['index']))
        else :
            heure = """Je n'ai pas de contrainte de temps"""
            # scrapping sur le departement, le jour et l'heure si sélectionnée
            scrap = scrapper_class(departement, heure)
            # Crée un dataframe à partir du scrapping
            top_10_spots = scrap.scrapper_function()

            # On montre les résultats
            st.dataframe(top_10_spots[['commune','spot', 'date', 'heure','qualité_des_vagues','level','conditions','hauteur','note','url']].reset_index().drop(columns=['index']))


        # st.dataframe(top_10_spots[['commune','spot', 'date', 'heure','qualité_des_vagues','level','conditions','hauteur','note','url']].reset_index().drop(columns=['index']))

if __name__ == '__main__':
    main()
