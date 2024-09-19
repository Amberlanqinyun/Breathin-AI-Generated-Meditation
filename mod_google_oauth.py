from flask import redirect, url_for, session, request, flash
from flask_oauthlib.client import OAuth
import os
import ssl
import certifi
from dotenv import load_dotenv
from mod_utilize import *
from mod_db_account import create_user, update_user, search_user
from db_baseOperation import execute_query

# Load environment variables from .env file
load_dotenv()

oauth = OAuth()

# Configure SSL context
ssl_context = ssl.create_default_context(cafile=certifi.where())

# Configure Google OAuth
google = oauth.remote_app(
    'google',
    consumer_key=os.getenv('GOOGLE_CLIENT_ID'),
    consumer_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    request_token_params={
        'scope': 'openid email profile',  # Use valid scopes
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
)

def pre_request(uri, headers, body):
    headers.update({'verify': certifi.where()})
    return uri, headers, body

google.pre_request = pre_request

def init_oauth(app):
    oauth.init_app(app)

def create_google_routes(app):
    @app.route('/google_login')
    def google_login():
        return google.authorize(callback=url_for('authorized', _external=True))

    @app.route('/login/callback')
    def authorized():
        try:
            print("Entering authorized function")
            response = google.authorized_response()
            print("Authorized response:", response)
            
            if response is None or response.get('access_token') is None:
                print("Access denied or no access token")
                flash('Access denied: reason={} error={}'.format(
                    request.args['error_reason'],
                    request.args['error_description']
                ))
                return redirect(url_for('index'))

            print("Access token received:", response['access_token'])

            session['google_token'] = (response['access_token'], '')
            user_info = google.get('userinfo', token=(response['access_token'], ''))
            print("User info response:", user_info)
            user_data = user_info.data

            print("User info received:", user_data)

            # Extract user information
            email = user_data.get('email')
            first_name = user_data.get('given_name', '')  # Default to empty string if missing
            last_name = user_data.get('family_name', '')  # Default to empty string if missing
            google_id = user_data.get('id')

            # Check if user exists in the database
            user = search_user(email)
            print("User found in database:", user)
            if user:
                # Update existing user
                update_user(user['UserID'], first_name, last_name, email, google_id)
                print("User updated:", user)
            else:
                # Create new user
                user_id = create_user(first_name, last_name, email, None, google_id)
                print("New user created with ID:", user_id)

            # Set session variables
            session['user_id'] = user['UserID'] if user else user_id
            session['role_id'] = user['RoleID'] if user else 2  # Assuming default role is 2 for new users
            session['user'] = user_data
            print("Session set for user:", session['user'])
            flash('You have successfully logged in!', 'success')
            return redirect(url_for('dashboard'))

        except Exception as e:
            print(f"Error in authorized function: {e}")
            import traceback
            traceback.print_exc()
            return redirect(url_for('index'))

    @google.tokengetter
    def get_google_oauth_token():
        return session.get('google_token')
