import streamlit as st
import pandas as pd
from database import DatabaseManager
from scraper import ZDFheuteScraper

st.set_page_config(page_title="ZDFheute | WhatsApp Artikel-Checker", layout="wide")

st.markdown("""<style>.block-container { padding-bottom: 1rem; }</style>""", unsafe_allow_html=True)

st.markdown("# ZDFheute 🧡 ZDF Digital | WhatsApp Artikel-Checker")
st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    uploaded_file = st.file_uploader("Hier Piano-Excel-Datei hochladen", type=["xlsx"])
with col2:
    start_date = st.date_input("Startdatum")
with col3:
    end_date = st.date_input("Enddatum")

if st.button("Artikel abgleichen"):
    if uploaded_file is None:
        st.warning("Bitte lade erst eine Excel-Datei hoch!")
    else:
        # 1. Scraper starten
        with st.spinner("Aktuelle Web-Artikel werden geladen..."):
            ZDFheuteScraper().fetch_and_store(max_clicks=5)
            
        # 2. Daten laden
        df_excel = pd.read_excel(uploaded_file)
        db_articles = pd.DataFrame(DatabaseManager().get_all_articles())
        
        # 3. Logik: Fehlende Artikel finden
        # Wir schauen: Welche URL aus der DB ist NICHT in der Excel-Liste?
        if 'URL' in df_excel.columns and 'url' in db_articles.columns:
            missing_articles = db_articles[~db_articles['url'].isin(df_excel['URL'])]
            
            st.success("Abgleich beendet!")
            st.subheader("Diese Artikel fehlen noch auf WhatsApp:")
            st.dataframe(missing_articles, use_container_width=True)
        else:
            st.error("Fehler: Die Excel-Datei muss eine Spalte namens 'URL' enthalten.")

st.markdown("---")
st.markdown("###### Du hast Feedback oder dir ist etwas aufgefallen? 🧡")
st.markdown("Schreibe oder schicke deine Anmerkungen jederzeit direkt an **Matthias Schmickl**.")
