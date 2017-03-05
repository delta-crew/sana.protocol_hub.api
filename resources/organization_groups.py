import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationGroup
from schemas import OrganizationGroupSchema


@falcon.after(app.hooks.shutdown_session)
class OrganizationGroupsResource(object):
    def on_get(self, req, res, organization_id):
        # TODO list organization groups
        pass

    def on_post(self, req, res, organization_id):
        # TODO create organization group
        pass
