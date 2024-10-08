import os

from authlib.integrations.flask_client import OAuth
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///db.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

db = SQLAlchemy(app)
oauth = OAuth(app)

google = oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url="https://accounts.google.com/o/oauth2/token",
    access_token_params=None,
    authorize_url="https://accounts.google.com/o/oauth2/auth",
    authorize_params=None,
    api_base_url="https://www.googleapis.com/oauth2/v1/",
    userinfo_endpoint="https://openidconnect.googleapis.com/v1/userinfo",
    client_kwargs={"scope": "openid email profile"},
    jwks_uri="https://www.googleapis.com/oauth2/v3/certs",
)

from app import routes
