from flask import render_template, request, redirect, url_for, flash, session, jsonify
from mod_utilize import app,datetime
from mod_db_meditation import getMeditationCategories, get_meditation_by_category, insert_user_feedback, get_meditation_by_id, insert_meditation_session

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

@app.route('/meditation_details/<int:meditation_id>')
def meditation_details(meditation_id):
    # Fetch details for a specific meditation
    meditation = get_meditation_by_id(meditation_id)
    user_id = session.get('user_id')
    # Insert the meditation session at the start
    session_date = datetime.now().date()  # Current date
    insert_meditation_session(user_id, meditation_id, session_date)
    
    if not meditation:
        flash("Meditation not found.", "error")
        return redirect(url_for('select_category'))

    return render_template('meditation_page.html', meditation=meditation)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    rating = request.form.get('rating')
    comments = request.form.get('comments')
    meditation_id = request.form.get('meditation_id')
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to submit feedback.", "error")
        return jsonify({'error': 'User not logged in'}), 400

    if not meditation_id or not meditation_id.isdigit():
        return jsonify({'error': 'Invalid meditation session.'}), 400

    try:
        insert_user_feedback(user_id, int(meditation_id), rating, comments)
        return jsonify({'message': 'Feedback submitted successfully!'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
