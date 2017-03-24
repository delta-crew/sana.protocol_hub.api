from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMember, User
from schemas import OrganizationMemberSchema


class OrganizationMembersResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, res, organization_id):
        organization_member_schema = OrganizationMemberSchema()
        session = req.context['session']

        # TODO pagination?
        members = session.query(OrganizationMember).\
                filter_by(organization_id=organization_id).\
                all()

        result = organization_group_member_schema.dump(members)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_members))
    def on_post(self, req, res, organization_id):
        organization_member_schema = OrganizationMemberSchema()
        session = req.context['session']
        user = resp.context['user']

        data, errors = organization_member_schema.load(req.context['body'])
        if errors:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        user = session.query(User).\
                filter_by(
                    id=data['userId'],
                ).\
                one_or_none()

        if member == None:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {'user_id': 'user not found'}
            return

        member = OrganizationMember(
            organization_id=organization_id,
            user_id=data['user_id'],
        )

        session.add(member)
        session.commit()

        result = organization_member_schema.dump(organization)
        resp.conext['result'] = result.data
