import streamlit as st
import pandas as pd
from datetime import date
from scrap_to_csv import scrapper_class
# from using_top_spot_csv import top_spots

def main():
    # liste des départements disponibles
    departement = st.selectbox("""Dans quel département souhaites tu surfer ? \n""", ['Morbihan', 'Cotes-darmor', 'Finsitere', 'Ille-et-vilaine'])
    # liste des jours de aujourd'hui à J+6
    datelist = pd.date_range(date.today(), periods=7).tolist()
    jour = st.selectbox("Quel jour souhaites tu surfer ?\n", datelist)
    # liste des heures
    heure = st.selectbox("""A quelle heure souhaites tu surfer ?\n""", ["""Je n'ai pas de contrainte de temps""", '6','9','12','15','18','21'])
    # scrapping sur le departement, le jour et l'heure si sélectionnée
    scrap = scrapper_class(departement, jour, heure)
    top_10_spots = scrap.scrapper_function()
    st.dataframe(top_10_spots[['commune','spot','date', 'heure','qualité_des_vagues','level','conditions','hauteur','note','url']])
    # Lien vers la page web d'un des spots
    # st.write("""Si tu souhaites avoir plus d'informations je t'invite à consulter la page Surf Sentinel :""")
    # Quelle commune
    # commune = st.selectbox("""Quelle commune t'intéresse ?""", sorted(list(set(top_10_spots[['commune']]))))
    # st.dataframe(top_10_spots[['commune','spot','url']])

    # Quel spot
    # spot = st.selectbox("Quel spot ? :", sorted(list(set(top_10_spots['spot']))))
    # Génère le lien
    # url = st.dataframe(top_10_spots['url'])
    # st.write("Lien url : [link]({url})")


if __name__ == '__main__':
    main()
