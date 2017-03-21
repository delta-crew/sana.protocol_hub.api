from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationGroup, OrganizationGroupMember
from schemas import OrganizationGroupSchema

class OrganizationGroupResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, res, organization_id, group_id):
        session = req.context['session']
        organization_group_schema = OrganizationGroupSchema()

        group = session.query(OrganizationGroup).get(group_id)

        result = organization_group_schema.dump(group)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_groups))
    def on_delete(self, req, res, organization_id, group_id):
        session = req.context['session']

        group = session.query(OrganizationGroup).\
                filter_by(id=group_id, organization_id=organization_id).\
                one()

        if group != None:
            session.delete(group)
            session.commit()
