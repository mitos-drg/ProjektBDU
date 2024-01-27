#!/usr/bin/env python3

import sys
import urllib.parse
import psycopg2 as psql
from os import environ

# Acquire psycopg2 UniqueViolation error
UniqueViolation = psql.errors.lookup('23505')

# Get user data from form POST request and throw error on different request method
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
index = data.get("index", [''])[0]
name = data.get("name", [''])[0]
surname = data.get("surname", [''])[0]
password = data.get("password", [''])[0]

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

# Insert new user to the database, throwing 500 code on server errors but ignoring duplicated entry
with connection.cursor() as cursor:
    try:
        cursor.execute("INSERT INTO VotersAPI VALUES (%s, %s, %s, %s)",
                       (index, name, surname, password))
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
