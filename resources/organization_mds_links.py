from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMDSLink
from schemas import OrganizationMDSLinkSchema


class OrganizationMDSLinksResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, res, organization_id):
        organization_mds_link_schema = OrganizationMDSLinkSchema()
        session = req.context['session']

        # TODO pagination?
        members = session.query(OrganizationMDSLink).\
                filter_by(organization_id=organization_id).\
                all()

        result = organization_group_member_schema.dump(members)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_mds))
    def on_post(self, req, res, organization_id):
        organization_group_member_schema = OrganizationMDSLinkSchema()
        session = req.context['session']
        user = resp.context['user']

        data, errors = organization_mds_link.load(req.context['body'])
        if errors:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        member = session.query(OrganizationMember).\
                filter_by(
                    organization_id=organization_id,
                    id=data['organization_member_id'],
                ).\
                one_or_none()

        if member == None:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {'member_id': 'member not found'}
            return

        gmember = OrganizationGroupMember(
            organization_id=organization_id,
            organization_member_id=data['organization_member_id'],
            organization_group_id=group_id,
        )

        session.add(gmember)
        session.commit()

        result = organization_group_member_schema.dump(organization)
        resp.conext['result'] = result.data
