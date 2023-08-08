from scrap_to_csv import scrapper
import streamlit as st

scrapper = scrapper()

def main():
    departement = st.text_input("""Dans quel département souhaites tu surfer ? \n""")
    jour = st.text_input("""Quel jour souhaites tu surfer (format aaaa-mm-dd) ?\nPour plusieurs journées merci de ne rien indiquer. \n""")
    heure = input("""A quelle heure souhaites tu surfer (6-9-12-15-18-21) ?\nPour plusieurs plages horaires merci de ne rien indiquer. \n""")

    df = scrapper(departement, jour, heure)

    st.write(f"{df}")
