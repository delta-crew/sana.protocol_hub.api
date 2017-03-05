import falcon
import json

from app.middleware import SessionWrapper, JSendTranslator
from resources import ProtocolResource

app = falcon.API(
    middleware=[
        SessionWrapper(),
        JSendTranslator(),
    ]
)

protocols = ProtocolResource()
app.add_route('/protocol/{protocol_id}', protocols)
