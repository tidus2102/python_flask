INSTALLATION
====================

1.  git clone git@github.com:tidus2102/python_flask.git --recursive
2.  cd python-flask
3.  vagrant up
4.  browse at: localhost:9100

Working Tips
====================
* Access Postgresql:
	+ ./vagrant/scripts/set_env.sh (this also Active virtual environment)
	+ psql
* Restart server:
	+ ./vagrant/scripts/restart.sh
* Stop server:
	+ ./vagrant/scripts/stop.sh
* Start server:
	+ ./vagrant/scripts/start.sh
* Dev mode debuging:
	+ ./vagrant/scripts/restart.sh
	+ tail -f /vagrant/logs/uwsgi.log => see the log
* Work with migration
    - Run migration:
```
    ./vagrant/scripts/set_env.sh
    cd /vagrant/schema
    python update.py commit
```
    - Create migration:

    1. Step1: Create sql in an exist or new yaml file (schema/migrations/table_name.yaml:

```
---
table: tbl_user
from: null
to: lmd_1
sql: |
  CREATE TYPE USER_STATUS_ENUM AS ENUM ('pending', 'active');
  CREATE TABLE tbl_user (
    id SERIAL NOT NULL PRIMARY KEY,
    full_name TEXT,
    fb_id TEXT,
    email TEXT,
    password TEXT,
    phone_code TEXT,
    phone_number TEXT,
    secret_token TEXT,
    status USER_STATUS_ENUM DEFAULT 'pending',
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT NOW(),
    UNIQUE(fb_id),
    UNIQUE(secret_token),
    UNIQUE(email)
  );
```

    2. Step2: Update version of that table in protected/schema/versions.json

```
        {
          "tbl_user": "lmd_1"
        }
```

    3. Run migration (see above)

Reference Packages
====================
*	SQLAlchemy: http://pythonhosted.org/Flask-SQLAlchemy/
*	WTF: https://flask-wtf.readthedocs.org/en/latest/
*	Login: http://pythonhosted.org/Flask-Login/
*	Principal Access controll: http://pythonhosted.org/Flask-Principal/
*	Translation: http://pythonhosted.org/Flask-BabelEx/
*   Jinja Template: http://jinja.pocoo.org/docs/templates
*   Flask Restful: http://flask-restful.readthedocs.org/

Note for APNS
=============

** Create PEM File **

```
openssl pkcs12 -in <config/apns_dev.p12 | config/apns_prod.p12> -out apns.pem -nodes
```

** Test Connection **

```
openssl s_client -connect gateway.sandbox.push.apple.com:2195 -cert apns.pem
```

** Test Send Push Notification **

```
. scripts/set_env.sh
./shell.py

from app.apns import _do_send

_do_send(['508da0cc23ec0f1f4ded32f7e706a80995988a12a066f5c306566514f1950e6b'], alert='Test Notification')
```
    
Working with translation
====================
* 	Use Flask-Babelex (a fork of Flask-Babel) with additional features, and support Flask-Admin (need to manually uninstall the existing Flask-Babel to avoid conflict)
*	In html file: {{ _('Log In') }}
*	In python file:
	+ from flask.ext.babelex import gettext
	+ gettext('A simple string')
* 	Generate new translation (e.g for Spanish) by running the script
	+ ./script/tr_init.sh vi => generate the message.po file (it will overwrite the exist one)
	+ ./script/tr_update.sh => update the message.po file
	+ then insert the translation texts in app/translations/es/LC_MESSAGES/message.po
	+ Flask-Babel need the compile the file before processing, run the compile script: ./script/tr_compile.sh