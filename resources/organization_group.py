from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationGroup, OrganizationGroupMember
from schemas import OrganizationGroupSchema

class OrganizationGroupResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, resp, organization_id, group_id):
        session = req.context['session']
        organization_group_schema = OrganizationGroupSchema()

        group = session.query(OrganizationGroup).get(group_id)
        if group == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'group': 'no group with id {}'.format(group_id),
            }
            return

        result = organization_group_schema.dump(group)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_groups))
    def on_delete(self, req, resp, organization_id, group_id):
        session = req.context['session']

        group = session.query(OrganizationGroup).get(group_id)

        if group == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'group': 'no group with id {}'.format(group_id),
            }
            return

        session.delete(group)
        session.commit()
        resp.context['result'] = {}

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_groups))
    def on_put(self, req, resp, organization_id, group_id):
        session = req.context['session']
        organization_group_schema = OrganizationGroupSchema()

        group = session.query(OrganizationGroup).get(group_id)

        if group == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'group': 'no group with id {}'.format(group_id),
            }
            return

        new_group, errors = organization_group_schema.load(
            req.context['body'], instance=group, session=session)
        if errors:
            resp.status = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        session.add(group)
        session.commit()

        result = organization_group_schema.dump(group)
        resp.context['result'] = result.data
