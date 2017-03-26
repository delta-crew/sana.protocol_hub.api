from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMember, Organization


class OrganizationMemberResource(object):
    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_members))
    def on_delete(self, req, resp, organization_id, user_id):
        session = req.context['session']

        isOwner = session.query(Organization).\
                filter_by(
                    owner_id=user_id,
                    id=organization_id,
                ).\
                first()

        if isOwner:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {'owner': 'Can\'t remove the owner from organization'}
            return

        member = session.query(OrganizationMember).\
                filter_by(
                    user_id=user_id,
                    organization_id=organization_id,
                ).\
                first()

        if member is None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'group': 'no organization member with id {}'.format(user_id),
            }
            return

        session.delete(member)
        session.commit()
        resp.context['result'] = {}
