import psycopg2 as p

def format_matchups():
    con = p.connect("dbname=demo user='postgres' password='' host='localhost' port=5433")
    cur = con.cursor()
    cur.execute("SELECT * FROM input_data WHERE seed=5")
    arr = cur.fetchall()

    print(arr)

if __name__ == '__main__':
    format_matchups()