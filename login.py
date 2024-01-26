#!/usr/bin/env python3

import sys
import urllib.parse
import psycopg2 as psql
from os import environ

# Get user data from form POST request
if environ['REQUEST_METHOD'] == 'POST':
    data_length = int(environ['CONTENT_LENGTH'])
    data = sys.stdin.read(data_length)
    data = urllib.parse.parse_qs(data)
else:
    data = {}


def login_error(error: str):
    # Send empty authorization cookie
    print(f"Set-Cookie: user=; is_admin=")

    error = urllib.parse.quote_plus(error)

    # Redirect with error
    print("Status: 303 See Other")
    print(f"Location: main-view.py?error={error}\n")
    # print("Content-Type: text/html\n")
    # print(f'<a href="/cgi-bin/main-view.cgi.py?error={error}">link</a>')
    print("You shouldn't see this...")
    exit(0)


username = data.get("user", [''])[0]
password = data.get("password", [''])[0]
is_admin = False
if username == '000000':
    is_admin = True

if username == '' or password == '':
    login_error("Nieprawidłowy login lub hasło")

# Connect to the database and get user password
result = None
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
        # Get user password
        cursor.execute("SELECT * FROM votersAPI WHERE index = %s AND password = %s", (username, password))
        result = cursor.fetchone()
    except (Exception, psql.DatabaseError) as error:
        print("Status: 500 Internal Server Error")
        print("Content-type: text/html\n")
        print(error)
        exit(0)

connection.close()

# Check user password
if result is None:
    login_error("Nieprawidłowy login lub hasło")

# Redirect client to the actual application
print("Status: 303 See Other")
print(f"Set-Cookie: user={username}; is_admin={is_admin};")
print(f"Location: main-view.py\n")
print("You shouldn't see this...")
