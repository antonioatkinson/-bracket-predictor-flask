from flask import Flask
import flask
from flask import request
from kenpom import kenpom_rankings
from sagarin import sagarin_rankings
from bpi import bpi_rankings
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

    if request.method == 'POST':
        if 'search' in request.form:
            text = request.form["search"]
            text2 = request.form["search2"]
            cur.execute("select * from input_data WHERE name=%s", [text])
            data = cur.fetchone()
            cur.execute("select * from input_data WHERE name=%s", [text2])
            print(cur.fetchone())

            context["team"] = data[0]
            context["seed"] = data[1]
            context["bpi"] = data[5]
            context["bpirank"] = data[6]
            context["kenpom"] = data[7]
            context["kenpomrank"] = data[8]
            context["sagarin"] = data[9]
            context["sagarinrank"] = data[10]
            print("Searching...", text)
        if 'update-data' in request.form:
            kenpom_rankings()
            sagarin_rankings()
            bpi_rankings()
            print("Updating...")


    return flask.render_template("hello.html", **context)


if __name__ == '__main__':
    app.run()
