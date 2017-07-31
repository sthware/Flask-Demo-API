import traceback
from http import HTTPStatus as codes
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import DBAPIError
from vgapi import APP, BUILDER, DB, BLUEPRINT, LOGGER
from vgapi.helpers.app_helper import GeneralValidationError
from vgapi.route_controllers.games_controller import NS as GAMES_NS
from vgapi.route_controllers.categories_controller import NS as CATS_NS

# Import management commands.
from vgapi.flask_commands import (
    reset_db,
    init_db,
    resetdb_command,
    initdb_command,
)

# Initialize app components.
BUILDER.init_app(BLUEPRINT)
BUILDER.add_namespace(GAMES_NS)
BUILDER.add_namespace(CATS_NS)
APP.register_blueprint(BLUEPRINT)
DB.init_app(APP)


# Set up global error handlers.
@BUILDER.errorhandler(NoResultFound)
def database_not_found_error_handler(e):
    LOGGER.warning(traceback.format_exc())
    return {'message': 'Item not found'}, 404


@BUILDER.errorhandler
def default_error_handler(e):
    message = 'An unhandled exception occurred.'
    LOGGER.exception(message)

    if not APP.config.FLASK_DEBUG:
        return {'message': message}, 500


@BUILDER.errorhandler(GeneralValidationError)
def validation_error_handler(e):
    LOGGER.warning(traceback.format_exc())
    return {'message': e.args[0]}, 400


@BUILDER.errorhandler(DBAPIError)
def database_general_handler(e):
    LOGGER.error(traceback.format_exc())
    return {'message': 'A general DB error occurred'}, 500
