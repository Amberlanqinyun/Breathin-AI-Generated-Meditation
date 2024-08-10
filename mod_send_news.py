# GROUP 2 PROJECT 2

# Import necessary modules and functions
from mod_utilize import  app, flash, session, redirect, url_for, render_template, request
from db_baseOperation import execute_query

# Route to update news for all members and staff
@app.route('/send_news', methods=['GET', 'POST'])
def send_news():
    # Ensure randoms can't access the page
    if 'user_id' not in session:
        return redirect(url_for('login'))
    # If not an admin, redirect to dashboard
    role_id = session.get('role_id')
    if role_id != 3:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        # Get the news text from the form
        news_text = request.form['news_text']

        # Update the news column for all members and staff in the database
        update_query = "UPDATE customers SET news = %s"
        execute_query(update_query, (news_text,))
        update_query = "UPDATE staff SET news = %s"
        execute_query(update_query, (news_text,))

        # Display success message
        flash('News successfully sent to all customers and staff.')

    return render_template('send_news.html')
