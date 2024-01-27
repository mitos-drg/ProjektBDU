#!/usr/bin/env python3

# Set user authentication cookie
print(f"Set-Cookie: user=; is_admin=;")

# Redirect client to the actual application
print("Status: 303 See Other")
print(f"Location: main-view.py\n")
print("You shouldn't see this...")
