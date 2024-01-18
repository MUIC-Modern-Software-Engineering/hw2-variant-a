# Simple Leave System Service
## Description
This is a simple leave system service where user can request their leave.
## Installation
1. Clone this repository
2. Install all the dependencies
```
poetry install
```
3. Run the service
```
poetry run uvicorn leave_system.app:app
```
4. Browse to http://localhost:8000
5. There are two users: `admin` and `nonadmin` both of them the password is `password`.

## Run The Test
```
poetry run pytest
```
