""" Game model for the VG Game API """

from datetime import datetime
from vgapi import DB, LOGGER
from sqlalchemy.orm import validates
from vgapi.helpers.app_helper import GeneralValidationError
from vgapi.models.joins import games_categories
from  sqlalchemy.schema import FetchedValue

class Game(DB.Model):
    """ Main game model """
    __tablename__ = 'games'
    __table_args__ = {'schema': 'public'}
    NAME_LEN = 256
    DESC_LEN = 2048
    MAX_CATEGORIES = 6

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(NAME_LEN))
    description = DB.Column(DB.String(DESC_LEN))
    pub_date = DB.Column(
        DB.DateTime,
        server_default=FetchedValue()
    )

    categories = DB.relationship(
        'Category',
        secondary=games_categories,
        backref='games',
        lazy='joined'
    )

    def __init__(self, name, description, pub_date=None, categories=None):
        self.name = name
        self.description = description

        if pub_date:
           self.pub_date = pub_date

        if categories:
            self.categories = categories

    @validates('name')
    def validate_name(self, key, val):
        val_len = len(val)

        if not (val_len > 0 and val_len <= self.NAME_LEN):
            raise GeneralValidationError(
                "Name length must be between 1 and {}, inclusive".format(
                    self.NAME_LEN
                )
            )

        return val

    @validates('description')
    def validate_description(self, key, val):
        val_len = len(val)

        if not (val_len > 0 and val_len <= self.DESC_LEN):
            raise GeneralValidationError(
                "Description length must be between 1 and {}, inclusive".format(
                    self.DESC_LEN
                )
            )

        return val

    def __repr__(self):
        return '<Game %r>' % self.name
