from flask_restplus import reqparse

pagination_args = reqparse.RequestParser(bundle_errors=True)
pagination_choices = [2, 10, 50, 100, 500]

pagination_args.add_argument(
    'page',
    type=int,
    required=False,
    default=1,
    help='Page number must be numeric'
)

pagination_args.add_argument(
    'per_page',
    type=int,
    required=False,
    choices=pagination_choices,
    default=10,
    help='per_page must be one of {}'.format(pagination_choices)
)
