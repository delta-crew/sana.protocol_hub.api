import falcon

from app import db
from app.constants import FAIL_RESPONSE
from models import (
    Token,
    User,
    Organization,
    OrganizationGroup,
    OrganizationMember,
    OrganizationGroupMember,
)


def authorize_organization_user_to(permission):
    # TODO authenticate user organization permissions a better way?

    def helper(req, resp, resource, params):
        session = req.context['session']
        user = req.context['user']

        organization_id = params['organization_id']
        organization = session.query(Organization).get(organization_id)
        if organization == None:
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {'organization': 'no organization with id {}'.format(organization_id)}
            raise falcon.HTTPNotFound()

        if user != organization.owner:
            has_permissions = session.query(OrganizationGroup).\
                    join(OrganizationGroupMember).\
                    filter(OrganizationGroup.organization_id==organization_id).\
                    filter(OrganizationGroupMember.user_id==user.id).\
                    filter(permission==True).\
                    one_or_none()

            if has_permissions == None:
                resp.context['type'] = FAIL_RESPONSE
                resp.context['result'] = {'unauthorized': 'no permission to perform'}
                raise falcon.HTTPUnauthorized()

    return helper


def user_belongs_to_organization(req, resp, resource, params):
    session = req.context['session']
    user = req.context['user']

    organization_id = params['organization_id']
    has_permissions = session.query(OrganizationMember).\
            filter_by(user_id=user.id, organization_id=organization_id).\
            one_or_none()

    if has_permissions == None:
        resp.context['type'] = FAIL_RESPONSE
        resp.context['result'] = {'unauthorized': 'no permission to perform'}
        raise falcon.HTTPUnauthorized()


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
