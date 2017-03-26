from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLink
from schemas import OrganizationMDSLinkSchema


class OrganizationMDSLinkResource(object):
    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds))
    def on_get(self, req, resp, organization_id, mds_link_id):
        session = req.context['session']
        organization_mds_link_schema = OrganizationMDSLinkSchema()

        mds = session.query(OrganizationMDSLink).\
                filter_by(
                    organization_id=organization_id,
                    id=mds_link_id,
                ).\
                one_or_none()

        if mds == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'mds_link': 'no mds link with id {}'.format(mds_link_id),
            }
            return

        result = organization_mds_link_schema.dump(mds)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds))
    def on_delete(self, req, resp, organization_id, mds_link_id):
        session = req.context['session']

        mds = session.query(OrganizationMDSLink).\
                filter_by(
                    organization_id=organization_id,
                    id=mds_link_id,
                ).\
                one_or_none()

        if mds == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'mds_link': 'no mds link with id {}'.format(mds_link_id),
            }
            return

        session.delete(mds)
        session.commit()
        resp.context['result'] = {}

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds))
    def on_put(self, req, resp, organization_id, mds_link_id):
        session = req.context['session']
        organization_mds_link_schema = OrganizationMDSLinkSchema()

        mds = session.query(OrganizationMDSLink).\
                filter_by(
                    organization_id=organization_id,
                    id=mds_link_id,
                ).\
                one_or_none()

        if mds == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'mds_link': 'no mds link with id {}'.format(mds_link_id),
            }
            return

        new_mds, errors = organization_mds_link_schema.load(
            req.context['body'], instance=mds, session=session)

        session.add(new_mds)
        session.commit()

        result = organization_mds_link_schema.dump(new_mds)
        resp.context['result'] = result.data
