from common import db, UTCDateTime, Base
from app.utils import helper
import pytz
import hashlib
import uuid
import time
from datetime import datetime
import bcrypt


class UserToken(Base, db.Model):
    __tablename__ = "tbl_user_token"

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    updated_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))

    user_id = db.Column(db.Integer, db.ForeignKey('tbl_user.id'))
    device_id = db.Column(db.UnicodeText())
    access_token = db.Column(db.UnicodeText())
    is_active = db.Column(db.Boolean, default=True)

    # TODO: Store push notification end points separately
    DEVICE_TYPE_APNS = u"apns"      # iOS
    DEVICE_TYPE_GCM = u"gcm"        # Android
    device_type = db.Column(db.Enum([DEVICE_TYPE_APNS, DEVICE_TYPE_GCM], native_enum=False), nullable=True, default=DEVICE_TYPE_APNS)

    device_token = db.Column(db.Unicode())

    unhashed_token = ''

    #################
    # Class methods #
    #################
    # find UserToken instance by access token and device, use for authentication
    @classmethod
    def findByTokenAndDevice(cls, access_token, device_id):
        user_token = cls.query.filter(
            cls.device_id == device_id,
            cls.is_active == True
        ).first()

        if user_token and bcrypt.hashpw(access_token, user_token.access_token) == user_token.access_token:
            return user_token
        else:
            return None

    @classmethod
    def create(cls, user_id, device_id):
        # mark inactive other tokens with same device
        cls.findAllByAttributes(device_id = device_id).update(dict(is_active=False))
        cls.findAllByAttributes(user_id = user_id).update(dict(is_active=False))

        # active token again
        token = cls.findByAttributes(user_id = user_id, device_id = device_id)
        if not token:
            token = cls()
            token.user_id = user_id
            token.device_id = device_id

        # Always regenerate new token
        h = hashlib.sha256(str(uuid.uuid4()))
        h.update(str(user_id))

        epoc = int(time.time())
        h.update(str(epoc))

        # origin
        token.unhashed_token = helper.uni(h.hexdigest().upper())

        # hash it
        token.access_token = bcrypt.hashpw(token.unhashed_token, bcrypt.gensalt(10))

        # active the token
        token.is_active = True

        db.session.add(token)
        return token


    # def update(self, data):
    #     device_token = data['device_token']
    #     self.device_token = device_token
    #
    #     device_type = helper.get(data, 'device_type', UserToken.DEVICE_TYPE_APNS)
    #     if device_type in [UserToken.DEVICE_TYPE_APNS, UserToken.DEVICE_TYPE_GCM]:
    #         self.device_type = device_type
    #
    #     return True, ''