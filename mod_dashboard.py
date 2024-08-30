from flask import render_template, request, redirect, url_for, flash, session, jsonify
from mod_utilize import app
from mod_db_achievements import get_user_achievements,get_user_usage_reports, get_user_meditation_history

@app.route('/dashboard')
def dashboard():
        # Assuming user_id is stored in session
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))

    # Retrieve user meditation history, achievements, and usage reports
    meditation_history = get_user_meditation_history(user_id)
    achievements = get_user_achievements(user_id)
    usage_reports = get_user_usage_reports(user_id)

    # Render the user dashboard with calculated data
    return render_template('dashboard.html', 
                           meditation_history=meditation_history,
                           achievements=achievements,
                           usage_reports=usage_reports)