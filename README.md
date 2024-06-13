# Register API

Flask web application to register users and activate accounts with a pin code sent by email.

# Configuration

The following variables must be defined in your environement :

    SMTP_HOST
    SMTP_PORT
    SMTP_USERNAME
    SMTP_PASSWORD
    MYSQL_DB
    MYSQL_USER
    MYSQL_PASSWORD
    MYSQL_URL

# Prerequises

- Python 3.12.4
- Docker & docker-compose

# External libraries

- Chocolatine is a Python library developped by myself (SQL queries generation)
- Bcrypt to encrypt the passwords and compare hashes

# SGBD

- MySQL

# Usage

```docker-compose up -d```

# Testing

```pytest```

# Code quality

- Code formatted with Black

# Architecture

- Take a look at the diagram available on this repo
