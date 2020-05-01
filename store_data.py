import mysql.connector
import time
from datetime import datetime
import json
import RPi.GPIO as GPIO

# BCM pin numbers for each sensor
QUARTER = 17
DIME = 18
NICKLE = 22
PENNY = 23

# Set up board, pins
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(QUARTER, GPIO.IN)
GPIO.setup(NICKLE, GPIO.IN)
GPIO.setup(PENNY, GPIO.IN)
GPIO.setup(DIME, GPIO.IN)

# Detects which sensor is triggered, amount to return
def get_amount():
    quarter_value = GPIO.input(QUARTER)
    nickle_value = GPIO.input(NICKLE)
    penny_value = GPIO.input(PENNY)
    dime_value = GPIO.input(DIME)

    if dime_value == 0:
        print("0.10")
        return 0.10
    if penny_value == 0:
        print("0.01")
        return 0.01
    if nickle_value == 0:
        print("0.05")
        return 0.05
    if quarter_value == 0:
        print("0.25")
        return 0.25
    return 0.00

def coin_detected():
    quarter_value = GPIO.input(QUARTER)
    nickle_value = GPIO.input(NICKLE)
    penny_value = GPIO.input(PENNY)
    dime_value = GPIO.input(DIME)

    if dime_value == 0:
        return True
    if penny_value == 0:
        return True
    if nickle_value == 0:
        return True
    if quarter_value == 0:
        return True
    return False

def store_data():
    if coin_detected():
        # Load database user credentials from JSON
        # <Based on code from Prof. Jim Eddy, CS 121>
        credentials = json.load(open("credentials.json", "r"))

        # Connect to database
        database = mysql.connector.connect(
            host=credentials["host"],
            user=credentials["user"],
            passwd=credentials["password"],
            database=credentials["database"]
        )
        # Create cursor object that executes database commands
        cursor = database.cursor()

        # SQL query statment
        query = "INSERT INTO transactions (timestamp, amount, current_bal) VALUES (%s, %s, %s);"

        now = datetime.now()

        print(now)

        amount = get_amount()

        cursor.execute("SELECT SUM(amount) FROM transactions;")
        for i in cursor.fetchall():
            if i[0]:
                bal = i[0] + amount
            else:
                bal = get_amount()

        # Execute SQL command
        data = (now, amount, bal)
        cursor.execute(query, data)
        database.commit()

        # Close database access
        cursor.close()
        database.close()

        time.sleep(0.5)

while True:
    store_data()