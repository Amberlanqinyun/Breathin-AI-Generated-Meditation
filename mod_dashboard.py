# Import necessary modules and functions
from mod_utilize import current_date, app, flash, session, redirect, url_for, render_template
from db_baseOperation import execute_query
from mod_db_meditation import getMeditationHistory, getMeditationAchievements, getStreakNotifications
from mod_db_user_queries import getQueryNumberByUserId, getQueryDetails
from mod_db_notification import getUnreadNotificationCount, getNotificationCount

# Define a route for displaying the dashboard
@app.route('/dashboard')
def dashboard():
    user_id = session.get('user_id')
    role_id = session.get('role_id')
    messages = ""

    if user_id is None:
        flash('Please log in to access the dashboard.')
        return redirect(url_for('login'))

    # Fetch user details based on their role
    query = "SELECT * FROM Users WHERE UserID = %s"
    user_details = execute_query(query, (user_id,), fetchone=True)
    
    if user_details is None:
        flash('User not found.')
        return redirect(url_for('login'))

    # Fetch user-specific data
    CustomerNumber = getQueryNumberByUserId(user_id)['count'] if role_id == 1 else 0
   
    notificationNumber = getUnreadNotificationCount(user_id)['count'] if role_id == 1 else getNotificationCount()['count']

    # Fetch meditation history and achievements
    meditation_history = getMeditationHistory(user_id)
    achievements = getMeditationAchievements(user_id)
    streak_notifications = getStreakNotifications(user_id)

    return render_template('dashboard.html',
                           user_details=user_details,
                           messages=messages,
                           CustomerNumber=CustomerNumber,
                           notificationNumber=notificationNumber,
                           meditation_history=meditation_history,
                           achievements=achievements,
                           streak_notifications=streak_notifications)
