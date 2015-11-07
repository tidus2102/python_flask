# -*- coding: utf-8 -*-
import pytz
import bcrypt
from datetime import datetime
from common import db, UTCDateTime, Base
from app.models.user_token import UserToken
from flask.ext.login import UserMixin
from flask import current_app as app, url_for
from app.utils import helper
from sqlalchemy import and_, or_

class User(UserMixin, Base, db.Model):
    __tablename__ = "tbl_user"

    ##############
    # Attributes #
    ##############
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.UnicodeText())
    first_name = db.Column(db.UnicodeText())
    last_name = db.Column(db.UnicodeText())
    username = db.Column(db.UnicodeText())
    email = db.Column(db.UnicodeText(), unique=True)
    password = db.Column(db.UnicodeText())
    birthday = db.Column(db.UnicodeText())
    facebook_id = db.Column(db.UnicodeText(), unique=True)
    facebook_token = db.Column(db.UnicodeText())
    secret_token = db.Column(db.UnicodeText(), unique=True)

    STATUS_UNACTIVATED = u"unactivated"
    STATUS_ACTIVATED = u"activated"
    status = db.Column(db.Enum([
        STATUS_UNACTIVATED, STATUS_ACTIVATED
    ], native_enum=False), nullable=False, default=STATUS_UNACTIVATED)
    updated_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))
    created_at = db.Column(UTCDateTime, default=lambda: pytz.UTC.localize(datetime.utcnow()))

    # Relations
    user_tokens = db.relationship('UserToken', backref='user', lazy='dynamic', foreign_keys='UserToken.user_id', order_by='UserToken.id')

    ####################
    # Instance methods #
    ####################
    def __repr__(self):
        return '<User id: %s, full_name: %s>' % (self.id, self.full_name)

    # Contruction
    def __init__(self, username, email, password):
        self.username = username
        self.email = email

        # TODO: Update this when user register by email, password
        #self.password = self._hash_password(helper.generate_string())
        if not password:
            self.password = self._hash_password(helper.generate_string())
        else:
            self.password = self._hash_password(password)

        self.secret_token = helper.generate_string()

        # TODO: Also update this later
        self.status = self.STATUS_ACTIVATED

    # # Update user avatar: create new if new user, update current avatar if exist
    # def updateAvatar(self, avatar):
    #     updateImage(self, "avatar", avatar, "avatar")

    # Hash the pasword
    def _hash_password(self, password):
        return bcrypt.hashpw(
            password,
            bcrypt.gensalt(12))

    # Return path
    # def getAvatar(self, size='origin'):
    #     avatar_sizes = app.config["IMG_SIZES"]["avatar"]
    #
    #     if not self.avatar:
    #         # return default avatar image
    #         return url_for('static', filename='img/default_avatar.png')
    #     return "%s?width=%s&height=%s" % (self.avatar, avatar_sizes[size], avatar_sizes[size])

    # Update avatar
    def updateAvatar(self):
        self.avatar = "http://graph.facebook.com/%s/picture" % (self.fb_id)

    # Return full url of avatar
    # def getFullAvatarUrl(self, size='origin'):
    #     return "%s%s/avatar/%s?type=%s" % ('http://', app.config['ENDPOINT'], self.id, size)
    #     # return 'http://' + app.config['ENDPOINT'] + "/avatar/" + self.id + "?type=" + size

    # Format data return for logged user with tokens
    def format_json(self, user_token):
        info = self.format_profile_json()
        info["access_token"] = user_token.access_token
        info["device_id"] = user_token.device_id
        return info

    def format_login_json(self, user_token):
        return {
            "id": self.id,
            "access_token": user_token.unhashed_token,
            "device_id": user_token.device_id
        }

    # Format data for profile of user
    def format_profile_json(self, fields=[]):
        all_fields = ["id", "first_name", "last_name", "email"]
        return self.returnJsonByFields(all_fields, fields)

    # Format basic data for profile of user that used in other places
    def format_basic_profile_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            #"fb_id": self.fb_id,
        }

    # Get list paties by status
    # def getPatiesByStatus(self, status='all'):
    #     if status == 'all':
    #         return Paty.query.join(PatyMember, Paty.id == PatyMember.paty_id).filter(PatyMember.user_id == self.id)
    #     else:
    #         return Paty.query.join(PatyMember, Paty.id == PatyMember.paty_id).filter(
    #             and_(PatyMember.user_id == self.id, Paty.status == status))

    # Get friend with
    # def getFriend(self, user_id):
    #     return Friend.query.filter(Friend.user1_id == self.id, Friend.user2_id == user_id).first()

    # Check current user instance is friend with checked user_id
    # def isFriendWith(self, user_id):
    #     return True if self.getFriend(user_id) else False

    # Get friends list
    # def getFriends(self):
    #     return Friend.query.filter(Friend.user1_id == self.id)

    # Get friends list by status
    # def getFriendsBy(self, status):
    #     if status == "all":
    #         return self.getFriends()
    #
    #     return Friend.query.filter(
    #         and_(
    #             Friend.user1_id == self.id,
    #             Friend.status == status,
    #         )
    #     )

    # Add new friendship
    # def addFriend(self, friend_id):
    #     if User.findById(friend_id) and not self.isFriendWith(friend_id):
    #         friend_entry1 = Friend(self.id, friend_id, Friend.STATUS_ACTIVE)
    #         friend_entry2 = Friend(friend_id, self.id, Friend.STATUS_ACTIVE)
    #         db.session.add(friend_entry1)
    #         db.session.add(friend_entry2)
    #         db.session.flush()
    #         return friend_entry1
    #     return None

    # Remove friend
    # def removeFriend(self, user_id):
    #     r = Friend.query.filter(
    #         or_(
    #             and_(Friend.user1_id == self.id, Friend.user2_id == user_id),
    #             and_(Friend.user1_id == user_id, Friend.user2_id == self.id)
    #         )
    #     ).delete()
    #
    #     if r:
    #         return True
    #
    #     return False

    # Update device token
    def updateDeviceToken(self, device_id, device_token, device_type):
        user_token = UserToken.findByAttributes(
            user_id=self.id,
            device_id=device_id,
        )

        if user_token:
            user_token.device_token = device_token
            user_token.device_type = device_type

            db.session.add(user_token)
            return user_token

        return None

    # logout device
    def logoutDevice(self, device_id):
        user_token = UserToken.findByUserAndDevice(self.id, device_id)

        if user_token:
            user_token.is_active = False
            return user_token

        return None

    # Count new activity of involved paties base on the updated at
    # def getNewActivityOfInvolvedPaties(self):
    #     query = """
    #         WITH involved_paties AS (
    #             SELECT paty_id, last_fetched_at
    #             FROM tbl_paty_user pu
    #             WHERE pu.user_id = :user_id
    #         )
    #         SELECT COUNT(*) AS num_activities, pa.paty_id as paty_id
    #         FROM tbl_paty_activity pa
    #         JOIN involved_paties ip ON ip.paty_id = pa.paty_id
    #         WHERE pa.sender_id <> :user_id AND
    #               pa.updated_at >= ip.last_fetched_at
    #         GROUP BY pa.paty_id;
    #     """
    #
    #     query_result = db.session.execute(query, {"user_id": self.id})
    #
    #     response = {}
    #     paties = []
    #     count = 0
    #     for row in query_result:
    #         count+=row.num_activities
    #         paties.append({"id": row.paty_id, "num": row.num_activities})
    #
    #     response.update({"all": count, "paties": paties})
    #     return response


    #################
    # Class methods #
    #################
    # Create user with data
    @classmethod
    def create(cls, data, source='normal'):
        username = data.get('username', None)
        email = data.get('email', None)
        password = data.get('password', None)
        user = cls.query.filter(or_(cls.email == email)).first()

        if user:
            # user instance and is_new
            return user, False

        user = cls(username, email, password)
        user.first_name = data['first_name']
        user.last_name = data['last_name']
        birthday = data.get('birthday', None)
        if birthday:
            user.birthday = birthday

        if source == 'fb':
            user.facebook_id = data['facebook_id']
            user.facebook_token = data['facebook_token']
            user.fb_avatar = "https://graph.facebook.com/%s/picture" % (data['facebook_id'])

        db.session.add(user)
        # user instance and is_new
        return user, True
