#!/usr/bin/bash

# Build project
./scripts/build.sh

# Compress build results
tar -czf site.tar.gz _site/*

# Send build result to remote host
scp site.tar.gz mm438860@students.mimuw.edu.pl:public_html/bdu/site.tar.gz
rm -f site.tar.gz
