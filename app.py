from flask import Flask, render_template,request
from mod_utilize import flash, render_template, request, app
from mod_login_logout import login, logout
from mod_reset_password import update_user_password
from mod_ai_meditation import prepare_meditation
from mod_contact_us import contact_us
from mod_forgot_password import forgot_password
from mod_reset_password import reset_password
from mod_view_users import view_users
from mod_view_profile import view_profile, view_user_profile
from mod_dashboard import dashboard
from mod_meditation_category import select_category,meditation_category, meditation_details, submit_feedback
from mod_breathing import breathing_exercise
from mod_edit_profile import edit_profile
from mod_register import register
from mod_change_password import change_password
from app_error_handling import *
import os


@app.route('/')
def index():
    return render_template('homepage.html')

app.add_url_rule('/prepare_meditation', 'prepare_meditation', prepare_meditation, methods=['GET', 'POST'])


@app.route('/meditation_end')
def meditation_end():
    return render_template('meditation_end.html')

if __name__ == '__main__':
    app.run(debug=True)
