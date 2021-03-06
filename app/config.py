"""
Config module
"""
import os
import logging
from pathlib import Path


SECRET_KEY = ''
DO_NOT_WRITE_BYTECODE = False
LOGGING_LEVEL = logging.INFO

POSTS_PER_PAGE = 10
DEFAULT_DATE_FORMAT = '%d/%m/%Y'
SLUG_DATE_FORMAT = '%d-%m-%y'

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), os.pardir))

ROOT_FOLDER = Path(PROJECT_DIR)
STATIC_FOLDER = ROOT_FOLDER / 'static'
TEMPLATES_DIR = ROOT_FOLDER / 'templates'

# Standalone run
RUN_HOST = '127.0.0.1'
RUN_PORT = 8031
DEBUG = False
RELOADER = False

# Database
DB_HOST = '127.0.0.1'
DB_PORT = 3306
DB_USER = 'bmwlog'
DB_PASS = 'Qwerty12#45'  # yes, it's a prod credentials
DB_NAME = 'bmwlogdb'

# Override values from config_local.py if exists
try:
    from . import config_local
    for key, value in config_local.__dict__.items():
        if key.isupper() and key in globals():
            globals()[key] = value
except ImportError:
    pass

# Override values from environment
for key, value in globals().copy().items():
    if key.isupper() and key in os.environ:
        globals()[key] = os.environ[key]
