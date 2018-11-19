from flask import Flask
import flask
from flask import request
from kenpom import kenpom_rankings
from sagarin import sagarin_rankings
from bpi import bpi_rankings
from get_bracket_matchups import inital_opponents
import psycopg2 as p
import urllib
from bs4 import BeautifulSoup
from secrets import dbname
from secrets import username
from secrets import password
from secrets import host
from secrets import port


app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def hello_world():
    con = p.connect("dbname=demo user='postgres' password='' host='localhost' port=5433")
    cur = con.cursor()
    context = {}
    beginning_year = 2008
    end_year = 2018

    if request.method == 'POST':
        if 'search' in request.form:
            text = request.form["search"]
            text2 = request.form["search2"]
            cur.execute("select * from input_data WHERE name=%s AND cur_year=2018", [text])
            data = cur.fetchone()
            print(text)
            print(data)
            print(text2)
            cur.execute("select * from input_data WHERE name=%s AND cur_year=2018", [text2])
            data2 = cur.fetchone()
            print(data2)
            # print(cur.fetchone())

            cur.execute("select * from input_data WHERE seed>0")
            context["tourney_teams"] = cur.fetchall()

            context["team"] = data[0]
            context["seed"] = data[1]
            context["bpi"] = data[5]
            context["bpirank"] = data[6]
            context["kenpom"] = data[7]
            context["kenpomrank"] = data[8]
            context["sagarin"] = data[9]
            context["sagarinrank"] = data[10]

            context["weighed_score"] = float(4 * context["sagarin"] + 3 * context["kenpom"] + 2 * context["bpi"]) / 9

            # Return if no input for second box
            if data2 == None:
                return flask.render_template("hello.html", **context)

            context["team2"] = data2[0]
            context["seed2"] = data2[1]
            context["bpi2"] = data2[5]
            context["bpirank2"] = data2[6]
            context["kenpom2"] = data2[7]
            context["kenpomrank2"] = data2[8]
            context["sagarin2"] = data2[9]
            context["sagarinrank2"] = data2[10]

            context["weighed_score2"] = float(4 * context["sagarin2"] + 3 * context["kenpom2"] + 2 * context["bpi2"]) / 9

            print("Searching...", text)
        if 'update-data' in request.form:
            print("Updating...")
            # Clears DB table
            # cur.execute("DELETE FROM input_data")
            for year in range(beginning_year, end_year + 1):
                kenpom_rankings(str(year))
                sagarin_rankings(str(year))
                bpi_rankings(str(year))
                inital_opponents(str(year))


            print("Updated!")


    return flask.render_template("hello.html", **context)


if __name__ == '__main__':
    app.run()
