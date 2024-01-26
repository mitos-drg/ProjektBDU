#!/usr/bin/env python3

import sys
import urllib.parse
import psycopg2 as psql
from os import environ

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

name = data.get("name", [''])[0]
seats = data.get("seats", [''])[0]
nominating = data.get("nominating", [''])[0]
start = data.get("start", [''])[0]
ends = data.get("ends", [''])[0]

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

connection.close()

# Redirect client to the actual application
print("Status: 303 See Other")
print(f"Location: elections.py\n")
print("You shouldn't see this...")
