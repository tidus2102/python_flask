# -*- coding: utf-8 -*-
import pytz
from common import db, UTCDateTime, Base
from datetime import datetime
from app.utils import helper
from sqlalchemy.event import listen
from flask import current_app as app, url_for

class Photo(Base, db.Model):
    __tablename__ = "tbl_photo"
    ##############
    # Attributes #
    ##############
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    updated_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))

    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))
    file_name = db.Column(db.UnicodeText())
    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    updated_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    is_deleted = db.Column(db.Boolean, default=False)

    # Relations
    # photo = db.relationship('Photo', backref='user', lazy='dynamic', foreign_keys='User.photo_id', order_by='Paty.id')


    ####################
    # Instance methods #
    ####################
    def __init__(self, sender_id):
        self.sender_id = sender_id

    # format response data
    def format_json(self, fields=[]):
        all_fields = ["id", "name", "created_at", "updated_at", "is_deleted"]
        json = self.returnJsonByFields(all_fields, fields)
        json.update({
            "sender_info": self.sender.format_basic_profile_json(),
        })
        return json

    # Check if the owner
    def isOwner(self, user_id):
        return self.user_id != user_id

    # Update photo image: create new if new photo, update current image if exist
    def updateImage(self, image):
        helper.updateImage(self, "name", image, "photo")

    # Return path
    def getPhotoUrl(self, size='origin'):
        config = app.config
        if not self.name:
            # return default avatar image
            return "%s%s" % (config.get("ENDPOINT"), url_for('static', filename='img/default_photo.png'))
        return "%s%s%s" % (config.get("PROTOCOL"), config.get("ENDPOINT"), url_for('static', filename="uploads/photo/%s/%s" %(size, self.name)))

    #################
    # Class methods #
    #################
    @classmethod
    def create(cls, sender_id):
        photo = Photo(sender_id)
        db.session.add(photo)
        return photo

    # Delete image file on disk
    @staticmethod
    def deletePhoto(mapper, connect, self):
        helper.deleteImage(self.name, app.config, "photo")

# Register event to trigger when entry is deleted
listen(Photo, "after_delete", Photo.deletePhoto)
