from flask import render_template, request, redirect, url_for, flash, session, jsonify
from mod_utilize import app,datetime
from mod_db_meditation import getMeditationCategories, get_meditation_by_category, insert_user_feedback, get_meditation_by_id
from mod_db_achievements import calculate_consecutive_days_streak, calculate_sessions_per_day, award_achievement,get_user_meditation_history,insert_meditation_session, has_achievement

@app.route('/select_category', methods=['GET', 'POST'])
def select_category():
    if request.method == 'POST':
        selected_category_id = request.form.get('category_id')
        if not selected_category_id:
            flash("No category selected. Please choose a category.", "error")
            return redirect(url_for('select_category'))
        
        # Redirect to the meditation category page with the selected category_id
        return redirect(url_for('meditation_category', category_id=selected_category_id))
    
    # Retrieve categories from the database
    categories = getMeditationCategories()
    
    # Render the category selection page
    return render_template('select_category.html', categories=categories)

@app.route('/meditation/<int:category_id>')
def meditation_category(category_id):
    # Fetch meditation details for the given category_id
    meditations = get_meditation_by_category(category_id)
    if not meditations:
        flash("No meditation found for the selected category.", "error")
        return redirect(url_for('select_category'))

    # Render the meditation selection page
    return render_template('select_meditation.html', meditations=meditations, category_id=category_id)


@app.route('/meditation_details/<int:meditation_id>', methods=['GET'])
def meditation_details(meditation_id):
    """
    Display details of a specific meditation and handle meditation session start.
    Automatically logs the session, checks for streaks, and awards achievements.
    """
    # Fetch details for the specific meditation
    meditation = get_meditation_by_id(meditation_id)
    user_id = session.get('user_id')

    if not meditation:
        flash("Meditation not found.", "error")
        return redirect(url_for('select_category'))

    if not user_id:
        flash("Please log in to start a meditation session.", "error")
        return redirect(url_for('login'))

    # Automatically log the meditation session
    success = insert_meditation_session(user_id, meditation_id)  # Only two arguments now

    if success:
        # Fetch the user's meditation history to check for achievements
        meditation_history = get_user_meditation_history(user_id)
        
        # Calculate the user's streak of consecutive meditation days
        streak = calculate_consecutive_days_streak(meditation_history)
        
        # Award achievements based on streak
        if streak >= 1 and not has_achievement(user_id, 'First Meditation'):
            award_achievement(user_id, 'First Meditation', 'Completed first meditation session')
        if streak >= 3 and not has_achievement(user_id, '3-Day Streak'):
            award_achievement(user_id, '3-Day Streak', 'Completed meditation for 3 consecutive days')

        # Calculate sessions per day
        sessions_per_day = calculate_sessions_per_day(meditation_history)
        for date, count in sessions_per_day.items():
            if count >= 3 and not has_achievement(user_id, 'Triple Meditation Day'):
                award_achievement(user_id, 'Triple Meditation Day', 'Completed 3 meditation sessions in one day')
    else:
        print("Failed to record meditation session. Please try again later.", "error")

    return render_template('meditation_page.html', meditation=meditation)


@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    rating = request.form.get('rating')
    comments = request.form.get('comments')
    meditation_id = request.form.get('meditation_id')
    user_id = session.get('user_id')

    if not user_id:
        return jsonify({'error': 'User not logged in'}), 400

    if not meditation_id or not meditation_id.isdigit():
        return jsonify({'error': 'Invalid meditation session.'}), 400

    if not comments:  # Check if feedback is empty
        return jsonify({'error': 'Feedback cannot be empty'}), 400

    try:
        insert_user_feedback(user_id, int(meditation_id), rating, comments)
        return jsonify({'message': 'Feedback submitted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
