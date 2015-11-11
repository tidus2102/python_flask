from app.models.common import db
from app.models.user import User
from flask.ext.script import Command
from flask import render_template, current_app

"""
class CheckExpired(Command):
    def run(self):
        cfg = current_app.config['email']
        users = User.getUsersToExpire()
        for user in users:
            user.update({"state": User.STATE_EXPIRED})
            # send email to notify user
            EmailMessage.create(
                db.session,
                [user.email],
                subject=cfg['prefix'] + ' Your account has expired',
                content=render_template('mail/expired.html',
                    user=user)
                )
        db.session.commit()


class NotifyExpired(Command):
    def run(self):
        cfg = current_app.config['email']
        # notify users before their accounts get expired (before 7, 3, 1 days)
        for day in (7, 3, 1):
            users = User.getUsersBeforeExpireNDays(day)
            for user in users:
                # send email to notify
                EmailMessage.create(
                    db.session,
                    [user.email],
                    subject=cfg['prefix'] + ' Your account will expire in %s days' % day,
                    content=render_template('mail/will_expire.html',
                        user=user, day=day)
                    )

class HashAccessToken():
    def run(self):
        from app.models.user_token import UserToken
        from app.models import db
        import bcrypt

        user_tokens = UserToken.query.all()
        for ut in user_tokens:
            print "ID: %s AT: %s" % (ut.id, ut.access_token)
            ut.access_token = bcrypt.hashpw(ut.access_token, bcrypt.gensalt(10))
            print "ID: %s AT: %s" % (ut.id, ut.access_token)
            db.session.add(ut)
        db.session.commit()
"""
