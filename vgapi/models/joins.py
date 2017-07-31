from vgapi import DB
from sqlalchemy.ext.declarative import declarative_base

# Represents the join relationship (and table) between categories and games.
games_categories = DB.Table(
    'games_categories',
    DB.metadata,
    DB.Column(
        'game_id',
        DB.Integer,
        DB.ForeignKey('public.games.id'),
        nullable=False,
    ),

    DB.Column(
        'category_id',
        DB.Integer,
        DB.ForeignKey('public.categories.id'),
        nullable=False,
    ),
    DB.PrimaryKeyConstraint('game_id', 'category_id'),
    schema='public'
)
