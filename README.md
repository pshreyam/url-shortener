# URL Shortener

## Requirements and Dependencies

Requirements are listed in [requirements.txt](./requirements.txt).

```bash
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

## Environment Variables

Set your environment variables replacing your values in place of `xyz`.

```bash
export SECRET_KEY=xyz
export GOOGLE_CLIENT_ID=xyz
export GOOGLE_CLIENT_SECRET=xyz
```

You may also want to set some Flask environment variables.

```bash
export FLASK_APP=app
export FLASK_ENV=development
```

Alternatively, you may use `.env` and `.flaskenv` files to store these environment variables respectively.

## Create Database

From the root of this project spawn up a python shell. Then type the following commands.

```bash
python3

>>> from app import db
>>> db.create_all()
```

## Run

```bash
flask run
```

## Restricted URLs

Add more restricted URLs as you can!

PS: Add new URLs in new lines.