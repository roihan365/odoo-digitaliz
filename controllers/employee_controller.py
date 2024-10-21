from odoo import http
from odoo.http import request
import json
from ..utils.cors import CorsHelper

class ApiEmployeeController(http.Controller):

    @http.route('/api/employee/<int:employee_id>', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_employee(self, employee_id, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=CorsHelper.cors_headers()
            )
        
        try:
            employee = request.env['hulutarget.employee'].get_employee(employee_id)

            if employee:
                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'data': employee
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

    @http.route('/api/employee/all', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_all_employees(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=CorsHelper.cors_headers()
            )

        try:
            employees = request.env['hulutarget.employee'].get_all_employee()
            if employees:
                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'data': employees
                    }),
                    headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
                )
                
            else:
                return request.make_response(
                    json.dumps({
                        'status': 'error',
                        'message': 'No Employee Data'
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
                headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
            )
