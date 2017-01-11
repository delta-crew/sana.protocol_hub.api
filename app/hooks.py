from app import db

def shutdown_session(req, resp, resource):
    db.Session.remove()
