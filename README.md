# My_Hellofresh
 This repository contains take-home programming challenges which will serve as important step in the interview process.
 
# Backend Focused
Problem Statement
Create a menu planning service which allows to manage weekly menu and associated recipies.

## Context
A weekly menu contains a set of recipies. Each week different set of recipies are selected. See example menu for this week.
A recipe contains ingredients, step-by-step instructions, nutirtional information, classification, and other metadata. See examples recipes here 1, 2, 3.
A customer can review weekly menu as well as recipe by assigning ratings and/or adding comments.

## Tasks
1. Create data models using your selected ORM for weekly menu, recipe, ingredients, review, etc. Make sure these data models are appripriately connected using FK, 1:M, M:M relationships.
2. Create REST APIs to create, list, read, update, delete data model objects. Bonus if you can secure API using API tokens (recommended) or JWT tokens. You can use Google Authentication to obtain JWT token.
3. Create unit and E2E tests. For E2E API tests you can use Postman but ensure Postman collection are commited to your repository. For unit tests use a framework acccording to your stack.
4. Make sure your tests can be run from a single command - create test runner makefile or bash script to run your tests.

## Technology Stack

Python 3, Flask as web framework, Flask-PyMongo as ORM, Docker as Container, MongoDB as a database, Pytest for unit test, Postman for API test
