import requests
from bs4 import BeautifulSoup
import sqlite3
import re

def scrape_and_save():
    url = 'https://www.sreality.cz/api/cs/v2/estates?category_main_cb=1&category_type_cb=1&page=0&per_page=500'
    #url='https://www.sreality.cz/hledani/prodej/domy?region=Praha&vzdalenost=0.5'

    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the JSON response
    response_json = response.json()
    estates = response_json.get('_embedded', {}).get('estates', [])

    # Connect to SQLite database
    conn = sqlite3.connect('sreality.db')
    cursor = conn.cursor()

    # Create a table if it doesn't exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS sreality_ads
                        (id INTEGER PRIMARY KEY AUTOINCREMENT,
                         title TEXT,
                         image_url TEXT)''')
    conn.commit()

    # Extract title and image URL and insert into the database
    for flat in estates:
        title = re.sub(r'\s', ' ', flat.get('name'))
        image_url = flat.get('_links', {}).get('images', [{}])[0].get('href')

        # Store data in the SQLite database
        cursor.execute('INSERT INTO sreality_ads (title, image_url) VALUES (?, ?)', (title, image_url))
        conn.commit()

    # Close the database connection
    conn.close()

if __name__ == "__main__":
    scrape_and_save()
