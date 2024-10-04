from odoo import http
from odoo.http import request
import json

class ApiEmployeeController(http.Controller):

    # Utility function to add CORS headers
    def _set_cors_headers(self, response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        return response

    @http.route('/api/employee/<int:employee_id>', type='http', auth='apikey', methods=['GET'], csrf=False)
    def get_employee(self, employee_id, **kwargs):
        try:
            # Fetching the employee record based on ID
            employee = request.env['hr.employee'].sudo().browse(employee_id)

            if employee.exists():
                response = request.make_response(
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
                    headers=[('Content-Type', 'application/json')]
                )
                return self._set_cors_headers(response)
            else:
                response = request.make_response(
                    json.dumps({
                        'status': 'error',
                        'message': 'Record not found'
                    }),
                    headers=[('Content-Type', 'application/json')]
                )
                return self._set_cors_headers(response)

        except Exception as e:
            response = request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)  # This will help you capture the actual error
                }),
                headers=[('Content-Type', 'application/json')],
                status=500  # Return a 500 status code
            )
            return self._set_cors_headers(response)

    @http.route('/api/employee/all', type='http', auth='apikey', methods=['GET'], csrf=False)
    def get_all_employees(self, **kwargs):
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

            response = request.make_response(
                json.dumps({
                    'status': 'success',
                    'data': employee_list
                }),
                headers=[('Content-Type', 'application/json')]
            )
            return self._set_cors_headers(response)

        except Exception as e:
            response = request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                headers=[('Content-Type', 'application/json')]
            )
            return self._set_cors_headers(response)
