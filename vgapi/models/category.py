""" Category models for the VG Game API """

from datetime import datetime
from vgapi import DB
from sqlalchemy.orm import validates
from vgapi.helpers.app_helper import GeneralValidationError
from vgapi.models.joins import games_categories

class Category(DB.Model):
    """ Category model """
    __tablename__ = 'categories'
    __table_args__ = {'schema': 'public'}
    NAME_LEN = 64
    NICK_LEN = 32
    DESC_LEN = 256

    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(NAME_LEN))
    nickname = DB.Column(DB.String(NICK_LEN), nullable=True)
    description = DB.Column(DB.String(DESC_LEN), nullable=True)

    def __init__(self, name, description=None, nickname=None):
        self.name = name

        if description:
            self.description = description

        if nickname:
            self.nickname = nickname

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

    @validates('nickname')
    def validate_nickname(self, key, val):
        val_len = len(val)

        if not (val_len > 0 and val_len <= self.NICK_LEN):
            raise GeneralValidationError(
                "Nickname length must be between 1 and {}, inclusive".format(
                    self.NICK_LEN
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
        return '<Category %r>' % self.name
