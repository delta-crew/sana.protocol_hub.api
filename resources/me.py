from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from schemas import UserSchema


class MeResource(object):
    @falcon.before(login_required)
    def on_get(self, req, resp):
        user = req.context['user']

        user_schema = UserSchema()
        result = user_schema.dump(user)

        resp.context['result'] = result.data
