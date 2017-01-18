import falcon
import json

from app.middleware import JSendTranslator
from resources import ProtocolResource

app = falcon.API(
    middleware=[
        JSendTranslator()
    ]
)

protocols = ProtocolResource()
app.add_route('/protocol/{protocol_id}', protocols)
