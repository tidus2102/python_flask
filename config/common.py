# -*- coding: utf-8 -*-
import os
CONFIG_DIR = os.path.dirname(os.path.abspath(__file__))
APP_ROOT = CONFIG_DIR.rsplit('/', 1)[0]

IMG_DIRS = {
    "photo":{
        "origin": os.path.join(APP_ROOT, 'app/static/uploads/photo/origin'),
        "large": os.path.join(APP_ROOT, 'app/static/uploads/photo/large'),
        "medium": os.path.join(APP_ROOT, 'app/static/uploads/photo/medium'),
        "small": os.path.join(APP_ROOT, 'app/static/uploads/photo/small'),
        "thumb": os.path.join(APP_ROOT, 'app/static/uploads/photo/thumb')
    },
}

IMG_SIZES = {
    "avatar":{
        "origin": 128,
        "small": 128,
        "thumb": 64
    },
    "paty_icon":{
        "small": 128,
        "thumb": 64
    },
    "photo":{
        "small": 200,
        "thumb": 128
    }
}


config = {
    'IMG_DIRS': IMG_DIRS,
    'IMG_SIZES': IMG_SIZES,
    'ALLOWED_EXTENSIONS': set(['png', 'jpg', 'jpeg', 'gif']),
    'MAX_CONTENT_LENGTH': 2 * 1024 * 1024,
    'DATETIME_FORMAT': "%d-%m-%Y %H:%M",
    'DATE_FORMAT': '%d-%m-%Y',
    'TIME_FORMAT': '%H:%M',
    'LANGUAGES': (
        ('vi', u'Tiếng Việt'),
        ('en', u'English')
    ),
    #'english_domains': ['skeleton.bestack.com']
    #'DOMAIN': 'skeleton.bestacker.com',
    # 'SECRET_KEY': 'flask-session-insecure-secret-key',
    # 'SQLALCHEMY_DATABASE_URI': '',
    # 'SQLALCHEMY_ECHO': False,

    # 'email': {
    # },
    # 'apns': {
    # },
    # 'gcm': {},
    # 'debug': True,
}
