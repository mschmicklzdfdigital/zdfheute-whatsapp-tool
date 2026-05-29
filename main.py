import streamlit as st
import pandas as pd
from database import DatabaseManager
from scraper import ZDFheuteScraper

# Layout
st.set_page_config(page_title="ZDFheute | WhatsApp Artikel-Checker", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    .stButton>button { background-color: #ff8c00; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("# ZDFheute 🧡 ZDF Digital | WhatsApp Artikel-Checker")
st.markdown("---")

# 1. Scraper Button (Separater Bereich)
st.subheader("1. Web-Daten aktualisieren")
if st.button("Jetzt ZDFheute scannen"):
    with st.spinner("Scrape läuft... das kann einen Moment dauern..."):
        ZDFheuteScraper().fetch_and_store(max_clicks=5)
        st.success("Datenbank erfolgreich aktualisiert!")

st.markdown("---")

# 2. Upload und Vergleich
st.subheader("2. Excel-Abgleich")
uploaded_file = st.file_uploader("Piano-Excel-Datei hochladen", type=["xlsx"])

if uploaded_file is not None:
    df_excel = pd.read_excel(uploaded_file)
    df_excel.columns = df_excel.columns.str.strip()
    
    if st.button("Abgleich starten"):
        db_data = DatabaseManager().get_all_articles()
        db_articles = pd.DataFrame(db_data)
        
        if not db_articles.empty:
            db_articles.columns = ['title', 'url', 'category']
            
            if 'URL' in df_excel.columns:
                missing = db_articles[~db_articles['url'].isin(df_excel['URL'])]
                st.subheader("Diese Artikel fehlen auf WhatsApp:")
                if not missing.empty:
                    st.dataframe(missing[['title', 'url']], use_container_width=True)
                else:
                    st.success("Alle aktuellen Web-Artikel sind bereits in der Liste vorhanden!")
            else:
                st.error(f"Fehler: Spalte 'URL' nicht gefunden. Gefunden: {list(df_excel.columns)}")
        else:
            st.warning("Die Datenbank ist noch leer! Klicke oben auf 'Jetzt ZDFheute scannen'.")

st.markdown("---")
st.markdown("###### Du hast Feedback? Schreibe direkt an Matthias Schmickl.")
