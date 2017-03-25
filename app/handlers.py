import falcon

from app.constants import ERROR_RESPONSE


def generic_error(ex, req, resp, params):
    resp.status = falcon.HTTP_INTERNAL_SERVER_ERROR
    resp.context['type'] = ERROR_RESPONSE
    resp.context['error_message'] = str(ex)
    resp.context['error_code'] = 500
