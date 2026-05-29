import streamlit as st
import pandas as pd
from database import DatabaseManager
from scraper import ZDFheuteScraper

# 1. Page Config
st.set_page_config(page_title="ZDFheute | WhatsApp Artikel-Checker", layout="wide")

# 2. Custom CSS für das "Dunkle Design" und Abstände
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stApp { color: #ffffff; }
    /* Weniger Platz vor dem Footer */
    .block-container { padding-bottom: 1rem; }
    div[data-testid="stMarkdownContainer"] { margin-bottom: 0px; }
    </style>
    """, unsafe_allow_html=True)

# 3. Header
st.markdown("# ZDFheute 🧡 ZDF Digital | WhatsApp Artikel-Checker")
st.markdown("---")

# 4. Input Bereich
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    uploaded_file = st.file_uploader("Hier Piano-Excel-Datei hochladen", type=["xlsx"])
with col2:
    start_date = st.date_input("Startdatum")
with col3:
    end_date = st.date_input("Enddatum")

st.info("💡 Du weißt nicht, wie du die erforderliche Excel-Datei bekommst? Hier gibt's die Anleitung zum Download.")

# 5. Erklärungskasten (Dein Text)
st.markdown("""
<div style="background-color: #161a22; padding: 20px; border-radius: 10px; border: 1px solid #333;">
Dieses Tool gleicht ab, welche Web/App-Artikel von ZDFheute bereits auf dem WhatsApp-Kanal erschienen sind.
<br><br>
<b>• Macht und Folgen:</b> Politik, Analysen & internationale Themen.<br>
<b>• Gut zu wissen:</b> Service, Ratgeber & Wetter.<br>
<b>• Zwischen Tat und Aufklärung:</b> True Crime.<br>
<b>• Trends, Pop & Kurioses:</b> Popkultur & Social Media.<br>
<b>• Sonstige Artikel:</b> Alles weitere.
</div>
""", unsafe_allow_html=True)

# 6. Action Button
if st.button("Artikel abgleichen"):
    with st.spinner("Scrape läuft..."):
        ZDFheuteScraper().fetch_and_store(max_clicks=5)
        st.success("Abgleich erfolgreich!")

# 7. Feedback Footer (Kompakter)
st.markdown("---")
st.markdown("###### Du hast Feedback oder dir ist etwas aufgefallen? 🧡")
st.markdown("Schreibe oder schicke deine Anmerkungen jederzeit direkt an **Matthias Schmickl**.")
