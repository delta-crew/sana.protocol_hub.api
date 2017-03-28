from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationGroupMember, OrganizationMember
from schemas import OrganizationGroupMemberSchema


class OrganizationGroupMembersResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, resp, organization_id, group_id):
        organization_group_member_schema = OrganizationGroupMemberSchema(many=True)
        session = req.context['session']

        # TODO pagination?
        members = session.query(OrganizationGroupMember).\
                join(OrganizationGroup).\
                filter(
                    OrganizationGroup.organization_id==organization_id,
                    OrganizationGroupMember.organization_group_id==group_id).\
                all()

        result = organization_group_member_schema.dump(members)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_groups))
    def on_post(self, req, resp, organization_id, group_id):
        organization_group_member_schema = OrganizationGroupMemberSchema()
        session = req.context['session']
        user = req.context['user']

        group_member, errors = organization_group_member_schema.load(
            req.context['body'], session=session)
        if errors:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        group_member.organization_group_id = group_id

        member = session.query(OrganizationMember).\
                filter_by(
                    organization_id=organization_id,
                    id=group_member.member.id,
                ).\
                one_or_none()

        if member == None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {'member_id': 'member not found'}
            return

        group = session.query(OrganizationGroup).get(group_id)

        if group == None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {'group_id': 'group not found'}
            return

        session.add(group_member)
        session.commit()

        result = organization_group_member_schema.dump(group_member)
        resp.context['result'] = result.data
