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

def sagarin_rankings(year):
    context = {}
    context["data"] = []

    # con = p.connect("dbname=" + dbname +" user=" + username + " password=" + password + " host=" + host + " port=" + port)
    con = p.connect("dbname=demo user='postgres' password='' host='localhost' port=5433")
    cur = con.cursor()
    cur.execute("select * from input_data")
    rows = cur.fetchall()

    list_of_teams = []
    # Get team names
    for row in rows:
        if (row[1] > 0):
            list_of_teams.append(row[0])

    # Sagarin rankings
    url = "https://www.usatoday.com/sports/ncaab/sagarin/" + year + "/team/"

    page = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find_all('pre')

    # Sanitize the data
    table_str = table.__str__().replace(";", "")
    table_str = table_str.replace('=<font color="#9900ff">', "")
    table_str = table_str.replace("</font>", "")
    table_str = table_str.replace("&ampnbsp", " ")
    table_str = table_str.replace("<br/>", " ")
    table_str = table_str.replace("=<font", " ")
    table_str = table_str.replace('color="#9900ff', " ")
    table_str = table_str.replace('color=', " ")
    table_str = table_str.replace('">', " ")
    table_str = table_str.replace('<font  "#000000', " ")

    # Rating = Sagarin value (eg. 92.12 or 78.91)
    # Ranking = Team ranking relative to other teams (eg. 1 or 42)
    # RATING_OFFSET = 32
    RATING_OFFSET = 40
    RANKING_OFFSET = 5

    # Alias of certain team names
    team_alias = {}
    team_alias["Saint Mary's"] = "Saint Mary's-Cal."
    team_alias["Xavier"] = "Xavier-Ohio"
    team_alias["Miami FL"] = "Miami-Florida"
    team_alias["VCU"] = "VCU(Va. Commonwealth)"
    team_alias["USC"] = "Southern California"
    team_alias["UNC Wilmington"] = "NC Wilmington"
    team_alias["North Carolina State"] = "NC State"
    team_alias["UNC Asheville"] = "NC Asheville"
    team_alias["Loyola MD"] = "Loyola-Maryland"
    team_alias["LIU Brooklyn"] = "Long Island U."

    seen_team = {}

    for team in list_of_teams:
        # Team name for database
        org_team = team

        # Check to see if there are any trailing white spaces
        if team[-1] == " ":
            team = team[0:-1]

        # Check to see if team name ends in "St." and replace it with "State"
        if team[-3:] == "St.":
            temp = team.split()
            temp[-1] = "State"
            team = " ".join(temp)
        # Check for an alias
        if team in team_alias:
            team = team_alias[team]

        indicies_of_results = find_all(table_str, team)

        print("TEAM: ", team)

        for element in indicies_of_results:
            # Grab the row
            row_info = table_str[element - RANKING_OFFSET:element + RATING_OFFSET].split()

            number_of_words = len(team.split())

            rank = 0
            rating = 0.0

            try:
                rank = int(row_info[0])
            except:
                rank = -1

            try:
                # rating = float(row_info[-1])
                rating = float(row_info[1+number_of_words])
            except:
                rating = -1

            # If rating and ranking are both valid then it checks the team name for a match
            if rank != -1 and rating != -1:
                del row_info[-1]
                del row_info[0]
                team_name = ' '.join(row_info)
                if team_name == team and team_name not in seen_team:
                    seen_team[team_name] = True
                    cur.execute("UPDATE input_data SET sagarin=%s, sagarinrank=%s WHERE name=%s",
                                [float(rating), int(rank), org_team])

    con.commit()

    return context

# Finds all indicies of a substring in a string
def find_all(a_str, sub):
    start = 0
    temp_arr = []
    while True:
        start = a_str.find(sub, start)
        if start == -1: return temp_arr
        temp_arr.append(start)
        # yield start
        start += len(sub) # use start += 1 to find overlapping matches