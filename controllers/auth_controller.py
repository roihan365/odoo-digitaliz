from odoo import http
from odoo.http import request
import json

class AuthController(http.Controller):

    @http.route('/api/login', type='http', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        try:
            json_data = json.loads(request.httprequest.data)
            username = json_data.get('username')
            password = json_data.get('password')

            if not username or not password:
                return request.make_response(
                    json.dumps({
                        'status': 'error',
                        'message': 'Username and password are required'
                    }),
                    headers=[('Content-Type', 'application/json')]
                )

            uid = request.session.authenticate(request.session.db, username, password)

            if uid:
                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'message': 'Login successful'
                    }),
                    headers=[('Content-Type', 'application/json')]
                )
            else:
                return request.make_response(
                    json.dumps({
                        'status': 'error',
                        'message': 'Invalid credentials'
                    }),
                    headers=[('Content-Type', 'application/json')]
                )
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                headers=[('Content-Type', 'application/json')]
            )

    @http.route('/api/logout', type='http', auth='user', methods=['POST'], csrf=False)
    def logout(self):
        try:
            request.session.logout()
            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'message': 'Logout successful'
                }),
                headers=[('Content-Type', 'application/json')]
            )
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                headers=[('Content-Type', 'application/json')]
            )