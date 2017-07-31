"""

TODO: 

    iTunes integration
    options method
    OAuth2:
    https://hub.docker.com/r/frolvlad/flask-restplus-server-example/
    migrations
    docker
    tests
    make
    docs

Sources, specs, insiprations, and guides:

    https://tools.ietf.org/html/rfc7231.html#section-6.5.6
    http://my.safaribooksonline.com/book/web-development/9781449359713
    https://www.owasp.org/index.php/REST_Security_Cheat_Sheet
    http://flask-restplus.readthedocs.io/en/latest/
    https://www.slideshare.net/stormpath/secure-your-rest-api-the-right-way?next_slideshow=1
    http://michal.karzynski.pl/blog/2016/06/19/building-beautiful-restful-apis-using-flask-swagger-ui-flask-restplus/
    https://stormpath.com/blog/secure-your-rest-api-right-way
    https://www.slideshare.net/rnewton/best-practices-you-must-apply-to-secure-your-apis
    https://flask-oauthlib.readthedocs.io/en/latest/#flask-oauthlib


"""
import os
import logging
import traceback
import click
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restplus import Api

APP_MODE = (os.environ.get('VGAPI_MODE', None) or 'dev').capitalize()
APP_NAME = 'vgapi'
APP = Flask(APP_NAME)
APP.config.from_object('vgapi.default_settings.{}Config'.format(APP_MODE))
APP.config.from_envvar('VGAPI_SETTINGS', silent=True)
APP.url_map.strict_slashes = False
BLUEPRINT = Blueprint('api', APP_NAME, url_prefix='/api')
DB = SQLAlchemy(APP)
LOGGER = logging.getLogger(APP_NAME)
LOG_HANDLER = logging.FileHandler(APP.config['LOG_FILE'])
LOGGER.addHandler(LOG_HANDLER)
LOGGER.setLevel(logging.DEBUG)

# Uncomment if you'd like to log server-generated messages separately.
# SERVER_LOGGER = logging.getLogger('werkzeug')
# SERVER_LOG_HANDLER = logging.FileHandler(APP.config['SERVER_LOG_FILE'])
# SERVER_LOGGER.addHandler(SERVER_LOG_HANDLER)
# SERVER_LOGGER.setLevel(logging.DEBUG)

BUILDER = Api(
    version=APP.config['API_VERSION'],
    title='Games DB API',
    description='Demo Games DB API',
)
