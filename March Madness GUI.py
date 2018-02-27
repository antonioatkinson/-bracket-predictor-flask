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
    #context = {}
    context = kenpom_rankings()
    sagarin_rankings()

    return flask.render_template("hello.html", **context)


if __name__ == '__main__':
    app.run()
