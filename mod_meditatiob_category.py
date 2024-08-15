# Route to display the meditation category selection page
from mod_utilize import  app, session, redirect, url_for, request, flash, render_template
@app.route('/select_category', methods=['GET', 'POST'])
def select_category():
    if request.method == 'POST':
        selected_category = request.form['category']
        session['selected_category'] = selected_category
        return redirect(url_for('start_meditation'))  # Redirect to the meditation start page
    
    # Render the category selection page
    categories = ["Mindfulness", "Relaxation", "Focus", "Sleep"]  # Example categories
    return render_template('select_category.html', categories=categories)
