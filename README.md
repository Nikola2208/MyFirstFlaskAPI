# Item Store
My first RESTful API with Flask

## Description
Application enables handling of domain-specific entities such as stores, items, tags. In addition, there is implemented user authetification and access control for endpoints using JWT.

## Getting Started

### Dependencies

Prerequisite:
* python@3.11
* IDE for programming in Python(recommended PyCharm)
* pip
* virtual environment using venv
  
Using following command you can install pip if it doesn't already exist(although venv comes with pip):
```
python3 -m ensurepip
```
After setting environment, through terminal run following command to install needed packages and libraries:
```
pip install -r requirements.txt
```

### Setting database

Before executing application, database needs to be set. If there isn't migrations folder already existed then first you need to run following commands to generate it and set initial version:
```
flask db init
```
```
flask db migrate
```
If there is migrations folder and database already has existing version, then run following command:
```
flask db upgrade
```
Initially database connection URL is set for PostgreSQL database on ElephantSQL platform (file .env) but by removing this line of code, automatically is created local SQLite database.

### Run application

After successful initialization of database, you are able to run application using command:
```
flask run
```

## Authors

Contributors:

* Nikola Holjevac - [n.holjevac@codeflex.it](mailto:n.holjevac@codeflex.it)
