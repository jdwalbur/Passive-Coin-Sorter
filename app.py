from flask import *
import mysql.connector
import json
import sys
from datetime import datetime, timedelta


app = Flask(__name__)

credentials = json.load(open("credentials.json", "r"))

latest_id = 0

def access_db(query):
    database = mysql.connector.connect(
        host=credentials["host"],
        user=credentials["user"],
        passwd=credentials["password"],
        database=credentials["database"]
    )
    cursor = database.cursor()

    cursor.execute(query)
    data = cursor.fetchall()

    cursor.close()
    database.close()
    return data

@app.route('/', methods=["GET"])
def default():
    global latest_id

    data = access_db("SELECT * FROM transactions ORDER BY id DESC;")

    latest_id = data[0][0]

    return render_template("main.html", data = data[0])

# @app.route('/data', methods=["GET"])
# def access():
#     return

@app.route('/history', methods=['GET'])
def history():
    now = datetime.now()
    now_string = now.isoformat(" ")

    timeframe = request.args.get('timeframe')

    if timeframe == None or timeframe == "today":
        oldest = now - timedelta(days=1)
        oldest_string = oldest.isoformat(" ")
    if timeframe == "week":
        oldest = now - timedelta(days=7)
        oldest_string = oldest.isoformat(" ")
    if timeframe == "all":
        oldest_string = datetime(2019, 11, 1).isoformat(" ")

    # Set up time objects
    query = "SELECT * FROM transactions WHERE timestamp BETWEEN '" + oldest_string + "' AND '" + now_string + "'ORDER BY id DESC;"

    data = access_db(query)

    return render_template("history.html", data = data)

@app.route('/update', methods=['GET'])
def update():
    global latest_id

    # Check if new data exists
    new_data = access_db("SELECT * FROM transactions WHERE id > '" + str(latest_id) + "' ORDER BY id DESC;")

    if (len(new_data) > 0):
        latest_id = int(new_data[0][0])

    return json.dumps(new_data)