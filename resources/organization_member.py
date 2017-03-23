from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMember


class OrganizationMemberResource(object):
    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_members))
    def on_delete(self, req, res, organization_id, member_id):
        session = req.context['session']

        member = session.query(OrganizationMember).\
                filter_by(
                    user_id=member_id,
                    organization_id=organization_id,
                ).\
                one()

        if member != None:
            session.delete(member)
            session.commit()
