import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import Organization
from schemas import OrganizationSchema


class OrganizationResource(object):
    def on_get(self, req, resp, organization_id):
        session = req.context['session']
        protocol = session.query(Organization).get(organization_id)
        if protocol == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'organization': 'no organization with id {}'.format(organization_id),
            }
            return

        organization_schema = OrganizationSchema()
        result = organization_schema.dump(organization)

        resp.context['result'] = result.data
