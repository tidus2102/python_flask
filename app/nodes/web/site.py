from flask import Blueprint, render_template, redirect, request
from app.models.common import db
from app.models.user import User
from app.utils import helper

web_site_blueprint = Blueprint('web_site_blueprint', __name__)

@web_site_blueprint.route('/')
def web_site_index():
    return render_template('/web/site/index.html')
