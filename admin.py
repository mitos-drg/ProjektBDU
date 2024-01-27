#!/usr/bin/env python3

from datetime import datetime
from jinja2 import Environment, FileSystemLoader
import app_utilities as utils
import psycopg2 as psql

# Get authorization info from cookie
user = utils.get_auth_cookie()

# Load jinja templates environment
env = Environment(loader=FileSystemLoader("templates"))

# Handle user authorization
if user['id'] != '000000':
    print("Status: 401 Unauthorized")
    print("Content-Type: text/html\n")
    # Print unauthorized template
    temp = env.get_template("error.html")
    print(temp.render(error="401 Unauthorized", description="Dostęp jedynie dla członków komisji wyborczej."))
    exit(0)

# Start response for the client
print("Status: 200 OK")
print("Content-type: text/html\n")

# Check which action to perform
action = utils.get_get_data().get('action', [None])[0]

# Render templated site
voters = []
if action == "election":
    template = env.get_template("election-form.html")
elif action == "user":
    template = env.get_template("user-form.html")
elif action == "list":
    # Connect to the database
    with open(".pgpass", "r") as pgfile:
        pgpass = pgfile.read()
    connection = psql.connect(pgpass)

    # Read all users from the database except voting committee
    with connection.cursor() as cursor:
        try:
            cursor.execute("SELECT * FROM VotersAPI WHERE index != '000000'")
            # Translate select results to elections objects
            for voter in cursor:
                voters.append(
                    {
                        # VotersAPI(index, name, surname, password)
                        'id': voter[0],
                        'name': voter[1],
                        'surname': voter[2],
                    }
                )
        except (Exception, psql.DatabaseError) as error:
            print("Status: 500 Internal Server Error")
            print("Content-type: text/html\n")
            print(error)
    template = env.get_template("user-list.html")

    # Close connection
    connection.close()
else:
    template = env.get_template("error.html")

# Prepare site data and render template
data = {
    'user': user,
    'error': "404 Page Does not Exist",
    'description': "Nie ma takiej akcji.",
    'voters': voters
}
print(template.render(data))
