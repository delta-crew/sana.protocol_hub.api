import config

from db import Session
from models import db, Protocol
from schemas import ProtocolSchema

from flask import Flask, jsonify


app = Flask(__name__)

@app.route('/protocol/<id>')
def get_protocol(id):
    session = Session()
    protocol = session.query(Protocol).get(id)
    protocol_schema = ProtocolSchema()
    result = protocol_schema.dump(protocol)
    return jsonify({'protocol': result.data})

@app.teardown_appcontext
def shutdown_session(exception=None):
    Session.remove()

if __name__ == "__main__":
    app.run(debug=config.DEV)
