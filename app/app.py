import falcon
import json

from resources import ProtocolResource

app = falcon.API()
protocols = ProtocolResource()
app.add_route('/protocol/{protocol_id}', protocols)
