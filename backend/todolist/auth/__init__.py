from flask import Blueprint
from flask_dance.contrib.github import make_github_blueprint
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_login import current_user

from .models import OAuth
from .. import db

auth_bp = Blueprint("auth_bp", __name__)
github_bp = make_github_blueprint(
    storage=SQLAlchemyStorage(OAuth, db.session), 
    login_url="/github/", 
    authorized_url="/github/authorized/",
    redirect_to="web_bp.home"
)

from . import routes