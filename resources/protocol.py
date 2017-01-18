import app.hooks
import falcon

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE
from models import Protocol
from schemas import ProtocolSchema


@falcon.after(app.hooks.shutdown_session)
class ProtocolResource(object):
    def on_get(self, req, resp, protocol_id):
        session = db.Session()
        protocol = session.query(Protocol).get(protocol_id)
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
