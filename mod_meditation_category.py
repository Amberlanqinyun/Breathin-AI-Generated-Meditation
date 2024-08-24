from flask import render_template, request, redirect, url_for, flash, session, Response
import json
from mod_utilize import app
from mod_db_meditation import getMeditationCategories, get_meditation_by_category, insert_user_feedback
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from mod_utilize import app
from mod_db_meditation import getMeditationCategories, get_meditation_by_category, insert_user_feedback

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
    
    return render_template('meditation_page.html', meditations=meditations, category_id=category_id)

@app.route('/submit_feedback', methods=['POST'])
def submit_feedback():
    rating = request.form.get('rating')
    comments = request.form.get('comments')
    meditation_id = request.form.get('meditation_id')
    
    # Assuming user_id is stored in session
    user_id = session.get('user_id')
    
    if not user_id:
        flash("Please log in to submit feedback.", "error")
        return redirect(url_for('login'))

    # Validate if meditation_id is provided and is a valid integer
    if not meditation_id or not meditation_id.isdigit():
        flash("Invalid meditation session. Please try again.", "error")
        return redirect(url_for('index'))

    try:
        # Insert feedback into the database
        insert_user_feedback(user_id, int(meditation_id), rating, comments)
        flash("Feedback submitted successfully!", "success")
    except Exception as e:
        flash(f"Error submitting feedback: {e}", "error")
        return redirect(url_for('index'))

    return redirect(url_for('index'))
