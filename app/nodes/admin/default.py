from flask import Blueprint, render_template, redirect, request
from app.utils import helper
from app.models.user import User
from app.models.common import db
import uuid

admin_default_blueprint = Blueprint('admin_default_blueprint', __name__)

@admin_default_blueprint.route('/')
def admin_default_index():
    return render_template('/admin/default/index.html')
