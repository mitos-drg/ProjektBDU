#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import app_utilities as utils
import psycopg2 as psql

# Load jinja templates environment
env = Environment(loader=FileSystemLoader("templates"))

# Get authorization info
user = utils.get_auth_cookie()

# Handle user authorization
if user['id'] == '':
    print("Status: 401 Unauthorized")
    print("Content-Type: text/html\n")
    # Print unauthorized template
    temp = env.get_template("error.html")
    print(temp.render(error="401 Unauthorized", description="Zaloguj się, aby wyświetlić zawartość."))
    exit(0)

# Get election id
election_id = utils.get_get_data().get('election', [None])[0]

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
candidates = []
election = {}
with connection.cursor() as cursor:
    try:
        # Election details
        cursor.execute("SELECT name, seats FROM ElectionsAPI WHERE id = %s", (election_id,))
        details = cursor.fetchone()
        election = {
            'id': election_id,
            'name': details[0],
            'seats': details[1],
        }
        # Get this election candidates
        cursor.execute("SELECT n.nominee, v.name, v.surname "
                       "FROM NomineesAPI n JOIN VotersAPI v ON n.nominee = v.index "
                       "WHERE n.election = %s", (election_id,))
        # Translate select results to elections objects
        for candidate in cursor:
            candidates.append(
                {
                    # NomineesAPI(election, nominee, votes)
                    'index': candidate[0],
                    'name': candidate[1],
                    'surname': candidate[2],
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

# Load and render template
template = env.get_template("vote.html")
data = {
    'user': user,
    'candidates': candidates,
    'election': election
}
print(template.render(data))
