# Import necessary modules and functions
from mod_utilize import current_date, app, flash, session, redirect, url_for, render_template
from db_baseOperation import execute_query
from mod_db_meditation import getMeditationHistory, getMeditationAchievements, getStreakNotifications
from mod_db_user_queries import getQueryNumberByUserId, getQueryDetails
from mod_db_notification import getUnreadNotificationCount, getNotificationCount
from mod_db_dashboard import get_user_meditation_history,get_user_achievements,get_user_meditation_activity


@app.route('/dashboard')
def user_dashboard():
    # Assuming user_id is stored in session
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))

    # Retrieve user meditation history, achievements, and activity data
    meditation_history = get_user_meditation_history(user_id)
    achievements = get_user_achievements(user_id)
    meditation_activity = get_user_meditation_activity(user_id)

    return render_template('dashboard.html', history=meditation_history, achievements=achievements, activity=meditation_activity)
