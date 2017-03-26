from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import Organization, OrganizationMember
from schemas import OrganizationSchema


class OrganizationsResource(object):
    @falcon.before(login_required)
    def on_get(self, req, resp):
        organization_schema = OrganizationSchema(many=True, exclude=('members'))
        session = req.context['session']
        user = req.context['user']

        organizations = session.query(Organization).\
                join(OrganizationMember).\
                filter(OrganizationMember.user_id==user.id).\
                all()

        result = organization_schema.dump(organizations)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    def on_post(self, req, resp):
        organization_schema = OrganizationSchema()
        session = req.context['session']
        user = req.context['user']

        organization, errors = organization_schema.load(
            req.context['body'], session=session)
        if errors:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        organization.owner_id = user.id

        session.add(organization)
        session.commit()

        member = OrganizationMember(user_id=user.id, organization_id=organization.id)
        session.add(member)
        session.commit()

        result = organization_schema.dump(organization)
        resp.context['result'] = result.data
