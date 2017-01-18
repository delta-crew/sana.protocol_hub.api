# Sana Protocol Hub - API
The home of the Sana Protocol Hub backend API. Written in Python 3 using the Falcon framework, with SQLAlchemy and marshmallow. The API responses follow the JSend structure defined [here](https://labs.omniti.com/labs/jsend).

## Running in development
```
# Postgres is required to run
# Defaults are found in app/config.py
# An example using docker
$ docker run --name ph-db \
             -e POSTGRES_USER=$PH_API_DB_USER \
             -e POSTGRES_PASSWORD=$PH_API_DB_PASSWORD \
             -e POSTGRES_DB=$PH_API_DB_DATABASE \
             -p 5432:5432 \
             -d postgres:9.6

# Install the requirements
$ pip install -r requirements.txt

# Create the database
$ invoke create_db

# Run using gunicorn
$ gunicorn app.app:app

# Reset/drop the database
$ invoke reset_db
$ invoke drop_db
```
