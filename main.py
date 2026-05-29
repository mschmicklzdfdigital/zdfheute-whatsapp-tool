import streamlit as st
import pandas as pd
from database import DatabaseManager
from scraper import ZDFheuteScraper

st.set_page_config(page_title="ZDFheute | WhatsApp Artikel-Checker", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("# ZDFheute 🧡 ZDF Digital | WhatsApp Artikel-Checker")
st.markdown("---")

col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    uploaded_file = st.file_uploader("Hier Piano-Excel-Datei hochladen", type=["xlsx"])
with col2:
    start_date = st.date_input("Startdatum")
with col3:
    end_date = st.date_input("Enddatum")

if uploaded_file is not None:
    df_excel = pd.read_excel(uploaded_file)
    st.write(f"✅ Datei geladen: {len(df_excel)} Zeilen erkannt.")

st.info("💡 Du weißt nicht, wie du die erforderliche Excel-Datei bekommst? Hier gibt's die Anleitung zum Download.")

if st.button("Artikel abgleichen"):
    if uploaded_file is None:
        st.warning("Bitte lade erst eine Excel-Datei hoch!")
    else:
        with st.spinner("Scrape läuft..."):
            ZDFheuteScraper().fetch_and_store(max_clicks=5)
            st.success("Abgleich erfolgreich!")

st.markdown("---")
st.markdown("###### Du hast Feedback oder dir ist etwas aufgefallen? 🧡")
st.markdown("Schreibe oder schicke deine Anmerkungen jederzeit direkt an **Matthias Schmickl**.")
