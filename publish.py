#!/usr/bin/env python3

import sys
import urllib.parse
import psycopg2 as psql
from os import environ
import app_utilities as utils

UniqueViolation = psql.errors.lookup('23505')

user = utils.get_auth_cookie().get('user', '')

# Get user data from form POST request
if user != '000000':
    print("Status: 401 Unauthorized")
    print("Content-type: text/html\n")
    print("A gdzie mnie tu szperasz?")
    exit(0)

election_id = utils.get_get_data().get("election", [''])[0]

# Add new nominee to the database
try:
    with open(".pgpass", "r") as pgfile:
        pgpass = pgfile.read()
    connection = psql.connect(pgpass)
except:
    print("Status: 500 Internal Server Error")
    print("Content-type: text/html\n")
    print("Error occurred while connecting to the database.")
    exit(0)

with connection.cursor() as cursor:
    try:
        # Set elections status to public
        cursor.execute("UPDATE ElectionsAPI SET is_public = TRUE WHERE id = %s", (election_id,))

        # Count votes
        candidates = []
        cursor.execute("SELECT n.index, COUNT(v.nominee) as votes "
                           "FROM NomineesAPI n "
                           "LEFT JOIN VotesAPI v ON n.index = v.nominee "
                           "WHERE n.election = %s GROUP BY n.index ORDER BY votes DESC", (election_id,))
        for candidate in cursor:
            candidates.append((candidate[0], candidate[1]))
        query = "UPDATE NomineesAPI as n SET n.votes = u.votes FROM (VALUES (%s, %s)"
        args = (candidates[0][0], candidates[0][1])
        for candidate in candidates[1:]
            query += ", (%s, %s)"
            args += (candidate[0], candidate[1])
        query += ") as u(index, votes) WHERE n.index = u.index"
        cursor.execute(query, args)
        connection.commit()
    except (Exception, psql.DatabaseError) as error:
        print("Status: 500 Internal Server Error")
        print("Content-type: text/html\n")
        print(error)
        exit(0)

connection.close()

# Redirect client to the actual application
print("Status: 303 See Other")
# print(f"Set-Cookie: password=")
print(f"Location: elections.py\n")
print("You shouldn't see this...")
