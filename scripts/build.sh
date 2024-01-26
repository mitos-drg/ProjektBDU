#!/usr/bin/bash

# Variables definitions
BUILD_DIR="_site"

# Create build directory if not existent
mkdir -p "$BUILD_DIR"
mkdir -p "$BUILD_DIR/assets"
mkdir -p "$BUILD_DIR/templates"

# Move all CGI scripts to target directory and set as executable
for file in *.py
do
    cp "$file" "$BUILD_DIR/$file"
    chmod +x "$BUILD_DIR/$file"
done

# Copy assets and templates
cp assets/* "$BUILD_DIR/assets/"
cp templates/* "$BUILD_DIR/templates/"

# Copy index file
cp index.html "$BUILD_DIR/index.html"

