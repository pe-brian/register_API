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

# Usage

```docker-compose up -d```

# Testing

```pytest```
