from flask import Flask, render_template
import sqlite3
#import scraper
app = Flask(__name__)

@app.route('/')
def index():
    # Connect to SQLite database
    conn = sqlite3.connect('sreality.db')
    cursor = conn.cursor()
    
    # Retrieve data from the database
    cursor.execute('SELECT title, image_url FROM sreality_ads LIMIT 500')
    ads = cursor.fetchall()
    
    # Close the connection
    conn.close()

    return render_template('index.html', ads=ads)

if __name__ == '__main__':
       app.run(debug=True, host='0.0.0.0' ,port='8080')
