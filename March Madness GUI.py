from flask import Flask
import flask
from kenpom import kenpom_rankings
from sagarin import sagarin_rankings
import psycopg2 as p
import urllib
from bs4 import BeautifulSoup
from secrets import dbname
from secrets import username
from secrets import password
from secrets import host
from secrets import port


app = Flask(__name__)


@app.route('/')
def hello_world():
    context = {}
    context["data"] = []

    # con = p.connect("dbname=" + dbname +" user=" + username + " password=" + password + " host=" + host + " port=" + port)
    con = p.connect("dbname=demo user='postgres' password='' host='localhost' port=5433")
    cur = con.cursor()
    cur.execute("select * from test_table")
    rows = cur.fetchall()

    i = 1
    N = 15
    # BPI rankings
    while i < N:
        # url = "http://www.espn.com/mens-college-basketball/bpi/_/season/2012/view/overview"
        url = "http://www.espn.com/mens-college-basketball/bpi/_/view/bpi/season/2012/page/"+str(i)
        i+=1
        page = urllib.request.urlopen(url).read()

        soup = BeautifulSoup(page, 'html.parser')

        # # Grab all the table rows and put it into a list
        for row in soup.find_all("tr")[2:]:
            names = row.find_all("span")
            team_data = row.find_all("td")
            del team_data[1]

            bpi_rank = team_data[0].get_text()
            bpi_rating = team_data[-2].get_text()
            team_name = names[1].get_text()

            print("name", names[1].get_text())
            print("bpi ranking", bpi_rank)
            print("bpi rating", bpi_rating)
            print("")

            cur.execute("UPDATE input_data SET bpi=%s, bpirank=%s WHERE name=%s",
                    [float(bpi_rating), int(bpi_rank), team_name])


        con.commit()

    return flask.render_template("hello.html", **context)


if __name__ == '__main__':
    app.run()
