import psycopg2
import csv

conn = psycopg2.connect("host=localhost port=5432 dbname=odscourse user=postgres password=secret")
cursor = conn.cursor()

'''query = """
CREATE TABLE if not EXISTS athlete_events (
    id SERIAL PRIMARY KEY,
    athlete_id INTEGER,
    name VARCHAR,
    sex VARCHAR,
    age INTEGER,
    height INTEGER,
    weight REAL,
    team VARCHAR,
    noc VARCHAR,
    games VARCHAR,
    year INTEGER,
    season VARCHAR,
    city VARCHAR,
    sport VARCHAR,
    event VARCHAR,
    medal VARCHAR
)
"""
cursor.execute(query)
conn.commit()

with open('athlete_events.csv', 'r') as f:
    reader = csv.reader(f)
    # Skip the header row
    next(reader)

    for Id, row in enumerate(reader):
        for i in range(len(row)):
            if row[i] == 'NA':
                if i in (3, 4, 5, 9):
                    row[i] = '0'

        cursor.execute(
            "INSERT INTO athlete_events VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
            [Id] + row)
conn.commit()'''
cursor.execute("SELECT * FROM athlete_events LIMIT 5")
records = cursor.fetchall()
print(records)