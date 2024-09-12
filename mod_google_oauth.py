from flask import redirect, url_for, session, request, flash
from flask_oauthlib.client import OAuth
import os
from mod_utilize import app

oauth = OAuth()

# Configure Google OAuth
google = oauth.remote_app(
    'google',
    consumer_key=os.getenv('GOOGLE_CLIENT_ID', 'YOUR_GOOGLE_CLIENT_ID'),
    consumer_secret=os.getenv('GOOGLE_CLIENT_SECRET', 'YOUR_GOOGLE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'email',
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def init_oauth(app):
    oauth.init_app(app)

def create_google_routes(app):
    @app.route('/google_login')
    def google_login():
        return google.authorize(callback=url_for('authorized', _external=True))

    @app.route('/login/callback')
    def authorized():
        response = google.authorized_response()
        if response is None or response.get('access_token') is None:
            flash('Access denied: reason={} error={}'.format(
                request.args['error_reason'],
                request.args['error_description']
            ))
            return redirect(url_for('index'))

        session['google_token'] = (response['access_token'], '')
        user_info = google.get('userinfo')
        session['user'] = user_info.data
        return redirect(url_for('dashboard'))

    @google.tokengetter
    def get_google_oauth_token():
        return session.get('google_token')
