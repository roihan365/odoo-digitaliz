from odoo import http
from odoo.http import request
import json

class EmployeeController(http.Controller):

    @http.route('/api/employee', type='json', auth='user', methods=['POST'], csrf=False)
    def create_employee(self, **kwargs):
        try:
            if not request.session.uid:
                return {
                        'status': 'error',
                        'message': 'User not authenticated'
                    }
            raw_data = request.httprequest.data.decode('utf-8')
            data = json.loads(raw_data)

            name = data.get('name')

            record = request.env['res.partner'].sudo().create({
                'name': name,
            })

            return {
                    'status': 'success',
                    'message': 'Data has been saved successfully!',
                    'id': record.id
                }

        except Exception as e:
            return {
                    'status': 'error',
                    'message': str(e)
                }

    @http.route('/api/employee/<int:employee_id>', type='json', auth='user', methods=['GET'], csrf=False)
    def get_employee(self, employee_id, **kwargs):
        try:
            if not request.session.uid:
                return {
                        'status': 'error',
                        'message': 'User not authenticated'
                    }
            employee = request.env['hr.employee'].sudo().browse(employee_id)

            if employee.exists():
                return {
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
                    }
            else:
                return {
                        'status': 'error',
                        'message': 'Record not found'
                    }
        except Exception as e:
            return {
                    'status': 'error',
                    'message': str(e)
                }

    @http.route('/api/employee/all', type='json', auth='user', methods=['GET'], csrf=False)
    def get_all_employees(self, **kwargs):
        try:
            if not request.session.uid:
                return {
                        'status': 'error',
                        'message': 'User not authenticated'
                    }
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

            return {
                    'status': 'success',
                    'data': employee_list
                }

        except Exception as e:
            return {
                    'status': 'error',
                    'message': str(e)
                }
