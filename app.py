import logging
import sys
import traceback
from dotenv import load_dotenv
from flask import redirect
from flask import request, jsonify, send_file, make_response
from marshmallow import ValidationError

from paraphrasing_bot.app import app
from paraphrasing_bot.src.domain.exceptions.HandledWithMessageException import HandledWithMessageException
from paraphrasing_bot.src.services import Config
from paraphrasing_bot.src.routes.generic import generic_blueprint
from paraphrasing_bot.src.applications.Bootstrap import Bootstrap as BootstrapApplication

# Load the .env file in case that it has been used to set envs
# instead of injecting them through docker
load_dotenv('.env')

app_config = Config.Config()

# Applications

custom_logger = logging.getLogger("paraphrasing_bot")


@app.before_request
def log_request_info():
    request_data = {
        "headers": dict(request.headers),
        "body": request.get_data()
    }
    custom_logger.debug(request_data)


@app.before_first_request
def initial_setup():
    BootstrapApplication()


# Loading blueprints
app.register_blueprint(generic_blueprint)


# Catch all exceptions
# Any exception not caught by the routes above will be handled here
@app.errorhandler(Exception)
def all_exception_handler(error: Exception):
    custom_logger.error(error)

    error_type = error.__class__.__name__
    status_code = 500
    message = "Ha ocurrido un error inesperado, por favor intente de nuevo. Si el problema persiste contacte al administrador del sistema."

    if isinstance(error, HandledWithMessageException):
        message = str(error)

    if isinstance(error, ValidationError):
        message = str(error)
        status_code = 400

    response = {
        "message": message
    }

    if app_config.DEV_MODE:
        cosa = traceback.format_exc()
        custom_logger.debug(cosa)

        response["error"] = str(error)
        response["stacktrace"] = cosa

    return jsonify(response), status_code


if __name__ == "__main__":
    app.run(host=app_config.APP_HOST, port=app_config.APP_PORT, debug=app_config.DEV_MODE)
