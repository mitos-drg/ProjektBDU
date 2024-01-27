#!/usr/bin/env python3

import sys
import urllib.parse
import psycopg2 as psql
from os import environ

# Acquire psycopg2 UniqueViolation error
UniqueViolation = psql.errors.lookup('23505')

# Get user data from form POST request
if environ['REQUEST_METHOD'] == 'POST':
    data_length = int(environ['CONTENT_LENGTH'])
    data = sys.stdin.read(data_length)
    data = urllib.parse.parse_qs(data)
else:
    print("Status: 401 Unauthorized")
    print("Content-type: text/html\n")
    print("A gdzie mnie tu szperasz?")
    exit(0)

# Fill data into variables
election_id = data.get("election", [''])[0]
user = data.get("user", [''])[0]
votes = data.get("votes", [])

# If user didn't vote return early
if not votes:
    print("Status: 303 See Other")
    print(f"Location: elections.py\n")
    print("You shouldn't see this...")
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

# Add new vote into database
with connection.cursor() as cursor:
    try:
        query = "INSERT INTO VotesAPI VALUES (%s, %s, %s)"
        args = (election_id, user, votes[0])
        for vote in votes[1:]:
            query += ", (%s, %s, %s)"
            args += (election_id, user, vote)
        cursor.execute(query, args)
        connection.commit()
    except (Exception, psql.DatabaseError) as error:
        print("Status: 500 Internal Server Error")
        print("Content-type: text/html\n")
        print(error)
        exit(0)
    except UniqueViolation:
        print("Ni mo, nie głosujemy więcej niż raz!")

# Close connection
connection.close()

# Redirect client to the actual application
print("Status: 303 See Other")
print(f"Location: elections.py\n")
print("You shouldn't see this...")
