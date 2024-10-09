from odoo import http
from odoo.http import request
import json

class ApiEmployeeController(http.Controller):

    def cors_headers(self):
        allowed_origins = [
            'http://hulutalent.test',
            'https://hulu.dtz-internal-only.com',
            'https://app.hulutarget.id'
        ]

        # Periksa apakah origin request berada dalam daftar allowed_origins
        origin = self.request.headers.get('Origin')
        
        if origin in allowed_origins:
            return [
                ('Access-Control-Allow-Origin', origin),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
            ]
        else:
            # Jika origin tidak diizinkan, tidak memberikan CORS headers
            return [
                ('Access-Control-Allow-Origin', 'null'),  # Atau bisa dikosongkan, sesuai kebutuhan
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With')
            ]

    @http.route('/api/employee/<int:employee_id>', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_employee(self, employee_id, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=self.cors_headers()
            )
        
        try:
            employee = request.env['hr.employee'].sudo().browse(employee_id)

            if employee.exists():
                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'data': {
                            'id': employee.id,
                            'name': employee.name,
                            'email': employee.work_email,
                            'phone': employee.work_phone,
                            'company': employee.company_id.name if employee.company_id else None,
                            'department': employee.department_id.name if employee.department_id else None,
                            'position': employee.job_id.name if employee.job_id else None,
                        }
                    }),
                    headers=[('Content-Type', 'application/json')] + self.cors_headers()
                )
            else:
                return request.make_response(
                    json.dumps({
                        'status': 'error',
                        'message': 'Record not found'
                    }),
                    headers=[('Content-Type', 'application/json')] + self.cors_headers()
                )
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                headers=[('Content-Type', 'application/json')] + self.cors_headers(),
                status=500
            )

    @http.route('/api/employee/all', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_all_employees(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=self.cors_headers()
            )

        try:
            employees = request.env['hr.employee'].sudo().search([])

            employee_list = [{
                'id': employee.id,
                'name': employee.name,
                'email': employee.work_email,
                'phone': employee.work_phone,
                'company': employee.company_id.name if employee.company_id else None,
                'department': employee.department_id.name if employee.department_id else None,
                'position': employee.job_id.name if employee.job_id else None,
            } for employee in employees]

            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'data': employee_list
                }),
                headers=[('Content-Type', 'application/json')] + self.cors_headers()
            )

        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                headers=[('Content-Type', 'application/json')] + self.cors_headers()
            )
