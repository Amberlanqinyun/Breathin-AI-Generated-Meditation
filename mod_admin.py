from flask import render_template, request, redirect, url_for, flash, session
from mod_utilize import app
from mod_db_user_management import get_all_users, get_user_by_id, update_user_profile, toggle_user_ban
from mod_db_meditation_management import get_all_meditations, get_meditation_by_id, insert_meditation, update_meditation, delete_meditation
from mod_db_category_management import get_all_categories, insert_category, update_category, get_category_by_id

# Admin Dashboard Home
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if not session.get('user_role') == 'Admin':
        return redirect(url_for('login'))  # Ensure only Admins access this route
    
    return render_template('admin/dashboard.html')

# User Management
@app.route('/admin/users', methods=['GET'])
def admin_users():
    users = get_all_users()
    return render_template('admin/users.html', users=users)

@app.route('/admin/user/<int:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    user = get_user_by_id(user_id)

    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        ban_status = request.form.get('ban_status')

        update_user_profile(user_id, first_name, last_name, email)
        toggle_user_ban(user_id, ban_status)
        flash('User updated successfully!', 'success')
        return redirect(url_for('admin_users'))

    return render_template('admin/edit_user.html', user=user)

# Meditation Management
@app.route('/admin/meditations', methods=['GET', 'POST'])
def admin_meditations():
    meditations = get_all_meditations()  # Fetch all meditations
    categories = get_all_categories()  # Fetch all categories

    if request.method == 'POST':
        category_id = request.form.get('category_id')
        text_content = request.form.get('text_content')
        audio_file_path = request.form.get('audio_file_path')

        insert_meditation(category_id, text_content, audio_file_path)
        flash('New meditation added successfully!', 'success')
        return redirect(url_for('admin_meditations'))

    return render_template('admin/meditations.html', meditations=meditations, categories=categories)


import os
from werkzeug.utils import secure_filename
from flask import flash, request, redirect, url_for

UPLOAD_FOLDER = 'static/music/'  # Set the upload folder path

@app.route('/admin/meditation/<int:meditation_id>', methods=['GET', 'POST'])
def admin_edit_meditation(meditation_id):
    meditation = get_meditation_by_id(meditation_id)

    if request.method == 'POST':
        text_content = request.form.get('text_content')
        
        # Check if a file is included in the request
        if 'audio_file_path' in request.files:
            audio_file = request.files['audio_file_path']

            if audio_file.filename != '':
                # Generate new file name based on the meditation name
                filename = secure_filename(f"{text_content}.mp3")

                # Save the file to the static/music/ directory
                audio_file.save(os.path.join(UPLOAD_FOLDER, filename))

                # Store the file path in the database
                audio_file_path = f"{UPLOAD_FOLDER}{filename}"
                
                # Update the database with the new audio file path
                update_meditation(meditation_id, text_content, audio_file_path)
                flash('Meditation updated successfully with new audio!', 'success')
            else:
                # If no new file is uploaded, just update the text content
                update_meditation(meditation_id, text_content, meditation['AudioFilePath'])
                flash('Meditation updated successfully!', 'success')

        return redirect(url_for('admin_meditations'))

    return render_template('admin/edit_meditation.html', meditation=meditation)


@app.route('/admin/meditation/delete/<int:meditation_id>', methods=['POST'])
def admin_delete_meditation(meditation_id):
    delete_meditation(meditation_id)
    flash('Meditation deleted successfully!', 'success')
    return redirect(url_for('admin_meditations'))

# Category Management
@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():
    categories = get_all_categories()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        insert_category(name, description)
        flash('Category created successfully!', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/categories.html', categories=categories)

@app.route('/admin/category/<int:category_id>', methods=['GET', 'POST'])
def admin_edit_category(category_id):
    category = get_category_by_id(category_id)

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')

        update_category(category_id, name, description)
        flash('Category updated successfully!', 'success')
        return redirect(url_for('admin_categories'))

    return render_template('admin/edit_category.html', category=category)
