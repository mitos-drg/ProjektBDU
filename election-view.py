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

# Fill variables from GET string data
election_id = utils.get_get_data().get('election', [None])[0]
election_name = utils.get_get_data().get('name', [None])[0]
is_public = utils.get_get_data().get('public', [False])[0]
is_closed = utils.get_get_data().get('closed', [False])[0]
seats = utils.get_get_data().get('seats', [1])[0]

# If there is invalid election id or name throw 404
if election_id is None or election_name is None:
    print("Status: 404 Page Not Found")
    print("Content-Type: text/html\n")
    temp = env.get_template("error.html")
    print(temp.render(error="404 Page Not Found", description="ID i nazwa wyborów są wymagane."))

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
with connection.cursor() as cursor:
    try:
        if is_public:
            cursor.execute("SELECT n.nominee, v.name, v.surname, n.votes "
                           "FROM NomineesAPI n JOIN VotersAPI v ON n.nominee = v.index "
                           "WHERE election = %s", (election_id,))
        else: # Admin view
            cursor.execute("SELECT n.index, MIN(vn.name), MIN(vn.surname), COUNT(n.index) as votes "
                           "FROM NomineesAPI n "
                           "LEFT JOIN VotesAPI v ON n.index = v.nominee LEFT JOIN VotersAPI vn ON n.index = vn.index "
                           "WHERE n.election = %s GROUP BY n.index ORDER BY votes DESC", (election_id,))

        # Translate select results to elections objects
        for candidate in cursor:
            candidates.append(
                {
                    # NomineesAPI(election, nominee, votes)
                    'index': candidate[0],
                    'name': candidate[1],
                    'surname': candidate[2],
                    'votes': candidate[3] if not None else 0,
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
template = env.get_template("election-details.html")
data = {
    'user': user,
    'candidates': candidates,
    'election': {
        'id': election_id,
        'name': election_name,
        'public': is_public,
        'closed': not is_closed,
        'seats': seats,
    }
}
print(template.render(data))
