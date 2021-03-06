from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import OrganizationMember, User
from schemas import OrganizationMemberSchema


class OrganizationMembersResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, resp, organization_id):
        organization_member_schema = OrganizationMemberSchema(
                only=('id', 'user.id', 'user.first_name', 'user.last_name', 'user.username'),
                many=True)
        session = req.context['session']

        # TODO pagination?
        members = session.query(OrganizationMember).\
                options(joinedload(OrganizationMember.user)).\
                filter_by(organization_id=organization_id).\
                all()

        result = organization_member_schema.dump(members)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_members))
    def on_post(self, req, resp, organization_id):
        organization_member_schema = OrganizationMemberSchema()
        session = req.context['session']

        member, errors = organization_member_schema.load(req.context['body'], session=session)
        if errors:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        user = session.query(User).\
                filter_by(
                    id=req.context['body']['user_id']
                ).\
                one_or_none()

        if user == None:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {'user_id': 'user not found'}
            return

        member.organization_id = organization_id
        member.user_id = user.id

        session.add(member)
        session.commit()

        result = organization_member_schema.dump(member)
        resp.context['result'] = result.data
