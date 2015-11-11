import traceback
from flask import Flask, render_template, current_app, redirect, flash
from flask.ext.login import current_user
from flask.ext.principal import Principal, identity_loaded, RoleNeed, UserNeed
from flask.ext.babelex import Babel, lazy_gettext
from flask.ext.cache import Cache

from app.models.common import db
from app.utils.auth import login_manager
from config.main import config as main_config

from nodes.web.site import web_site_blueprint
from nodes.admin.default import admin_default_blueprint

from nodes.api.base import api_blueprint
from nodes.api.v1 import api_v1_blueprint
#from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config.update(main_config)
app.debug = main_config.get("debug", False)

db.init_app(app)
login_manager.init_app(app)

# Admin blueprints
app.register_blueprint(admin_default_blueprint, url_prefix='/admin')


# Web blueprints
app.register_blueprint(web_site_blueprint)


# API blueprints
app.register_blueprint(api_blueprint)

app.register_blueprint(api_v1_blueprint)

principals = Principal(app)
babel = Babel(app)

cache = Cache()
cache.init_app(app)

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    # Set the identity user object
    identity.user = current_user

    # Add the UserNeed to the identity
    if current_user:
        identity.provides.add(UserNeed(current_user.id))

    # Assuming the User model has a list of roles, update the
    # identity with the roles that the user provides
    if current_user.id and current_user.role:
        identity.provides.add(RoleNeed(current_user.role.value))


from app.utils import helper
app.jinja_env.add_extension('jinja2.ext.loopcontrols')
app.jinja_env.globals.update({
    'enumerate': enumerate,
    'str':str,
    'len':len,
    'getattr': getattr,
    'format_datetime': helper.format_datetime,
    'format_date': helper.format_date,
    'format_time': helper.format_time,
    'current_app': current_app,
    'getLocale': helper.getLocale,
})

@babel.localeselector
def get_locale():
    return helper.getLocale()

@app.errorhandler(403)
@cache.cached(timeout=60*60*24)
def permission_denied(e):
    return render_template('errors/403.html'), 403

@app.errorhandler(404)
@cache.cached(timeout=60*60*24)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
@cache.cached(timeout=60*60*24)
def internal_error(e):
    return render_template('errors/500.html'), 500


# Register custom events
from app import events
events.wire(app)


# Email notification on error
# if not app.debug:
#     from app import mail
#
#     @app.errorhandler(Exception)
#     def got_error(e):
#         stack_trace = traceback.format_exc()
#         emails = current_app.config["email"].get("errors", [])
#
#         mail.send(
#             [{"email": e} for e in emails],
#             u"[Error on %s]" % (current_app.config.get("env", None)),
#             stack_trace,
#             "errors@skeleton.com",
#         )
#         return ""

# toolbar = DebugToolbarExtension(app)
