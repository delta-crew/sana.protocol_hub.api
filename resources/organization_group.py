import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationGroup
from schemas import OrganizationGroupSchema


@falcon.after(app.hooks.shutdown_session)
class OrganizationGroupResource(object):
    def on_get(self, req, res, organization_id, group_id):
        # TODO get organization group (list all members?)
        pass

    def on_delete(self, req, res, organization_id, group_id):
        # TODO remove organization group
        pass
