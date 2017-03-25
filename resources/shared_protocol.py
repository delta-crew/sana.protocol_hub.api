from app.hooks import *
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from sqlalchemy.orm import joinedload
from models import SharedProtocol
from schemas import ProtocolSchema


class SharedProtocolResource(object):
    @falcon.before(login_required)
    @falcon.before(user_belongs_to_organization)
    def on_get(self, req, resp, organization_id, protocol_id):
        session = req.context['session']

        protocol = session.query(SharedProtocol.protocol).\
            options(joinedload(SharedProtocol.protocol)).\
            filter_by(
                SharedProtocol.protocol_id==protocol_id,
                SharedProtocol.organization_id==organization_id,
            ).\
            one_or_none()

        if protocol == None:
            resp.status = falcon.HTTP_NOT_FOUND
            resp.context['type'] = FAIL_RESPONSE
            resp.context['result'] = {
                'protocol': 'no protocol with id {}'.format(protocol_id),
            }
            return

        protocol_schema = ProtocolSchema()
        result = protocol_schema.dump(protocol)

        resp.context['result'] = result.data

    @falcon.before(login_required)
    @falcon.before(authorize_organization_user_to(OrganizationGroup.manage_protocols))
    def on_delete(self, req, resp, organization_id, protocol_id):
        session = req.context['session']

        group = session.query(SharedProtocol).\
                filter_by(protocol_id=protocol_id, organization_id=organization_id).\
                one()

        if group != None:
            session.delete(group)
            session.commit()
