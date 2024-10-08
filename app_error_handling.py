import logging
from flask import flash, render_template
from werkzeug.routing import BuildError
from jinja2.exceptions import TemplateNotFound
from mod_utilize import app

# Configure logging
logging.basicConfig(level=logging.ERROR)

# Custom error handler for TemplateNotFound
@app.errorhandler(TemplateNotFound)
def template_not_found(error):
    logging.error(f"TemplateNotFound: {error}")
    error_type = "template_not_found"
    return render_template('error_page.html', error_type=error_type), 404

# Custom error handler for 404 - Page Not Found
@app.errorhandler(404)
def page_not_found(error):
    logging.error(f"404 Error: {error}")
    error_type = "page_not_found"
    return render_template('error_page.html', error_type=error_type), 404

# Custom error exception handler
@app.errorhandler(Exception)
def exception(error):
    logging.error(f"Exception: {error}")
    error_type = "exception"
    return render_template('error_page.html', error_type=error_type), 500

# Custom error handler for BuildError
@app.errorhandler(BuildError)
def build_error(error):
    logging.error(f"BuildError: {error}")
    error_type = "build_error"
    return render_template('error_page.html', error_type=error_type), 500

# Custom error handler for 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    logging.error(f"500 Error: {error}")
    error_type = "internal_server_error"
    return render_template('error_page.html', error_type=error_type), 500