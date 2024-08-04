copy environment file and fill in environment variables
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
