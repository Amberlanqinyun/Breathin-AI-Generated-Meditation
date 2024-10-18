from flask import render_template, request, redirect, url_for, flash, session, abort, logging
from mod_utilize import app
from mod_db_user_management import get_all_users, get_user_by_id, update_user_profile, toggle_user_ban, delete_user
from mod_db_meditation_management import get_all_meditations, get_meditation_by_id, insert_meditation, update_meditation, delete_meditation
from mod_db_category_management import get_all_categories, insert_category, update_category, get_category_by_id, delete_category
from mod_db_account import is_admin
from mod_custom_login import *
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'static/music/'  # Set the upload folder path


# Admin Dashboard Home
@app.route('/admin', methods=['GET'])
def admin_dashboard():
    if not is_admin():
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))
    
    return render_template('admin/dashboard.html')

# User Management
@app.route('/admin/users', methods=['GET'])
def admin_users():
    if not is_admin():
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    search_query = request.args.get('search', '')
    try:
        users = get_all_users(search_query)
    except Exception as e:
        flash(f"Error retrieving users: {str(e)}", 'error')
        users = []
    return render_template('admin/users.html', users=users, search_query=search_query)

@app.route('/admin/user/<int:user_id>', methods=['GET', 'POST'])
def admin_edit_user(user_id):
    if not is_admin():
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    try:
        user = get_user_by_id(user_id)
        if not user:
            flash('User not found.', 'error')
            return redirect(url_for('admin_users'))
    except Exception as e:
        logging.error(f"Error retrieving user: {str(e)}")
        flash(f"Error retrieving user: {str(e)}", 'error')
        return redirect(url_for('admin_users'))

    if request.method == 'POST':
        try:
            first_name = request.form.get('first_name')
            last_name = request.form.get('last_name')
            email = request.form.get('email')
            ban_status = request.form.get('ban_status')

            update_user_profile(user_id, first_name, last_name, email)
            toggle_user_ban(user_id, ban_status)
            flash('User updated successfully!', 'success')
        except Exception as e:
            flash(f"Error updating user: {str(e)}", 'error')
        return redirect(url_for('admin_users'))

    return render_template('admin/edit_user.html', user=user)

@app.route('/admin/user/delete/<int:user_id>', methods=['POST'])
def admin_delete_user(user_id):
    if not is_admin():
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    try:
        delete_user(user_id)  # Call the delete_user function
        flash('User deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error deleting user: {str(e)}", 'error')
    return redirect(url_for('admin_users'))

# Meditation Management
@app.route('/admin/meditations', methods=['GET', 'POST'])
def admin_meditations():
    if not is_admin():
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    search_query = request.args.get('search', '')
    try:
        meditations = get_all_meditations(search_query)
        categories = get_all_categories()
    except Exception as e:
        flash(f"Error retrieving meditations or categories: {str(e)}", 'error')
        meditations, categories = [], []

    if request.method == 'POST':
        try:
            category_id = request.form.get('category_id')
            text_content = request.form.get('text_content')
            audio_file_path = request.form.get('audio_file_path')

            insert_meditation(category_id, text_content, audio_file_path)
            flash('New meditation added successfully!', 'success')
        except Exception as e:
            flash(f"Error adding meditation: {str(e)}", 'error')
        return redirect(url_for('admin_meditations'))

    return render_template('admin/meditations.html', meditations=meditations, categories=categories, search_query=search_query)

@app.route('/admin/meditation/<int:meditation_id>', methods=['GET', 'POST'])
def admin_edit_meditation(meditation_id):
    if not is_admin():
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    try:
        meditation = get_meditation_by_id(meditation_id)
        if not meditation:
            flash('Meditation not found.', 'error')
            return redirect(url_for('admin_meditations'))
    except Exception as e:
        flash(f"Error retrieving meditation: {str(e)}", 'error')
        return redirect(url_for('admin_meditations'))

    if request.method == 'POST':
        try:
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
        except Exception as e:
            flash(f"Error updating meditation: {str(e)}", 'error')
        return redirect(url_for('admin_meditations'))

    return render_template('admin/edit_meditation.html', meditation=meditation)

@app.route('/admin/meditation/delete/<int:meditation_id>', methods=['POST'])
def admin_delete_meditation(meditation_id):
    if not is_admin():
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    try:
        delete_meditation(meditation_id)
        flash('Meditation deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error deleting meditation: {str(e)}", 'error')
    return redirect(url_for('admin_meditations'))

# Category Management
@app.route('/admin/categories', methods=['GET', 'POST'])
def admin_categories():
    if not is_admin():
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    search_query = request.args.get('search', '')
    try:
        categories = get_all_categories(search_query)
    except Exception as e:
        flash(f"Error retrieving categories: {str(e)}", 'error')
        categories = []

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            description = request.form.get('description')

            insert_category(name, description)
            flash('Category created successfully!', 'success')
        except Exception as e:
            flash(f"Error creating category: {str(e)}", 'error')
        return redirect(url_for('admin_categories'))

    return render_template('admin/categories.html', categories=categories, search_query=search_query)

@app.route('/admin/category/<int:category_id>', methods=['GET', 'POST'])
def admin_edit_category(category_id):
    if not is_admin():
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    try:
        category = get_category_by_id(category_id)
        if not category:
            flash('Category not found.', 'error')
            return redirect(url_for('admin_categories'))
    except Exception as e:
        flash(f"Error retrieving category: {str(e)}", 'error')
        return redirect(url_for('admin_categories'))

    if request.method == 'POST':
        try:
            name = request.form.get('name')
            description = request.form.get('description')

            update_category(category_id, name, description)
            flash('Category updated successfully!', 'success')
        except Exception as e:
            flash(f"Error updating category: {str(e)}", 'error')
        return redirect(url_for('admin_categories'))

    return render_template('admin/edit_category.html', category=category)

@app.route('/admin/category/delete/<int:category_id>', methods=['POST'])
def admin_delete_category(category_id):
    if not is_admin():
        flash('Access denied. Admins only.', 'error')
        return redirect(url_for('login'))

    try:
        delete_category(category_id)  # Call the delete_category function
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        flash(f"Error deleting category: {str(e)}", 'error')
    return redirect(url_for('admin_categories'))
