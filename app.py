
# from app_error_handling import template_not_found, build_error, exception, internal_server_error, page_not_found
from db_baseOperation import execute_query
# from db_orderDataInsert import insertPaymentAndCompletedOrder
from mod_contact_us import contact_us
from mod_create_account import create_account, create_customer_account
from mod_dashboard import dashboard
from mod_login_logout import login, logout
from mod_register import register
from mod_send_news import send_news
from mod_update_customer import update_customer
from mod_update_password import update_password
from mod_update_staff import update_staff
from mod_utilize import flash, render_template, request, app
from mod_view_customers import view_customers
from mod_view_notification import view_notification
from mod_view_profile import view_profile
from mod_view_staffs import view_staffs



# Function for showing the homepage
@app.route('/')
def index():
    return render_template('homepage.html')

# Run the app in debug mode
if __name__ == '__main__':
    app.run(debug=True)
