from odoo import http
from odoo.http import request
import json

class EmployeeController(http.Controller):

    import json
from odoo import http
from odoo.http import request

class ApiEmployeeController(http.Controller):

    @http.route('/api/employee/<int:employee_id>', type='http', auth='apikey', methods=['GET'], csrf=False, cors='*')
    def get_employee(self, employee_id, **kwargs):
        try:
            # Fetching the employee record based on ID
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
                    headers=[('Content-Type', 'application/json')]
                )
            else:
                return request.make_response(
                    json.dumps({
                        'status': 'error',
                        'message': 'Record not found'
                    }),
                    headers=[('Content-Type', 'application/json')]
                )
        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)  # This will help you capture the actual error
                }),
                headers=[('Content-Type', 'application/json')],
                status=500  # Return a 500 status code
            )


    @http.route('/api/employee/all', type='http', auth='apikey', methods=['GET'], csrf=False, cors='*')
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

            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'data': employee_list
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
