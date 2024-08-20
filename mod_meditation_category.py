from mod_utilize import app, session, redirect, url_for, request, render_template
from mod_db_meditation import getMeditationCategories

@app.route('/select_category', methods=['GET', 'POST'])
def select_category():
    if request.method == 'POST':
        selected_category = request.form['category']
        session['selected_category'] = selected_category
        return redirect(url_for('start_meditation'))  # Redirect to the meditation start page
    
    # Retrieve categories from the database
    categories = getMeditationCategories()
    
    # Render the category selection page
    return render_template('select_category.html', categories=categories)
