#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import app_utilities as utils

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

# Start response for the client
print("Status: 200 OK")
print("Content-type: text/html\n")

# Load and render template
template = env.get_template("nominate.html")
data = {
    'user': user,
    'election': {
        'id': election_id
    }
}
print(template.render(data))
