import falcon

from app import db
from app.constants import FAIL_RESPONSE
from models import Token, User


def login_required(req, resp, resource, params):
    if req.auth == None:
        resp.context['type'] = FAIL_RESPONSE
        resp.context['result'] = {'unauthorized': 'no auth token provided'}
        raise falcon.HTTPUnauthorized()

    session = req.context['session']

    token = session.query(Token).filter_by(key=req.auth).one_or_none()
    if token == None:
        resp.context['type'] = FAIL_RESPONSE
        resp.context['result'] = {'unauthorized': 'invalid token'}
        raise falcon.HTTPUnauthorized()

    user = session.query(User).get(token.user_id)
    if user == None:
        resp.context['type'] = FAIL_RESPONSE
        resp.context['result'] = {'unauthorized': 'invalid user'}
        raise falcon.HTTPUnauthorized()

    req.context['user'] = user
