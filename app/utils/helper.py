import uuid
import string
import os, re
from random import choice
from PIL import Image
from flask import current_app, session, request
from datetime import timedelta, datetime
from dateutil.relativedelta import relativedelta
import pytz
from flask.ext.babelex import gettext

CRASH = object()


def st(u, coding="utf-8"):
    try:
        return str(u)
    except UnicodeEncodeError:
        return unicode(u).encode(coding)


def utcnow():
    return pytz.UTC.localize(datetime.utcnow())


def format_datetime(value, format=None):
    try:
        format = format or current_app.config['DATETIME_FORMAT']

        # convert to client timezone
        value = value + relativedelta(days=current_app.config['tizo_offset'])
        return value.strftime(format)
    except Exception, e:
        return ""


def format_date(value, format=None):
    try:
        format = format or current_app.config['DATE_FORMAT']
        return value.strftime(format)
    except Exception, e:
        return ""

def time_to_str(value, format="%Y-%m-%dT%H:%M:%S%z"):
    try:
        return value.strftime(format)
    except Exception, e:
        return ""


def format_time(value, format=None):
    try:
        format = format or current_app.config['TIME_FORMAT']

        # convert to client timezone
        value = value + relativedelta(days=current_app.config['tizo_offset'])
        return value.strftime(format)
    except Exception, e:
        return ""


def generate_string(length=16):
    return ''.join([choice(string.letters + string.digits) for i in range(length)])


def generateUniqueString():
    return str(uuid.uuid4())


def checkValidImageFile(extension, cfg):
    return extension in cfg['ALLOWED_EXTENSIONS']


def getThumbSize(size, thumbSize):
    # keep either width or height equals thumbSize
    width = size[0]
    height = size[1]
    ratio = 1.0*width/height
    if width > height:
        thumbWidth = thumbSize
        thumbHeight = int(thumbWidth / ratio)
    else:
        thumbHeight = thumbSize
        thumbWidth = int(thumbHeight * ratio)
    return (thumbWidth, thumbHeight)


def saveImage(stream, filename, cfg, img_type = "avatar"):
    # print "IN uploadAvatar() Filename: %s" %(filename)
    dirs = cfg["IMG_DIRS"][img_type]
    sizes = cfg["IMG_SIZES"][img_type]

    orig = Image.open(stream)
    img = orig.copy()

    # print "IN uploadAvatar() save origin"
    filepath = dirs['origin'] + '/' + filename
    img.save(filepath, orig.format)

    # print "IN uploadAvatar() save small"
    small = img.resize(getThumbSize(img.size, sizes["small"]), Image.ANTIALIAS)
    filepath = dirs['small'] + '/' + filename
    small.save(filepath, orig.format)

    # print "IN uploadAvatar() save thumb"
    thumb = img.resize(getThumbSize(img.size, sizes["thumb"]), Image.ANTIALIAS)
    filepath = dirs['thumb'] + '/' + filename
    thumb.save(filepath, orig.format)


def deleteImage(filename, cfg, img_type="avatar"):
    dirs = cfg['IMG_DIRS'][img_type]
    for key, path in dirs.iteritems():
        path = path + "/" + filename
        if os.path.exists(path) and os.path.isfile(path):
            os.remove(path)

def updateImage(model, attribute, file, type):
    extension = file.filename.rsplit('.', 1)[1]
    filename = generateUniqueString() + '.' + extension

    cfg = current_app.config
    if file and checkValidImageFile(extension, cfg):
        old_filename = getattr(model, attribute)
        # current_app.logger.info("Old Avatar: {0}".format(old_filename))
        try:
            saveImage(file.stream, filename, cfg, type)
            setattr(model, attribute, filename)
        except Exception, e:
            # current_app.logger.error("Exception: {0}".format(e))
            return {"message": gettext("NOT_FOUND")}, 404

        # Delete the old avatar, no need to keep it
        try:
            if old_filename:
                deleteImage(old_filename, cfg, type)
        except Exception, e:
            current_app.logger.error("Exception: {0}".format(e))
            pass

def uni(s, coding="utf-8"):
    if isinstance(s, unicode):
        return s
    return unicode(s, coding)


def getInt(request, key, default=None):
    try:
        return int(request.form.get(key, default))
    except Exception:
        if default is CRASH:
            raise
        return default


def getUnicode(request, key, default=None, crashOnBlank=False):
    try:
        val = request.form.get(key).strip()
        if crashOnBlank:
            assert val
        return uni(val)
    except Exception, e:
        if default is CRASH:
            raise
        return default


def getBool(request, key):
    val = request.form.get(key, None)
    return val in ('1', 'True', 'true')


email_re = re.compile(
    r"(^[-!#$%&'*+/=?^_`{}|~0-9A-Z]+(\.[-!#$%&'*+/=?^_`{}|~0-9A-Z]+)*"  # dot-atom
    r'|^"([\001-\010\013\014\016-\037!#-\[\]-\177]|\\[\001-011\013\014\016-\177])*"' # quoted-string
    r')@(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?$', re.IGNORECASE)


def checkEmail(email):
    if email_re.match(email) is None:
        return False
    return True


def allowedLocales():
    return [k for k, _ in current_app.config['LANGUAGES']]


class UnsupportedLocale(Exception):
    pass


def setLocale(code):
    print "code", code
    locales = allowedLocales()
    if code in locales:
        session["app.locale"] = code
    else:
        # TODO: Custom type
        raise UnsupportedLocale(locales)


def getLocale():
    locale = session.get("app.locale")
    if locale:
        return locale
    else:
        host = request.headers['Host']
        if host in current_app.config['english_domains']:
            return 'en'

        # Favor first language for now
        return allowedLocales()[0]
        # return request.accept_languages.best_match(allowedLocales())


def format_currency(value):
    try:
        value = int(value)
        value = "{:,}".format(value)
        return value
        #return value.replace(",", ".")
    except Exception, e:
        return 'N/A'

def get(data, key, default=None):
    if not key in data:
        return default

    if not data.get(key):
        return default

    return data.get(key)


def getFields(fields):
    if not fields:
        return []
    return fields.replace(" ", "").split(",")

def checkSublist(sublist, list):
    try:
        return set(sublist).issubset(list)
    except:
        return False