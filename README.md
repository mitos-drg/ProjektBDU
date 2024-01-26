# Project for the Databases lecture at University of Warsaw 2023/2024

This repository contains final version of my project for the Databases and Online Services class in winter semester of 2023/2024. Development history is unavailable due to security reasons.

This application is meant to be run as a collection of CGI scripts at a `~mm438860/bdu` directory on your server (to change that modify redirect line in `index.html` file). To connect to your database you'll need a `.pgpass` file (application supports only PostgreSQL database) with one line with following contents:

```
dbname='<databasename>' user='<username>' host='<hostname>' password='<password>'
```

The project is provided "as-is", without any guarantees or rights. There is currently no documentation and next-to-no comments explaining the code - both may or may not appear in the future.

The application stores passwords as plain text in the database. I know, atrocious, but it is generally not secure at all and security never was any concern - it's simple learning project (on the databases, not cybersecurity!). Those bothered by that fact are welcome to create pull requests fixing it.

All user-facing text is in polish, as that was the language of the class.
