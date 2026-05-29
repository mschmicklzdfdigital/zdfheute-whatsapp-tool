from scraper import ZDFheuteScraper

def run_automated_task():
    print("Starte automatisiertes Scraping...")
    scraper = ZDFheuteScraper()
    scraper.fetch_and_store(max_clicks=15)
    print("Scraping erfolgreich beendet.")

if __name__ == "__main__":
    run_automated_task()
