from flask import Flask
import flask
from kenpom import kenpom_rankings
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
    cur.execute("select * from input_data")
    rows = cur.fetchall()

    list_of_teams = []
    # Get team names
    for row in rows:
        if(row[1]>0):
            list_of_teams.append(row[0])

    # Sagarin rankings
    url = "https://www.usatoday.com/sports/ncaab/sagarin/2012/team/"

    page = urllib.request.urlopen(url).read()

    soup = BeautifulSoup(page, 'html.parser')

    table = soup.find_all('pre')


    # Sanitize the data
    table_str = table.__str__().replace(";", "")
    table_str = table_str.replace('=<font color="#9900ff">', "")
    table_str = table_str.replace("</font>", "")
    table_str = table_str.replace("&ampnbsp", "")
    table_str = table_str.replace("<br/>", " ")

    # Test data
    # print(table.__str__().split())
    print(table_str.find("Ohio State"))
    print(table_str[4090-5:4090 + 60].replace(";", ""))
    print(table_str.find("Kentucky"))
    print(table_str[3933-5:3933 + 60].replace(";", ""))

    print(table_str.find("Texas-San Antonio(UTSA)"))
    print(table_str[38975-5:38975 + 60].replace(";", ""))

    print(table_str.find("Central Michigan"))
    print(table_str[55583-5:55583 + 32].replace(";", ""))

    print(table_str.find("Michigan"))
    print(table_str[4561 - 5:4561 + 32])
    print(table_str[4561 - 5:4561 + 32].split())

    # Rating = Sagarin value (eg. 92.12 or 78.91)
    # Ranking = Team ranking relative to other teams (eg. 1 or 42)
    RATING_OFFSET = 32
    RANKING_OFFSET = 5

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
            row_info = table_str[element - RANKING_OFFSET:element + RATING_OFFSET].split()

            rank = 0
            rating = 0.0

            try:
                rank = int(row_info[0])
            except:
                rank = -1

            try:
                rating = float(row_info[-1])
            except:
                rating = -1

            # If rating and ranking are both valid then it checks the team name for a match
            if rank != -1 and rating != -1:
                del row_info[-1]
                del row_info[0]
                team_name = ' '.join(row_info)
                if team_name == team:
                    cur.execute("UPDATE input_data SET where ")
                    print("IT WORKED!", row_info, rank, rating)



    table_arr = table.__str__().split()
    for e in range(len(table_arr)):
        if table_arr[e] == 'Kentucky':
            print(table_arr[e])
            print(table_arr[e-1])
            print(table_arr[e+2])
            #print("PASSED")

    # The first tr contains the field names.
    # headings = [th.get_text() for th in table.find("tr").find_all("th")]

    datasets = []
    # for row in table.find_all("tr")[1:]:
    #     #print(row)
    #     #print(td.get_text() for td in row.find_all("td"))
    #     data = row.find_all("td")
    #     temp_arr = []
    #     for td in data:
    #         # print(td.get_text())
    #         temp_arr.append(td.get_text())
    #
    #     datasets.append(temp_arr)
    #
    # datasets[:] = [item for item in datasets if len(item) != 0]
    # #print(datasets)
    # cur.execute("DELETE FROM input_data")
    # for row in datasets:
    #     rank = row[0]
    #     seed = ""
    #     if len(row[1].split()) > 1:
    #         seed = row[1].split()[-1]
    #     kenpom_val = row[4]
    #     # Remove first character (+)
    #     kenpom_val = kenpom_val[1:]
    #
    #     try:
    #         seed = int(seed)
    #     except:
    #         seed = 0
    #
    #     if seed > 0:
    #         print("Seed", row[1])
    #         # Remove seed from row
    #         temp_arr = row[1].split()
    #         temp_arr.pop(-1)
    #
    #         # Turn list into string
    #         temp_arr = ' '.join(temp_arr)
    #         row[1] = temp_arr
    #         context["data"].append(str(row[0]) + str(row[1]))
    #     name = str(row[1])
    #
    #     # print(name)
    #
    #     cur.execute("INSERT INTO input_data(name, seed, kenpom, kenpomrank) VALUES (%s, %s, %s, %s)", [name, seed, float(kenpom_val), rank])
    #
    # con.commit()




    #context = {}
    # context = kenpom_rankings()
    return flask.render_template("hello.html", **context)


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

if __name__ == '__main__':
    app.run()
