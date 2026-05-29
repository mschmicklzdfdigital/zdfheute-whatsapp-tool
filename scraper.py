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
        options.binary_location = "/usr/bin/chromium" 
        self.driver = webdriver.Chrome(options=options)
        self.db = DatabaseManager()

    def fetch_and_store(self, max_clicks=2):
        try:
            self.driver.get("https://www.zdfheute.de/suche?q=*&type=article")
            time.sleep(5) # Wartezeit erhöhen
            
            # Suche nach den Teaser-Elementen
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div.teaser-standard__body")
            
            # WICHTIG: Wenn elements leer ist, drucke etwas in das Log
            print(f"Gefundene Elemente: {len(elements)}")
            
            articles = []
            for el in elements:
                try:
                    title = el.find_element(By.TAG_NAME, "h3").text
                    url = el.find_element(By.TAG_NAME, "a").get_attribute("href")
                    articles.append({'title': title, 'url': url, 'category': 'Sonstige'})
                except: continue
            
            if articles:
                self.db.add_articles(articles)
        finally:
            self.driver.quit()
