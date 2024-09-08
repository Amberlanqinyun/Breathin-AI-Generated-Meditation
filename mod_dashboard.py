from flask import render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
from mod_utilize import app
from mod_db_achievements import get_user_achievements, get_user_meditation_history
from mod_db_account import get_user_profile
from mod_db_meditation import search_meditations  # Assuming this is where your DB query is

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    """
    Render the user dashboard page, displaying profile information, meditation history, achievements, and usage reports.
    Includes a search functionality for meditations.
    """
    user_id = session.get('user_id')

    if not user_id:
        flash("Please log in to access the dashboard.", "error")
        return redirect(url_for('login'))

    try:
        # Fetch user profile, meditation history, and achievements
        user_profile = get_user_profile(user_id)
        meditation_history = get_user_meditation_history(user_id)
        achievements = get_user_achievements(user_id)

        # Handle search input
        search_query = request.args.get('search_query', '')
        if search_query:
            # Perform search based on query
            search_results = search_meditations(search_query)
        else:
            search_results = []  # No search results if no query

        # Prepare heatmap data (last year)
        today = datetime.now().date()
        start_date = today - timedelta(days=365)
        days_practiced = {session['SessionDateTime'].date() for session in meditation_history}
        heatmap_data = [(start_date + timedelta(days=i)) in days_practiced for i in range(365)]

    except Exception as e:
        flash(f"An error occurred while fetching data: {str(e)}", "error")
        return redirect(url_for('login'))

    return render_template(
        'dashboard.html',
        user_profile=user_profile,
        meditation_history=meditation_history,
        achievements=achievements,
        heatmap_data=heatmap_data,
        search_results=search_results,  # Pass the search results to the template
        search_query=search_query,      # Pass the search query back to the template
        datetime=datetime
    )
