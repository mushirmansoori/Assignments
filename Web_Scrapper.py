import requests
from bs4 import BeautifulSoup
import csv
import datetime
import sqlite3

def scrape_verge():
    url = 'https://www.theverge.com/'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    articles = soup.find_all('div', {'class': 'c-entry-box--compact__body'})

    data = []
    for article in articles:
        headline = article.h2.a.text.strip()
        url = article.h2.a['href']
        author = article.find('span', {'class': 'c-byline__item'}).a.text
        date = article.find('time')['datetime'][:10]
        data.append([url, headline, author, date])
    
    return data

def save_csv(data):
    today = datetime.date.today().strftime('%d%m%Y')
    filename = today + '_verge.csv'

    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['id', 'URL', 'headline', 'author', 'date'])
        for i, d in enumerate(data):
            writer.writerow([i, d[0], d[1], d[2], d[3]])

def save_db(data):
    conn = sqlite3.connect('verge_articles.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS articles
                 (id INTEGER PRIMARY KEY, url TEXT, headline TEXT, author TEXT, date TEXT)''')

    # Check if the table is empty
    c.execute('''SELECT count(*) FROM articles''')
    count = c.fetchone()[0]

    # Read the data and insert new data into the table
    if count == 0:
        for i, d in enumerate(data):
            c.execute("INSERT INTO articles (id, url, headline, author, date) VALUES (?, ?, ?, ?, ?)",
                      (i, d[0], d[1], d[2], d[3]))
    else:
        for d in data:
            c.execute("SELECT count(*) FROM articles WHERE url=?", (d[0],))
            exists = c.fetchone()[0]
            if not exists:
                c.execute("INSERT INTO articles (id, url, headline, author, date) VALUES (?, ?, ?, ?, ?)",
                          (count, d[0], d[1], d[2], d[3]))
                count += 1

    conn.commit()
    conn.close()

if __name__ == '__main__':
    data = scrape_verge()
    save_csv(data)
    save_db(data)
