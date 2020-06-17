from flask import Flask, render_template, redirect, url_for, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import secrets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///urlshortner.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = secrets.token_hex(16)
db = SQLAlchemy(app)
 
class URL(db.Model):
    __tablename__ = 'URL'
    id = db.Column(db.Integer, primary_key=True)
    full = db.Column(db.String(255), nullable=False)
    short = db.Column(db.String(255), nullable=False, unique=True)
    clicks = db.Column(db.Integer, default=0)

@app.route('/')
def index():
    url_list = URL.query.all()
    return render_template('index.html', url_list=url_list)

@app.route('/shorten/url', methods=['POST'])
def shorten_url():
    full_url = request.form.get('full-url')
    existing_url = True
    while existing_url:
        short_url = secrets.token_urlsafe(10)
        existing_url = URL.query.filter_by(short=short_url).first()
    new_url = URL(full=full_url,short=short_url)
    db.session.add(new_url)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/<string:short_url>')
def get_url(short_url):
    existing_url = URL.query.filter_by(short=short_url).first()
    if existing_url:
        full_url = existing_url.full
        existing_url.clicks += 1
        db.session.commit()
        return redirect(full_url, code=301)
    else:
        abort (404)

@app.route('/delete/<int:url_id>')
def delete_url(url_id):
    URL.query.filter_by(id=url_id).delete()
    db.session.commit()
    return redirect(url_for('index'))

@app.errorhandler(404)
def error_handler(err):
    return '<h1>Sorry! No URL found!</h1>', 404

if __name__ == "__main__":
    app.run(debug=True)
