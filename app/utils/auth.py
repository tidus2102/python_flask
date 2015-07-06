from flask.ext.login import AnonymousUserMixin, LoginManager

from app.models.user import User

login_manager = LoginManager()

class AnonymousUser(AnonymousUserMixin):
    id = None


login_manager.anonymous_user = AnonymousUser
login_manager.login_view = "user_route.signin"


@login_manager.user_loader
def load_user(user_id):
    return User.findById(user_id)
