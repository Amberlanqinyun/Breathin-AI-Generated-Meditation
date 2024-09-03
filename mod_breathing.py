from flask import render_template, request, redirect, url_for, flash, session
from mod_utilize import app  


@app.route('/breathing_exercise')
def breathing_exercise():
    """
    Render the breathing exercise page.
    """
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to access the breathing exercise.", "error")
        return redirect(url_for('login'))

    # Render the breathing exercise page
    return render_template('breathing.html')
