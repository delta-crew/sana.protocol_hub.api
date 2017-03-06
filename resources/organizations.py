import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import Organization
from schemas import OrganizationSchema


class OrganizationsResource(object):
    def on_post(self, req, res):
        organization_schema = OrganizationSchema()
        session = req.context['session']
        user = resp.context['user']

        data, errors = organization_schema.load(req.context['body'])
        if errors:
            resp.stats = falcon.HTTP_BAD_REQUEST
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = errors
            return

        organization = Organization(name=data['name'], owner_id=user.id)
        organization.members.append(OrganizationMember(user_id=user.id))

        session.add(organization)
        session.commit()

        result = organization_schema.dump(organization)
        resp.conext['result'] = result.data
