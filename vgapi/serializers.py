from flask_restplus import fields
from vgapi import BUILDER

category_item = BUILDER.model('Category', {
    'id': fields.Integer(
        readOnly=True,
        description='Unique ID for category'
    ),
    'name': fields.String(required=True, description='Category name'),
    'nickname': fields.String(required=False, description='Category nickname'),
    'description': fields.String(
        required=True,
        description='Category description'
    ),
})

base_game_item = BUILDER.model('Game', {
    'id': fields.Integer(
        readOnly=True,
       description='Game ID'
    ),

    'name': fields.String(required=True, description='Game name'),
    'description': fields.String(required=True, description='Game description'),

    # Automatically set to the current date and time in the DB if not set.
    'pub_date': fields.DateTime(description='Publication date'),

})

list_game_item = BUILDER.inherit('Game output item', base_game_item, {

    'categories': fields.List(fields.Integer(attribute='id'))

})

game_item = BUILDER.inherit('Game item', base_game_item, {

    'categories': fields.List(fields.Nested(category_item)),

})

pagination = BUILDER.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(
        description='Number of items per page of results'
    ),
    'total': fields.Integer(description='Total number of results'),
})

games_collection = BUILDER.inherit(
    'Page of game entries',
    pagination, 
    {
        'items': fields.List(fields.Nested(list_game_item))
    }
)

