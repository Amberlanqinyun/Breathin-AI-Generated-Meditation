from flask import flash, render_template
from werkzeug.routing import BuildError
from jinja2.exceptions import TemplateNotFound
import openai
from mod_utilize import app
from openai import InvalidRequestError, OpenAIError

# Custom error handler for TemplateNotFound
@app.errorhandler(TemplateNotFound)
def template_not_found(error):
    error_type = "template_not_found"
    return render_template('error_page.html', error_type=error_type), 404

# Custom error handler for 404 - Page Not Found
@app.errorhandler(404)
def page_not_found(error):
    error_type = "page_not_found"
    return render_template('error_page.html', error_type=error_type), 404


# Custom error handler for InvalidRequestError
@app.errorhandler(InvalidRequestError)
def handle_invalid_request_error(error):
    error_type = "invalid_request_error"
    return render_template('error_page.html', error_type=error_type, error_message=str(error)), 400

# Custom error exception handler
@app.errorhandler(Exception)
def exception(error):
    error_type = "exception"
    return render_template('error_page.html', error_type=error_type), 500

# Custom error handler for BuildError
@app.errorhandler(BuildError)
def build_error(error):
    error_type = "build_error"
    return render_template('error_page.html', error_type=error_type), 500

# Custom error handler for 500 - Internal Server Error
@app.errorhandler(500)
def internal_server_error(error):
    error_type = "internal_server_error"
    return render_template('error_page.html', error_type=error_type), 500
