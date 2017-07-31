""" Router and controller for Category items. """
from flask import request
from flask_restplus import Resource
from http import HTTPStatus as codes
from vgapi import BUILDER, LOGGER, DB
from vgapi.models.category import Category
from vgapi.serializers import category_item
from vgapi.helpers.app_helper import (
        set_fields,
        GeneralValidationError,
        X_WARNINGS_KEY,
        X_WARNINGS_DESC
)

NS = BUILDER.namespace(
    'categories',
    description='Operations related to categories'
)

ROUTER = NS.route


@ROUTER('/')
class CategoryCollection(Resource):
    """ Lists all categories, allows adding new ones to system. """

    @BUILDER.marshal_list_with(category_item)
    def get(self):
        """ Returns a list of all categories. """
        categories = Category.query.all()
        return categories

    @BUILDER.response(codes.CREATED, 'Category successfully created')
    @BUILDER.expect(category_item)
    def post(self):
        """ Creates a new category. """
        req_data = request.json
        name = req_data.get('name')
        nickname = req_data.get('nickname')
        description = req_data.get('description')
        category = Category(name, description, nickname)

        DB.session.add(category)
        DB.session.commit()
        return None, codes.CREATED


@ROUTER('/<int:category_id>')
@BUILDER.response(codes.NOT_FOUND, 'Category not found')
class CategoryItem(Resource):
    UPDATEABLE_FIELDS = ('name', 'nickname', 'description')

    def do_update(self, category_id):
        """ Updates an existing category item.

        Args:
            category_id 
        Returns:
            A tuple with the follow values:
            None
            x_warnings -- list of strings containing warnings to be
            placed in special warnings header

    """

        x_warnings = []
        fields_diff = None
        category = Category.query.filter(Category.id == category_id).one()
        req_data = request.json
        passed_fields = req_data.keys()
        valid_fields = set(CategoryItem.UPDATEABLE_FIELDS)

        set_fields(category, req_data, CategoryItem.UPDATEABLE_FIELDS)

        DB.session.add(category)
        DB.session.commit()

        # Warn API users about unsupported fields they've passed us.
        fields_diff = set(passed_fields) - valid_fields

        if fields_diff:
            x_warnings.append("Unupported fields: {}".format(fields_diff))

        return None, x_warnings

    @BUILDER.marshal_with(category_item)
    def get(self, category_id):
        """ Get a single category item """
        return Category.query.filter(Category.id == category_id).one()

    @BUILDER.response(codes.NO_CONTENT, 'Category updated')
    @BUILDER.header(X_WARNINGS_KEY, X_WARNINGS_DESC)
    def patch(self, category_id):
        """ Partially updates a category item. """
        ret = None
        x_warnings = []

        ret, x_warnings = self.do_update(category_id)

        return None, codes.NO_CONTENT, {X_WARNINGS_KEY: x_warnings}

    @BUILDER.expect(category_item)
    @BUILDER.response(codes.NO_CONTENT, 'Category updated')
    @BUILDER.header(X_WARNINGS_KEY, X_WARNINGS_DESC)
    def put(self, category_id):
        """ Fully updates a category item. """
        ret = None
        x_warnings = []

        ret, x_warnings = self.do_update(category_id)

        return None, codes.NO_CONTENT, {X_WARNINGS_KEY: x_warnings}

    @BUILDER.response(codes.NO_CONTENT, 'Category deleted')
    def delete(self, category_id):
        """ Deletes a category item. """
        category = Category.query.filter(Category.id == category_id).one()

        DB.session.delete(category)
        DB.session.commit()
        return None, codes.NO_CONTENT
