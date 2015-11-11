
# -*- coding: utf-8 -*-
import pytz
from common import db, UTCDateTime, Base
from datetime import datetime

class Notification(Base, db.Model):
    __tablename__ = "tbl_notification"

    ##############
    # Attributes #
    ##############
    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('tbl_activity.id'))

    is_read = db.Column(db.Boolean, default=False)
    #is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    updated_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))


    @classmethod
    def create(cls, activity_id, user_id):
        self = cls()

        self.user_id = user_id
        self.activity_id = activity_id

        db.session.add(self)
        #db.session.flush()

        return self

    def getMessage(self):
        return self.activity.getNotiMessage()

    def getOptionData(self):
        return self.activity.getOptionData()

    def format_json(self, fields=[]):
        all_fields = ["id", "is_read", "created_at", "updated_at"]
        response = self.returnJsonByFields(fields, all_fields)
        response.update({
            "detail": self.activity.to_json(),
            #"action_info": activity.getActionInfo(),
        })

        return response

    def markRead(self):
        self.is_read = True