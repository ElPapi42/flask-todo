import uuid

from flask_dance.consumer.storage.sqla import OAuthConsumerMixin
from sqlalchemy.dialects.postgresql import UUID

from ... import db
from ...api.models import User

class OAuth(OAuthConsumerMixin, db.Model):
    """ Storage for oauth tokens """

    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, nullable=False)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey(User.id))
    user = db.relationship(User)

    def __init__(self, user_id, user):
        self.user_id = user_id
        self.user = user
        self.id = uuid.uuid4()

    def __repr__(self):
        return "<user {}>".format(self.user_id.email)