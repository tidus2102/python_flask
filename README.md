================================================================================
INSTALLATION
================================================================================
1.  git clone git@github.com:tidus2102/python_flask.git --recursive
2.  cd python-flask
3.  vagrant up
4.  Browse at: localhost:9990



================================================================================
WORKING TIPS
================================================================================
vagrant ssh

*** Start, Stop, Restart Server:
sudo stop skeleton
sudo start skeleton
sudo restart skeleton

*** Access Postgresql:
. vagrant/scripts/set_env.sh
psql

*** View log:
tail -f /vagrant/logs/uwsgi.log

*** Check error
. vagrant/scripts/set_env.sh
./vagrant/shell.py



================================================================================
DB MIGRATION
================================================================================
cd /vagrant
. set_env.sh

1. Create migration file:
alembic revision -m "<table> <version> <dev_name> <changes>"

Ex: alembic revision -m "tbl_user 1 hn add update_at column"

2. Upgrade:
alembic upgrade head
alembic upgrade <revision>

3. Downgrade:
alembic downgrade -1
alembic downgrade <revision>



================================================================================
NOTIFICATION FOR IOS
================================================================================
*** Create PEM file from p12 file
openssl pkcs12 -in config/apns.p12 -out apns.pem -nodes

*** Check SSL connection with pem file
openssl s_client -connect gateway.sandbox.push.apple.com:2195 -cert config/apns.pem

*** Test push notification
. /vagrant/scripts/set_env.sh
./vagrant/shell.py
from app.apns import _do_send
_do_send(['<device_token>'], alert='Test Notification')



================================================================================
TRANSLATION
================================================================================
*** Use Flask-Babelex (a fork of Flask-Babel) with additional features, and support Flask-Admin (need to manually uninstall the existing Flask-Babel to avoid conflict)

- In html file: {{ _('Log In') }}

- In python file:
  + from flask.ext.babelex import gettext
  + gettext('A simple string')

*** Generate new translation by running the script (Ex: Vietnamese)
./script/tr_init.sh vi => generate the message.po file (it will overwrite the exist one)
./script/tr_update.sh => update the message.po file
Then add translation texts in app/translations/vi/LC_MESSAGES/message.po

*** Flask-Babel need the compile the file before processing, run the compile script:
./script/tr_compile.sh



================================================================================
REFERENCES DOCUMENT
================================================================================
*	SQLAlchemy: http://pythonhosted.org/Flask-SQLAlchemy/
*	WTF: https://flask-wtf.readthedocs.org/en/latest/
*	Login: http://pythonhosted.org/Flask-Login/
*	Principal Access Control: http://pythonhosted.org/Flask-Principal/
*	Translation: http://pythonhosted.org/Flask-BabelEx/
*   Jinja Template: http://jinja.pocoo.org/docs/templates
*   Flask Restful: http://flask-restful.readthedocs.org/
*   Alembic: http://alembic.readthedocs.org/en/latest/ops.html