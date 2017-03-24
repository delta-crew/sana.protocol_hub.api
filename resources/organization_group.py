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

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_groups))
    def on_put(self, req, res, organization_id, group_id):
        session = req.context['session']
        organization_group_schema = OrganizationGroupSchema()

        group = session.query(OrganizationGroup).\
                filter_by(
                    organization_id=organization_id,
                    id=group_id,
                ).\
                one_or_none()

        if group == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'mds_link': 'no mds link with id {}'.format(mds_link_id),
            }
            return

        # TODO can the schema make this nicer?
        group.name = req.data['name']
        group.manage_protocols = req.data['manage_protocols']
        group.manage_mds = req.data['manage_mds']
        group.manage_mds_protocols = req.data['manage_mds_protocols']
        group.synchronize_mds = req.data['synchronize_mds']
        group.manage_groups = req.data['manage_groups']
        group.manage_members = req.data['manage_members']
        group.manage_ownership = req.data['manage_ownership']

        session.add(group)
        session.commit()

        result = organization_group_schema.dump(group)
        resp.context['result'] = result.data
