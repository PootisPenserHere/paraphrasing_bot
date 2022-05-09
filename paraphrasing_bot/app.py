import logging.config
from datetime import timedelta
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_log_request_id import RequestID, RequestIDLogFilter
from logging.handlers import RotatingFileHandler

from paraphrasing_bot.src.services import Config

app_config = Config.Config()

app = Flask(__name__, static_folder='static')

cors = CORS(app, expose_headers=["Content-Disposition"])
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%s:%s@%s:%i/%s' % (
    app_config.POSTGRES_USER,
    app_config.POSTGRES_PASSWORD,
    app_config.POSTGRES_HOST,
    app_config.POSTGRES_PORT,
    app_config.POSTGRES_DB
)

# Print queries in dev mode
app.config['SQLALCHEMY_ECHO'] = app_config.DEV_MODE

app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_recycle': app_config.SQLALCHEMY_POOL_RECYCLE,
    'pool_timeout': app_config.SQLALCHEMY_POOL_TIMEOUT,
    'pool_size': app_config.SQLALCHEMY_POOL_SIZE,
    'max_overflow': app_config.SQLALCHEMY_POOL_MAX_OVERFLOW,
}

db = SQLAlchemy(app, session_options={'autocommit': True})
migrate = Migrate(app, db, compare_type=True)

# Will add a unique identifier to each request
RequestID(app)

# Initializing the logger object
logger = logging.getLogger()
logger.setLevel(logging.DEBUG if app_config.DEV_MODE else logging.INFO)

# Configuring the log to stream to stdout
stream_handler = logging.StreamHandler()
stream_formatter = logging.Formatter(
    '%(asctime)-15s %(request_id)-36s %(levelname)-8s %(message)s')
stream_handler.setFormatter(stream_formatter)
stream_handler.addFilter(RequestIDLogFilter())
logger.addHandler(stream_handler)

# Configuring the log output to a file in json format
file_handler = RotatingFileHandler('/var/log/paraphrasing_bot/app.json', maxBytes=100 * 1024 * 1024, backupCount=10, mode='a',
                                   encoding='utf-8')
file_formatter = logging.Formatter(
    '{"timestamp":"%(created)f", '
    '"time":"%(asctime)s", '
    '"name": "%(name)s", '
    '"request_id":"%(request_id)s", '
    '"level": "%(levelname)s", '
    '"caller_function": "%(funcName)s", '
    '"script_path": "%(pathname)s", '
    '"message": "%(message)s"}')
file_handler.setFormatter(file_formatter)
file_handler.addFilter(RequestIDLogFilter())
logger.addHandler(file_handler)
