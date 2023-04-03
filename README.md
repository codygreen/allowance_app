# Allowance Demo Application

Demo application based on providing allowances and tracking deposits and withdrawals.

## Requirements

This demo leverages:

- [Task](https://taskfile.dev/#/) runner for ease of use
- [NGINX Unit](https://unit.nginx.org) as the API server
- [MongoDB](https://www.mongodb.com/) as the database

## Tasks

task: Available tasks for this project:

- local-dev-family:         Launch local server for development
- local-dev-ledger:         Launch local server for development
- local-dev-users:          Launch local server for development
- mongo-delete:             Remove the MongoDB container
- mongo-deploy:             Deploy the MongoDB container
- mongo-start:              Start the MongoDB container
- mongo-stop:               Stop the MongoDB container
- unit-delete:              Delete the NGINX Unit container
- unit-deploy:              Launch NGINX unit against local dev code
- unit-get-config:          Get the NGINX Unit configuration
- unit-reload-config:       Reload the NGINX Unit configuration
