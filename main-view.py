#!/usr/bin/env python3

from jinja2 import Environment, FileSystemLoader
import app_utilities as utils

# Start response for the client
print("Status: 200 OK")
print("Content-type: text/html\n")

# Get authorization info
user = utils.get_auth_cookie()

# Get potential errors from url
error = utils.get_get_data().get('error', [''])[0]

# Load and render template
env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("main.html")
data = {
    'user': user,
    'site': {
        'error': error
    }
}
print(template.render(data))
