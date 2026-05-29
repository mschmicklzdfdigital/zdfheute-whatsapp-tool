import streamlit as st
from database import DatabaseManager
from scraper import ZDFheuteScraper

# Konfiguration
st.set_page_config(page_title="ZDFheute WhatsApp Hub", layout="wide")
db = DatabaseManager()

st.title("ZDFheute | WhatsApp Artikel-Hub")
st.markdown("Willkommen! Hier sehen alle Kollegen den aktuellen Stand der publizierten Artikel.")

# Funktion, um den Scraper manuell anzustoßen (nur für Admins)
if st.button("Aktuelle Artikel von ZDFheute abrufen"):
    with st.spinner("Scraper läuft... bitte einen Moment Geduld."):
        scraper = ZDFheuteScraper()
        scraper.fetch_and_store(max_clicks=10)
        st.success("Daten wurden erfolgreich aktualisiert!")

# Daten anzeigen
st.subheader("Aktuelle Artikel-Datenbank")
articles = db.get_all_articles()

if articles:
    # Einfache Anzeige als Tabelle
    import pandas as pd
    df = pd.DataFrame(articles)
    st.dataframe(df, use_container_width=True)
else:
    st.info("Noch keine Daten gefunden. Bitte klicke auf den Button oben.")

# Footer mit deinem gewünschten Design
st.markdown("---")
st.markdown("Fragen oder Feedback? Schreibe direkt an **Matthias Schmickl**.")