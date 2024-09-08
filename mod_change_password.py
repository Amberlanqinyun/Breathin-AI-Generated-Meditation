from flask import render_template, request, redirect, url_for, flash, session
from mod_utilize import app

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if request.method == 'POST':
        # Logic to change the password
        flash("Password has been changed successfully.", "success")
        return redirect(url_for('dashboard'))
    
    return render_template('change_password.html')
