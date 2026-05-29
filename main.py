import streamlit as st
import pandas as pd
from scraper import ZDFheuteScraper

st.set_page_config(page_title="ZDFheute | WhatsApp Artikel-Checker", layout="wide")

st.markdown("""<style>.stApp { background-color: #0e1117; color: #ffffff; } .stButton>button { background-color: #ff8c00; color: white; }</style>""", unsafe_allow_html=True)

st.markdown("# ZDFheute 🧡 ZDF Digital | WhatsApp Artikel-Checker")
st.markdown("---")

uploaded_file = st.file_uploader("Piano-Excel-Datei hochladen", type=["xlsx"])

if uploaded_file and st.button("Abgleich starten"):
    with st.spinner("Scrape läuft, bitte kurz warten..."):
        # Daten vom Scraper
        web_data = ZDFheuteScraper().fetch_articles()
        df_web = pd.DataFrame(web_data)
        
        # Daten vom Excel
        df_excel = pd.read_excel(uploaded_file)
        # Leerzeichen entfernen und Spaltennamen vereinheitlichen
        df_excel.columns = df_excel.columns.str.strip()
        
        if 'URL' in df_excel.columns:
            # Vergleich: Finde alles in df_web, was NICHT in df_excel ist
            missing = df_web[~df_web['URL'].isin(df_excel['URL'])]
            
            st.subheader(f"Gefundene Web-Artikel: {len(df_web)}")
            st.subheader("Diese Artikel fehlen auf WhatsApp:")
            if not missing.empty:
                st.dataframe(missing, use_container_width=True)
            else:
                st.success("Alle Artikel sind bereits auf WhatsApp vorhanden!")
        else:
            st.error(f"Fehler: Deine Excel-Datei muss zwingend eine Spalte namens 'URL' haben. Gefunden: {list(df_excel.columns)}")
