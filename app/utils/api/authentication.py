from flask import request
from flask.ext.restful import abort
from app.models.user_token import UserToken
from flask.ext.babelex import gettext

def doAuth(*args, **kwargs):
    access_token = request.headers.get("X-Access-Token")
    device_id = request.headers.get("X-Device-Id")

    if not access_token or not device_id:
        abort(404, message=gettext("NOT_FOUND"))

    token = UserToken.findByTokenAndDevice(access_token, device_id)

    if not token or not token.user:
        abort(403, message=gettext("PERMISSION_DENIE"))
    return token.user


def authenticate(**kwargs):
    need_auth = kwargs.get("need_auth", True)
    def wrapped(func):
        def authed(*args, **kwargs):
            # print "IN authenticate() authed()"
            if not need_auth:
                return func(*args, **kwargs)

            # print "Do Authentication"
            # do authentication
            user = doAuth(*args, **kwargs)

            if not user:
                abort(403, message=gettext("PERMISSION_DENIE"))

            kwargs['user'] = user
            return func(*args, **kwargs)
        return authed
    return wrapped
