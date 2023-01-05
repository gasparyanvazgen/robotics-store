from flask import Blueprint
from .handlers import handle_forbidden

errors = Blueprint('errors', __name__)

# Register error handling functions
errors.app_errorhandler(403)(handle_forbidden)
