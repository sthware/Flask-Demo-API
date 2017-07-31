""" Router and controller for Game items. """

from http import HTTPStatus as codes
from flask import request
from flask_restplus import Resource
from vgapi import BUILDER, DB
from vgapi.models.game import Game
from vgapi.models.category import Category
from vgapi.helpers.query_string_parsers import pagination_args
from vgapi.helpers.app_helper import (
        set_fields,
        GeneralValidationError,
        X_WARNINGS_KEY,
        X_WARNINGS_DESC,
        check_unsupported_fields,
)

from vgapi.serializers import (
        game_item,
        list_game_item,
        games_collection
)

NS = BUILDER.namespace(
    'games',
    description='Operations related to game entries'
)

ROUTER = NS.route
NAME_FIELD = 'name'
DESCRIPTION_FIELD = 'description'
CATEGORIES_FIELD = 'categories'
UPDATEABLE_FIELDS = (NAME_FIELD, DESCRIPTION_FIELD)
VALID_FIELDS =  set([*UPDATEABLE_FIELDS, CATEGORIES_FIELD])

def set_categories(game, category_ids):
    """ Sets categories on a game object
    Args:
        game -- Game model instance
        category_ids -- list of category ids

    Returns: None

  """
    categories = []

    if not category_ids:
        return

    game.categories = []

    for category_id in category_ids:
        category = Category.query.get(category_id)

        if not category:
            raise GeneralValidationError(
                "'{}' is not a valid category ID".format(category_id)
            )

        categories.append(category)

    game.categories = categories


@ROUTER('/')
class GamesCollection(Resource):
    """ Lists all games, allows adding new ones to system. """

    @BUILDER.expect(pagination_args)
    @BUILDER.marshal_with(games_collection)
    def get(self):
        """ Returns a list of all games. """
        args = pagination_args.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 1)

        return Game.query.paginate(page, per_page, error_out=False)

    @NS.expect(list_game_item)
    @BUILDER.response(codes.CREATED, 'Game created')
    @BUILDER.header(X_WARNINGS_KEY, X_WARNINGS_DESC)
    def post(self):
        """ Creates a new game item. """
        game = None
        req_data = request.json
        name = req_data.get(NAME_FIELD)
        description = req_data.get(DESCRIPTION_FIELD)
        category_ids = req_data.get(CATEGORIES_FIELD)
        passed_fields = req_data.keys()
        category_ids = req_data.get(CATEGORIES_FIELD)

        message = check_unsupported_fields(passed_fields, VALID_FIELDS)

        if message:
            x_warnings.append(message)

        game = Game(name, description)
        set_categories(game, category_ids)

        DB.session.add(game)
        DB.session.commit()
        return None, codes.CREATED


@ROUTER('/<int:game_id>')
@BUILDER.response(codes.NOT_FOUND, 'Game not found')
class GameItem(Resource):
    """ Single game item management methods. """

    @BUILDER.marshal_with(list_game_item)
    def get(self, game_id):
        """ Returns a single game item """
        return Game.query.filter(Game.id == game_id).one()

    def do_update(self, game_id):
        """ Updates an existing game item.

        Args:
            game_id
        Returns:
            A tuple with the follow values:
            None
            x_warnings -- list of strings containing warnings to be
            placed in special warnings header

    """

        x_warnings = []
        fields_diff = None
        game = Game.query.filter(Game.id == game_id).one()
        req_data = request.json
        passed_fields = req_data.keys()
        category_ids = req_data.get(CATEGORIES_FIELD)
        message = ''

        set_fields(game, req_data, UPDATEABLE_FIELDS)
        set_categories(game, category_ids)

        DB.session.add(game)
        DB.session.commit()

        message = check_unsupported_fields(passed_fields, VALID_FIELDS)

        if message:
            x_warnings.append(message)

        return None, x_warnings

    @BUILDER.response(codes.NO_CONTENT, 'Game updated')
    @BUILDER.header(X_WARNINGS_KEY, X_WARNINGS_DESC)
    def patch(self, game_id):
        """ Partially updates a game item. """
        ret = None
        x_warnings = []

        ret, x_warnings = self.do_update(game_id)

        return None, codes.NO_CONTENT, {X_WARNINGS_KEY: x_warnings}

    @BUILDER.expect(game_item)
    @BUILDER.response(codes.NO_CONTENT, 'Game updated')
    @BUILDER.header(X_WARNINGS_KEY, X_WARNINGS_DESC)
    def put(self, game_id):
        """ Fully updates a game item. """
        ret = None
        x_warnings = []

        ret, x_warnings = self.do_update(game_id)

        return None, codes.NO_CONTENT, {X_WARNINGS_KEY: x_warnings}

    @BUILDER.response(codes.NO_CONTENT, 'Game deleted')
    def delete(self, game_id):
        """ Deletes a game item. """
        game = Game.query.filter(Game.id == game_id).one()

        DB.session.delete(game)
        DB.session.commit()

        return None, codes.NO_CONTENT
