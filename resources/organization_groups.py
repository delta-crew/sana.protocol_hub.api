from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationGroup
from schemas import OrganizationGroupSchema


class OrganizationGroupsResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, resp, organization_id):
        organization_group_schema = OrganizationGroupSchema(many=True)
        session = req.context['session']

        # TODO pagination?
        groups = session.query(OrganizationGroup).\
                filter_by(organization_id=organization_id).\
                all()

        result = organization_group_schema.dump(groups)
        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_groups))
    def on_post(self, req, resp, organization_id):
        schema = OrganizationGroupSchema()
        session = req.context['session']
        user = req.context['user']

        group, errors = schema.load(req.context['body'], session=session)
        if errors:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        group.organization_id = organization_id

        session.add(group)
        session.commit()

        result = schema.dump(group)
        resp.context['result'] = result.data
