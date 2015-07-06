from flask.ext.admin.contrib.sqla import ModelView
from flask.ext.login import current_user
from flask.ext.admin.base import AdminIndexView


def checkPermission():
    return current_user.is_authenticated() and current_user.is_admin

class AdminView(ModelView):
    def is_accessible(self):
        return checkPermission()

class AdminIndex(AdminIndexView):
    def is_accessible(self):
        # default behavior of Flask-Admin when checking permission is that
        # it will raise 403 http error, 
        # need to handle it to redirect to login page
        return checkPermission()