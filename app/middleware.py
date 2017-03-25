import json

from app import db
from app.constants import SUCCESS_RESPONSE, FAIL_RESPONSE, ERROR_RESPONSE
from app.errors import ResponseError


class BodyParser(object):
    def process_request(self, req, resp):
        if req.content_length:
            req.context['body'] = json.load(req.stream)


class SessionWrapper(object):
    def process_request(self, req, resp):
        req.context['session'] = db.Session()

    def process_response(self, req, resp, resource):
        db.Session.remove()


class JSendTranslator(object):
    def process_response(self, req, resp, resource):
        if req.method == 'OPTIONS':
            return

        resp_type = SUCCESS_RESPONSE
        if 'type' in resp.context:
            resp_type = resp.context['type']

        if 'result' not in resp.context and resp_type != ERROR_RESPONSE:
            raise ResponseError('Missing response schema!')

        if resp_type == SUCCESS_RESPONSE:
            result = self.success_response(resp.context['result'])
        elif resp_type == FAIL_RESPONSE:
            result = self.fail_response(resp.context['result'])
        elif resp_type == ERROR_RESPONSE:
            error_message = 'Unknown Error'
            if 'error_message' in resp.context:
                message = resp.context['error_message']

            code = None
            if 'error_code' in resp.context:
                code = resp.context['error_code']

            data = None
            if 'error_data' in resp.context:
                data = resp.context['error_data']

            result = self.error_response(message, code, data)
        else:
            raise ResponseError('Unknown response type {}'.format(resp_type))

        resp.body = json.dumps(result)

    def success_response(self, data):
        return {
            'status': SUCCESS_RESPONSE,
            'data': data,
        }


    def fail_response(self, data):
        return {
            'status': FAIL_RESPONSE,
            'data': data,
        }

    def error_response(self, message, code=None, data=None):
        return {
            'status': ERROR_RESPONSE,
            'message': message,
            'code': code,
            'data': data,
        }
