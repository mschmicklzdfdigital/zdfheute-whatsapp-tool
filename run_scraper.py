import schedule
import time
from scraper import ZDFheuteScraper

def job():
    print("Starte automatisiertes Scraping...")
    scraper = ZDFheuteScraper()
    scraper.fetch_and_store(max_clicks=15)
    print("Scraping beendet.")

# Zeitplan festlegen: Jede Stunde ausführen
schedule.every().hour.do(job)

if __name__ == "__main__":
    job() # Einmal sofort beim Start ausführen
    while True:
        schedule.run_pending()
        time.sleep(60) # Alle Minute prüfen, ob der Job ansteht