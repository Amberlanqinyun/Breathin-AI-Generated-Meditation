from flask import Flask, render_template, request, redirect, url_for, flash, session
from mod_utilize import app
from mod_google_oauth import init_oauth, create_google_routes
from mod_custom_login import login, enter_password, logout
from mod_reset_password import update_user_password
from mod_ai_meditation import prepare_meditation
from mod_contact_us import contact_us
from mod_forgot_password import forgot_password
from mod_reset_password import reset_password
from mod_view_users import view_users
from mod_view_profile import view_profile, view_user_profile
from mod_dashboard import dashboard
from mod_meditation_category import select_category, meditation_category, meditation_details, submit_feedback
from mod_breathing import breathing_exercise
from mod_edit_profile import edit_profile
from mod_register import register
from mod_change_password import change_password
from app_error_handling import *
from mod_admin import admin_dashboard, admin_meditations, admin_delete_meditation, admin_categories, admin_edit_meditation
from mod_chat_ai import chat_ai
import os
import ssl
import certifi
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.DEBUG)
print("Starting Flask Application...")

# Create SSL context
ssl_context = ssl.create_default_context(cafile=certifi.where())
print("SSL context created with certifi path:", certifi.where())

# Initialize Google OAuth
try:
    init_oauth(app)
    create_google_routes(app)
except Exception as e:
    print(f"Error initializing Google OAuth: {e}")

# Define routes
@app.route('/')
def index():
    return render_template('homepage.html')

# Add URL rule for prepare_meditation
app.add_url_rule('/prepare_meditation', 'prepare_meditation', prepare_meditation, methods=['GET', 'POST'])

# Define another route
@app.route('/meditation_end')
def meditation_end():
    return render_template('meditation_end.html')


# Main application entry point
if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))

    # Print all routes
    print("\nListing all registered routes:")
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, URL: {rule.rule}")

    # Start the Flask app
    app.run(host="0.0.0.0", port=port)
