from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from database import DatabaseManager
import time

class ZDFheuteScraper:
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        # Automatischer Setup des Treibers
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.db = DatabaseManager()
        self.base_url = "https://www.zdfheute.de/suche?q=*&type=article"

    def fetch_and_store(self, max_clicks=15):
        self.driver.get(self.base_url)
        wait = WebDriverWait(self.driver, 10)
        
        for i in range(max_clicks):
            try:
                # Klicke den Button, um die Suche zu erweitern
                load_more = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button-load-more")))
                load_more.click()
                time.sleep(2)
            except Exception:
                break 
        
        # Daten extrahieren
        elements = self.driver.find_elements(By.CSS_SELECTOR, "div.teaser-standard__body")
        articles = []
        for el in elements:
            try:
                title = el.find_element(By.TAG_NAME, "h3").text
                url = el.find_element(By.TAG_NAME, "a").get_attribute("href")
                # Einfache Kategorisierung direkt hier beim Scrapen
                category = "Sonstige Artikel" # Hier könnte man deine Logik einbauen
                articles.append({'title': title, 'url': url, 'category': category})
            except: continue
            
        # Direkt in die Datenbank schreiben
        if articles:
            self.db.add_articles(articles)
            
        self.driver.quit()
        print(f"Scraping abgeschlossen: {len(articles)} Artikel verarbeitet.")