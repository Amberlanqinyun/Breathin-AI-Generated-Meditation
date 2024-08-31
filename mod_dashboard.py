from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash, session
from mod_utilize import app
from mod_db_achievements import get_user_achievements, get_user_meditation_history

@app.route('/dashboard')
def dashboard():
    """
    Render the user dashboard page, displaying meditation history, achievements, and usage reports.
    """
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))

    try:
        # Fetch user meditation history, achievements, and usage reports
        meditation_history = get_user_meditation_history(user_id)
        achievements = get_user_achievements(user_id)

        # Prepare data for heatmap (past year)
        today = datetime.now().date()
        start_date = today - timedelta(days=365)
        days_practiced = {session['SessionDateTime'].date() for session in meditation_history}
        heatmap_data = [(start_date + timedelta(days=i)) in days_practiced for i in range(365)]

        # Debugging information to check fetched data
        print(f"Meditation History: {meditation_history}")
        print(f"Achievements: {achievements}")

    except Exception as e:
        flash(f"An error occurred while fetching data: {str(e)}", "error")
        return redirect(url_for('login'))

    # Render the user dashboard with calculated data
    return render_template('dashboard.html', 
                           meditation_history=meditation_history,
                           achievements=achievements,
                           heatmap_data=heatmap_data)
