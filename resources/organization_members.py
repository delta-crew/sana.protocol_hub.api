from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import OrganizationMember
from schemas import OrganizationMemberSchema


class OrganizationMembersResource(object):
    def on_get(self, req, res, organization_id):
        # TODO list organization members
        pass

    def on_post(self, req, res, organization_id):
        # TODO add organization group member
        pass
