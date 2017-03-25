import falcon

from app.constants import ERROR_RESPONSE


def route_not_found(req, resp):
    resp.status = falcon.HTTP_NOT_FOUND
    resp.context['type'] = ERROR_RESPONSE
    resp.context['error_message'] = "route not found"
    resp.context['error_code'] = 404
    resp.context['error_data'] = {'route': req.relative_uri}
