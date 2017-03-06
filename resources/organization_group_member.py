from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationGroupMember


class OrganizationGroupMemberResource(object):
    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_groups))
    def on_delete(self, req, res, organization_id, group_id, member_id):
        session = req.context['session']

        member = session.query(OrganizationGroupMember).\
                filter_by(
                    organization_member_id=member_id,
                    organization_group_id=group_id,
                ).\
                one()

        if member != None:
            session.delete(member)
            session.commit()
