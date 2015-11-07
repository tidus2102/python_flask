from flask import Blueprint, render_template, redirect, request
from app.utils import helper
from app.models.user import User
from app.models.common import db
import uuid

web_blueprint = Blueprint('web_blueprint', __name__)

@web_blueprint.route('/')
def web_site_index():
    return render_template('/web/site/index.html')
