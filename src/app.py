import os
import sys
from flask import Flask, redirect, url_for, render_template, flash, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user
from oauth import OAuthSignIn
from onetimepass import get_totp
from hashlib import md5
from base64 import b32encode


app = Flask(__name__)
app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'pyramus': {
        'id': os.getenv('PYRAMUS_CLIENT_ID'),
        'secret': os.getenv('PYRAMUS_CLIENT_SECRET')
    },
}

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=False)


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/credentials')
def get_credentials():
    if not current_user.is_authenticated:
        abort(403)
    user = "{0.first_name}.{0.last_name}".format(current_user)
    jid = user + "@chatproto.muikkuverkko.fi"
    password = str(get_totp(b32encode(md5(jid).digest())))
    print(sys.stderr, "Secret key: {}".format(b32encode(md5(jid).digest())))
    return jsonify({
        "jid": jid,
        "password": password
    })


@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    external_id, first_name, last_name, email = oauth.callback()
    if external_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(external_id=external_id).first()
    if not user:
        user = User(
                external_id=external_id,
                first_name=first_name, 
                last_name=last_name, 
                email=email
        )
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=False)
