import streamlit as st
import pandas as pd
from database import DatabaseManager
from scraper import ZDFheuteScraper

# Layout-Konfiguration
st.set_page_config(page_title="ZDFheute | WhatsApp Artikel-Checker", layout="wide")

st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: #ffffff; }
    h1 { color: #ffffff; font-size: 2rem; }
    .stButton>button { background-color: #ff8c00; color: white; border: none; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("# ZDFheute 🧡 ZDF Digital | WhatsApp Artikel-Checker")
st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    uploaded_file = st.file_uploader("Hier Piano-Excel-Datei hochladen (XLSX)", type=["xlsx"])
with col2:
    start_date = st.date_input("Startdatum")
with col3:
    end_date = st.date_input("Enddatum")

if uploaded_file is not None:
    # Excel einlesen und Spaltennamen bereinigen
    df_excel = pd.read_excel(uploaded_file)
    df_excel.columns = df_excel.columns.str.strip()
    
    if st.button("Artikel abgleichen"):
        with st.spinner("Scrape und Abgleich läuft..."):
            # Scraper ausführen
            ZDFheuteScraper().fetch_and_store(max_clicks=5)
            
            # Daten aus DB laden und Spalten sicher benennen
            db_data = DatabaseManager().get_all_articles()
            db_articles = pd.DataFrame(db_data)
            
            # WICHTIG: Hier erzwingen wir die Spaltennamen, damit der Key 'url' existiert
            if not db_articles.empty:
                db_articles.columns = ['title', 'url', 'category']
                
                # Prüfung: Existiert 'URL' in Excel?
                if 'URL' in df_excel.columns:
                    # Abgleich der URLs
                    missing = db_articles[~db_articles['url'].isin(df_excel['URL'])]
                    
                    st.subheader("Fehlende Artikel auf WhatsApp:")
                    if not missing.empty:
                        st.dataframe(missing[['title', 'url']], use_container_width=True)
                    else:
                        st.success("Alle Artikel sind bereits auf WhatsApp vorhanden!")
                else:
                    st.error(f"Fehler: Spalte 'URL' nicht in Excel gefunden. Gefunden: {list(df_excel.columns)}")
            else:
                st.warning("Keine Artikel in der Datenbank gefunden.")

st.markdown("---")
st.markdown("###### Du hast Feedback oder dir ist etwas aufgefallen? 🧡")
st.markdown("Schreibe oder schicke deine Anmerkungen jederzeit direkt an **Matthias Schmickl**.")
