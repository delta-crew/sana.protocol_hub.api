from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import Organization
from schemas import OrganizationSchema


class OrganizationResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, resp, organization_id):
        session = req.context['session']
        organization = session.query(Organization).get(organization_id)
        if organization == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'organization': 'no organization with id {}'.format(organization_id),
            }
            return

        organization_schema = OrganizationSchema()
        result = organization_schema.dump(organization)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_ownership))
    def on_put(self, req, resp, organization_id):
        session = req.context['session']
        organization_schema = OrganizationSchema()

        organization = session.query(Organization).get(organization_id)
        if organization == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'organization': 'no organization with id {}'.format(organization_id),
            }
            return

        new_organization, errors = organization_schema.load(
            req.context['body'], instance=organization, session=session)
        if errors:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        session.add(organization)
        session.commit()

        result = organization_schema.dump(organization)
        resp.context['result'] = result.data
