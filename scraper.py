from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ZDFheuteScraper:
    def __init__(self):
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.binary_location = "/usr/bin/chromium" 
        self.driver = webdriver.Chrome(options=options)

    def fetch_articles(self):
        articles = []
        try:
            self.driver.get("https://www.zdfheute.de/suche?q=*&type=article")
            wait = WebDriverWait(self.driver, 10)
            
            # Klicke 3 Mal auf "Mehr laden"
            for _ in range(3):
                try:
                    btn = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.button-load-more")))
                    btn.click()
                    time.sleep(2)
                except: break
            
            elements = self.driver.find_elements(By.CSS_SELECTOR, "div.teaser-standard__body")
            for el in elements:
                try:
                    title = el.find_element(By.TAG_NAME, "h3").text
                    url = el.find_element(By.TAG_NAME, "a").get_attribute("href")
                    articles.append({'title': title, 'URL': url}) # Spalte heißt jetzt 'URL'
                except: continue
        finally:
            self.driver.quit()
        return articles
