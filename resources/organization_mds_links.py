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
        organization_mds_link_schema = OrganizationMDSLinkSchema(many=True)
        session = req.context['session']

        # TODO pagination?
        mds_links = session.query(OrganizationMDSLink).\
                filter_by(organization_id=organization_id).\
                all()

        result = organization_mds_link_schema.dump(mds_links)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds))
    def on_post(self, req, resp, organization_id):
        organization_mds_link_schema = OrganizationMDSLinkSchema()
        session = req.context['session']

        mds_link, errors = organization_mds_link_schema.load(
            req.context['body'], session=session)
        if errors:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        mds_link.organization_id = organization_id

        session.add(mds_link)
        session.commit()

        result = organization_mds_link_schema.dump(mds_link)
        resp.context['result'] = result.data
