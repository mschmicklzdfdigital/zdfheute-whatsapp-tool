from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from database import DatabaseManager
import time

class ZDFheuteScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        # Dieser Pfad ist der Standard-Speicherort für Chromium in der Streamlit-Cloud
        options.binary_location = "/usr/bin/chromium" 
        
        # Initialisierung ohne webdriver-manager, da Chromium systemweit vorinstalliert ist
        self.driver = webdriver.Chrome(options=options)
        self.db = DatabaseManager()

    def fetch_and_store(self, max_clicks=5):
        try:
            self.driver.get("https://www.zdfheute.de/suche?q=*&type=article")
            wait = WebDriverWait(self.driver, 10)
            
            for _ in range(max_clicks):
                try:
                    # Suche den "Mehr laden"-Button
                    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button-load-more")))
                    btn.click()
                    time.sleep(2)
                except Exception:
                    break # Button nicht mehr gefunden, Ende des Scrappings
            
            # Daten extrahieren
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div.teaser-standard__body")
            articles = []
            for el in elements:
                try:
                    title = el.find_element(By.TAG_NAME, "h3").text
                    url = el.find_element(By.TAG_NAME, "a").get_attribute("href")
                    articles.append({'title': title, 'url': url, 'category': 'Sonstige'})
                except:
                    continue
            
            # In DB speichern
            if articles:
                self.db.add_articles(articles)
                
        finally:
            self.driver.quit()
