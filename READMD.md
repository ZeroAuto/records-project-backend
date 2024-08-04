copy environment file and fill in environment variables
the JWT_SECRET isn't strictly necessary and can be deleted but if nothing is set you will need to sign in again every time there is a server change
likewise if you are going to use localhost:3000 FRONTEND_URL can also be removed
`cp .flaskenv.example .flaskenv`

setup up venv
`python -m venv .venv`

open environment
`source .venv/bin/activate`

install dependencies
`pip install -r requirements.txt`

migrate database
`flask db migrate`

run server
`flask run`
