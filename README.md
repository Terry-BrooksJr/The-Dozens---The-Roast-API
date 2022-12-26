# Yo' Mama - The Roast API

[![linting: pylint](https://img.shields.io/badge/linting-pylint-yellowgreen)](https://github.com/PyCQA/pylint)

This project shows one of the possible ways to implement RESTful API server.

There are implemented two models: User and Todo, one user has many todos.

Main libraries used:

1. Flask-JWT-Extended - for handling Bearer Token Provision and Validation for Creation, Update operations.
2. Flask-RESTful - restful API library.
3. Flask-Script - provides support for writing external scripts.
4. Flask-Mongoengine - adds support for MongoDB ORM.
5. Flask-Bcrypt - supports the user registration system for users who want to contribute jokes

Project structure:

```
.
├── app.py
├── config.py
├── database
│   ├── db.py
│   ├── init_jokes.json
│   ├── _init__.py
│   └── models.py
├── name
├── README.md
├── requirements.txt
├── resources
│   ├── auth.py
│   ├── __init__.py
│   ├── insult.py
│   └── routes.py
├── test
│   └── db-test.py
└── utils
    ├── arguments.py
    ├── errors.py
    ├── gatekeeper.py
    ├── __init__.py
    └── parser.py
```

- resources - holds all endpoints.
- app.py - flask application initialization(entrypoint).
- tests - all testing related to the API
- utils - Collection of Global utility Classes and functions
- database - All things related to the primary Database - MongoDB

## Running

1. Clone repository.
2. pip install requirements.txt
3. Start server by running python3 app.py run

## Usage

### Method Agonistic -

Using Any HTTP Method to the **<API_URL>/status** endpoint will return:

```json

```

## POST endpoints

POST <API_URL>/signup
<API_URL>/signup

REQUEST

```json
{
  "email": "sample@email.com",
  "password": "myPassWord"
}
```

POST Keys:

- `email`: Valid Email Address
- `password` : Any combination Of **7 or More** ASCII Character.
  RESPONSE

```json
{
  "id": "639908d09e3d57d4baa655d4"
}
```

Returns BSON id - You **DO NOT** need to retain this ID.

POST <API_URL>/token

#TODO - Finish Documentation

## GET Endpoints

````
GET <API_URL>/insult
```json

````

GET <API_URL>/insult/<catagory>

```json

```

## DELETE & PATCH Operations Are Not Supported.

<sub>Feel free to open an issue or submit a PR</em>

## Additional Documentation

- [Postman](https://www.postman.com/terryabrooksjr/workspace/the-roast-api-yo-mama-jokes)
- [Swagger](http://FIXME\) #TODO - Add Swagger Link
