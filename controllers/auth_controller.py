from odoo import http
from odoo.http import request
import json

class AuthController(http.Controller):

    @http.route('/api/login', type='json', auth='public', methods=['POST'], csrf=False)
    def login(self, **kwargs):
        try:
            json_data = json.loads(request.httprequest.data)
            username = json_data.get('username')
            password = json_data.get('password')

            if not username or not password:
                return{
                        'status': 'error',
                        'message': 'Username and password are required'
                    }

            uid = request.session.authenticate(request.session.db, username, password)

            if uid:
                return {
                        'status': 'success',
                        'message': 'Login successful'
                    }
            else:
                return {
                        'status': 'error',
                        'message': 'Invalid credentials'
                    }
        except Exception as e:
            return {
                    'status': 'error',
                    'message': str(e)
                }

    @http.route('/api/logout', type='json', auth='user', methods=['POST'], csrf=False)
    def logout(self):
        try:
            request.session.logout()
            return {
                    'status': 'success',
                    'message': 'Logout successful'
                }
        except Exception as e:
            return {
                    'status': 'error',
                    'message': str(e)
                }