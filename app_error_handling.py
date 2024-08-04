
# Import various modules created for and used in this python srcipt
from meditator import app, flash, render_template
from werkzeug.routing import BuildError
from jinja2.exceptions import TemplateNotFound


# Custom error handler for TemplateNotFound
@app.errorhandler(TemplateNotFound)
def template_not_found(error):
    # Create error type variable for displaying on error page, then render it for use
    error_type = "template_not_found"
    return render_template('error_page.html', error_type=error_type), 404


# Custom error handler for 404 - Page Not Found
@app.errorhandler(404)
def page_not_found(error):
    # Create error type variable for displaying on error page, then render it for use
    error_type = "page_not_found"
    return render_template('error_page.html', error_type=error_type), 404


# Custom error exception handler
@app.errorhandler(Exception)
def exception(error):
    # Create error type variable for displaying on error page, then render it for use
    error_type = "exception"
    return render_template('error_page.html', error_type=error_type), 500


# Custom error handler for BuildError
@app.errorhandler(BuildError)
def build_error(error):
    # Create error type variable for displaying on error page, then render it for use
    error_type = "build_error"
    return render_template('error_page.html', error_type=error_type), 500


# Custom error handler for 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    # Create error type variable for displaying on error page, then render it for use
    error_type = "internal_server_error"
    return render_template('error_page.html', error_type=error_type), 500