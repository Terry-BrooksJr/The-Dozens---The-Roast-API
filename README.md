# Yo' Mama - The Roast API 

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

* resources - holds all endpoints.
* app.py - flask application initialization(entrypoint).
* tests - all testing related to the API
* utils - Collection of Global utility Classes and functions
* database - All things related to the primary Database - MongoDB

## Running 

1. Clone repository.
2. pip install requirements.txt
3. Start server by running  python3 app.py run
## Usage
### POST endpoints
POST http://127.0.0.1:5000/signup
http://127.0.0.1:5000/signup    
REQUEST
```json
{
	"email": "sample@email.com",
    "password": "myPassWord"
}
```
RESPONSE
```json
{
    "id": "639908d09e3d57d4baa655d4"
}
```
POST http://127.0.0.1:5000/token

#TODO - Finish Documentation
```
GET http://127.0.0.1:5000/insult
```json

```
GET http://127.0.0.1:5000/insult/<catagory>
```json

```
