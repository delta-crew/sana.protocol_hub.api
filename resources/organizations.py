import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import Organization
from schemas import OrganizationSchema


class OrganizationsResource(object):
    def on_post(self):
        # TODO create organization
        pass
