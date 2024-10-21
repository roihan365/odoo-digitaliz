from odoo import http
from odoo.http import request
import json
from ..utils.cors import CorsHelper

class ApiAttendanceController(http.Controller):
    @http.route('/api/attendance/<int:employee_id>', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_attendance(self, employee_id, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(json.dumps({}), headers=CorsHelper.cors_headers())
        
        try:
            attendances = request.env['hulutarget.attendance'].get_attendance(employee_id)
            if attendances:
                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'data': attendances
                    }),
                    headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
                )
            else:
                return request.make_response(
                    json.dumps({
                        'status': 'error',
                        'message': 'Record not found'
                    }),
                    headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers(),
                    status=404
                )
            
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers(),
                status=500
            )


    @http.route('/api/attendance/all', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_all_attendances(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(json.dumps({}), headers=CorsHelper.cors_headers())

        try:
            attendances = request.env['hulutarget.attendance'].get_all_attendances()

            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'data': attendances
                }),
                headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
            )

        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers(),
                status=500
            )
