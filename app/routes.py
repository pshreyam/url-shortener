import secrets

from flask import abort, flash, redirect, render_template, request, session, url_for

from app import app, db, oauth
from app.decorators import login_required, logout_required
from app.models import URL

with open("./restricted_urls", "r") as f:
    restricted_urls = f.read().split("\n")


@app.route("/login")
@logout_required
def login():
    return render_template("login.html")


@app.route("/login/google")
@logout_required
def login_google():
    google = oauth.create_client("google")
    redirect_uri = url_for("authorize", _external=True)
    return google.authorize_redirect(redirect_uri)


@app.route("/authorize")
@logout_required
def authorize():
    google = oauth.create_client("google")
    token = google.authorize_access_token()
    response = google.get("userinfo", token=token)
    user_info = response.json()
    session["email"] = user_info["email"]
    session["name"] = user_info["name"]
    session["picture"] = user_info["picture"]
    return redirect(url_for("index"))


@app.route("/logout")
@login_required
def logout():
    session.clear()
    return redirect(url_for("index"))


@app.route("/")
@login_required
def index():
    url_list = URL.query.filter_by(user=session.get("email"))
    return render_template("index.html", url_list=url_list, session=session)


@app.route("/shorten/url", methods=["POST"])
@login_required
def shorten_url():
    full_url = request.form.get("full-url")
    if full_url in restricted_urls:
        flash("Sorry, this URL is restricted. It cannot be shortened!", "danger")
        return redirect(url_for("index"))
    existing_url = True
    while existing_url:
        short_url = secrets.token_urlsafe(10)
        existing_url = URL.query.filter_by(short=short_url).first()
    new_url = URL(full=full_url, short=short_url, user=session.get("email"))
    db.session.add(new_url)
    db.session.commit()
    flash("URL successfully shortened!", "success")
    return redirect(url_for("index"))


@app.route("/<string:short_url>")
def get_url(short_url):
    existing_url = URL.query.filter_by(short=short_url).first()
    if existing_url:
        full_url = existing_url.full
        existing_url.clicks += 1
        db.session.commit()
        return redirect(full_url, code=301)
    else:
        abort(404)


@app.route("/delete/<int:url_id>")
@login_required
def delete_url(url_id):
    url = URL.query.filter_by(id=url_id).first_or_404()
    if url.user == session.get("email"):
        db.session.delete(url)
        db.session.commit()
    else:
        flash("You are not authorized to peform that action!", "danger")
    return redirect(url_for("index"))


@app.errorhandler(404)
def error_handler(err):
    return render_template("404.html"), 404
