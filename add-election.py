#!/usr/bin/env python3

import sys
import urllib.parse
import psycopg2 as psql
from os import environ

# Acquire psycopg2 UniqueViolation error
UniqueViolation = psql.errors.lookup('23505')

# Get user data from form POST request or throw unauthorized error when accessed via GET request
if environ['REQUEST_METHOD'] == 'POST':
    data_length = int(environ['CONTENT_LENGTH'])
    data = sys.stdin.read(data_length)
    data = urllib.parse.parse_qs(data)
else:
    print("Status: 401 Unauthorized")
    print("Content-type: text/html\n")
    print("A gdzie mnie tu szperasz?")
    exit(0)

# Fill data into variables, with empty string being the default (error) value
name = data.get("name", [''])[0]
seats = data.get("seats", [''])[0]
nominating = data.get("nominating", [''])[0]
start = data.get("start", [''])[0]
ends = data.get("ends", [''])[0]

# Connect to the database and throw server error on failure
try:
    with open(".pgpass", "r") as pgfile:
        pgpass = pgfile.read()
    connection = psql.connect(pgpass)
except:
    print("Status: 500 Internal Server Error")
    print("Content-type: text/html\n")
    print("Error occurred while connecting to the database.")
    exit(0)

# Insert new nominee into the database, throwing server error on database failure and silently ignore duplicated entry
with connection.cursor() as cursor:
    try:
        cursor.execute("INSERT INTO ElectionsAPI(name, seats, submit, start, ends, is_public) VALUES (%s, %s, %s, %s, %s, FALSE)",
                       (name, seats, nominating, start, ends))
        connection.commit()
    except (Exception, psql.DatabaseError) as error:
        print("Status: 500 Internal Server Error")
        print("Content-type: text/html\n")
        print(error)
        exit(0)
    except UniqueViolation:
        print("Nominee already exists.")

# Close connection
connection.close()

# Redirect client to the actual application
print("Status: 303 See Other")
print(f"Location: elections.py\n")
print("You shouldn't see this...")
