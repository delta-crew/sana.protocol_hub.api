from app.hooks import *
import falcon
from sqlalchemy import or_

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import User
from schemas import UserSchema


class UsersResource(object):
    def on_get(self, req, resp):
        session = req.context['session']
        query = req.params.get('query', '')
        user_schema = UserSchema(many=True)

        users = session.query(User).\
                filter(or_(
                    User.last_name.ilike('%' + query + '%'),
                    User.first_name.ilike('%' + query + '%'),
                )).\
                limit(100).\
                all()

        result = user_schema.dump(users)
        resp.context['result'] = result.data
