from flask import Flask
import flask
import psycopg2 as p
import urllib
from bs4 import BeautifulSoup
from secrets import dbname
from secrets import username
from secrets import password
from secrets import host
from secrets import port

app = Flask(__name__)

def kenpom_rankings():
    context = {}
    context["data"] = []

    # con = p.connect("dbname=" + dbname +" user=" + username + " password=" + password + " host=" + host + " port=" + port)
    con = p.connect("dbname=demo user='postgres' password='' host='localhost' port=5433")
    cur = con.cursor()
    cur.execute("select * from test_table")
    rows = cur.fetchall()

    # Kenpom rankings
    url = "https://kenpom.com/index.php?y=2017"
    # page = html.fromstring(urllib.request.urlopen(url).read())
    page = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(page, 'html.parser')

    # table = soup.find("table", attrs={"class": "details"})
    table = soup.find(id="ratings-table")

    # The first tr contains the field names.
    headings = [th.get_text() for th in table.find("tr").find_all("th")]

    datasets = []
    for row in table.find_all("tr")[1:]:
        # print(row)
        # print(td.get_text() for td in row.find_all("td"))
        data = row.find_all("td")
        temp_arr = []
        for td in data:
            # print(td.get_text())
            temp_arr.append(td.get_text())

        datasets.append(temp_arr)

    datasets[:] = [item for item in datasets if len(item) != 0]
    # print(datasets)
    cur.execute("DELETE FROM input_data")
    for row in datasets:
        rank = row[0]
        seed = ""
        if len(row[1].split()) > 1:
            seed = row[1].split()[-1]
        kenpom_val = row[4]
        # Remove first character (+)
        kenpom_val = kenpom_val[1:]

        try:
            seed = int(seed)
        except:
            seed = 0

        if seed > 0:
            print("Seed", row[1])
            # Remove seed from row
            temp_arr = row[1].split()
            temp_arr.pop(-1)

            # Turn list into string
            temp_arr = ' '.join(temp_arr)
            row[1] = temp_arr
            context["data"].append(str(row[0]) + str(row[1]))
        name = str(row[1])

        # print(name)

        cur.execute("INSERT INTO input_data(name, seed, kenpom, kenpomrank) VALUES (%s, %s, %s, %s)",
                    [name, seed, float(kenpom_val), rank])

    con.commit()

    return context