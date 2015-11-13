from common import db, UTCDateTime, Base
import pytz
from datetime import datetime

class Notification(Base, db.Model):
    __tablename__ = "tbl_notification"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    updated_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))

    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('tbl_activity.id'))

    is_read = db.Column(db.Boolean, default=False)
    #is_deleted = db.Column(db.Boolean, default=False)


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

    def markRead(self):
        self.is_read = True