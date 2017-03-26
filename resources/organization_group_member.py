from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationGroupMember


class OrganizationGroupMemberResource(object):
    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_groups))
    def on_delete(self, req, resp, organization_id, group_id, user_id):
        session = req.context['session']

        member = session.query(OrganizationGroupMember).\
                filter_by(
                    organization_member_id=user_id,
                    organization_group_id=group_id,
                ).\
                first()

        if member == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'member': 'no member with id {}'.format(user_id),
            }
            return

        session.delete(member)
        session.commit()
        resp.context['result'] = {}
