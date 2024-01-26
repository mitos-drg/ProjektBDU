#!/usr/bin/env python3

import urllib.parse
from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import app_utilities as utils
import psycopg2 as psql

# Get authorization info
user = utils.get_auth_cookie()

# Load jinja templates environment
env = Environment(loader=FileSystemLoader("templates"))

# Handle user authorization
if user['id'] == '':
    print("Status: 401 Unauthorized")
    print("Content-Type: text/html\n")
    # Print unauthorized template
    temp = env.get_template("error.html")
    print(temp.render(error="401 Unauthorized", description="Zaloguj się, aby wyświetlić zawartość."))
    exit(0)

# Connect to the database
try:
    with open(".pgpass", "r") as pgfile:
        pgpass = pgfile.read()
    connection = psql.connect(pgpass)
except:
    print("Status: 500 Internal Server Error")
    print("Content-type: text/html\n")
    print("Error occurred while connecting to the database.")
    exit(0)

# Get elections data
elections = []
with connection.cursor() as cursor:
    try:
        # Get elections this user has voted in
        cursor.execute("SELECT election FROM VotesAPI WHERE voter = %s", (user['id'],))
        voted = cursor.fetchall()
        voted = [v[0] for v in voted]

        # Get all elections
        cursor.execute("SELECT * FROM ElectionsAPI")
        # Translate select results to elections objects
        for election in cursor:
            elections.append(
                {
                    # ElectionsAPI(id, name, seats, submit, start, ends, is_public)
                    'id': election[0],
                    'name': election[1],
                    'name_url': urllib.parse.quote_plus(election[1]),
                    'seats': election[2],
                    'nominating': election[3],
                    'start': election[4],
                    'end': election[5],
                    'is_public': election[6],
                    'is_nominating': datetime.now() <= election[3],
                    'is_voting': election[4] <= datetime.now() <= election[5],
                    'voted': election[0] in voted,
                }
            )
    except (Exception, psql.DatabaseError) as error:
        print("Status: 500 Internal Server Error")
        print("Content-type: text/html\n")
        print(error)

# Close connection
connection.close()

# Start response for the client
print("Status: 200 OK")
print("Content-type: text/html\n")

# Render templated site
template = env.get_template("elections.html")
data = {
    'user': user,
    'elections': elections
}
print(template.render(data))
