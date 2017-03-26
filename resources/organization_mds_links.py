from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLink
from schemas import OrganizationMDSLinkSchema


class OrganizationMDSLinksResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, resp, organization_id):
        organization_mds_link_schema = OrganizationMDSLinkSchema()
        session = req.context['session']

        # TODO pagination?
        members = session.query(OrganizationMDSLink).\
                filter_by(organization_id=organization_id).\
                all()

        result = organization_mds_link_schema.dump(members)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds))
    def on_post(self, req, resp, organization_id):
        organization_mds_link_schema = OrganizationMDSLinkSchema()
        session = req.context['session']
        user = req.context['user']

        mds_link, errors = organization_mds_link_schema.load(
            req.context['body'], session=session)
        if errors:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        mds_link.organization_id = organization_id

        organization = session.query(Organization).get(organization_id)

        if organization == None:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {'organization_id': 'organization not found'}
            return

        session.add(mds_link)
        session.commit()

        result = organization_mds_link_schema.dump(mds_link)
        resp.context['result'] = result.data
