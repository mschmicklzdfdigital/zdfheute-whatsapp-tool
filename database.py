import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="zdf_articles.db"):
        self.conn = sqlite3.connect(db_name, check_same_thread=False)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            url TEXT UNIQUE,
            category TEXT,
            timestamp DATETIME
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_articles(self, articles):
        """Fügt eine Liste von Artikeln hinzu, ignoriert Duplikate via URL."""
        query = "INSERT OR IGNORE INTO articles (title, url, category, timestamp) VALUES (?, ?, ?, ?)"
        for a in articles:
            self.conn.execute(query, (a['title'], a['url'], a['category'], datetime.now()))
        self.conn.commit()

    def get_all_articles(self):
        cursor = self.conn.execute("SELECT title, url, category FROM articles ORDER BY id DESC")
        return [{"title": row[0], "url": row[1], "category": row[2]} for row in cursor.fetchall()]