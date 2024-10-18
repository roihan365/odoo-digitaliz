from odoo import http
from odoo.http import request
import json
from datetime import datetime
from collections import defaultdict

class ApiAttendanceController(http.Controller):

    def cors_headers(self):
        allowed_origins = [
            'http://hulutalent.test',
            'https://hulu.dtz-internal-only.com',
            'https://app.hulutarget.id'
        ]

        origin = request.httprequest.headers.get('Origin')
        if origin in allowed_origins:
            return [
                ('Access-Control-Allow-Origin', origin),
                ('Access-Control-Allow-Methods', 'GET, POST, OPTIONS'),
                ('Access-Control-Allow-Headers', 'Content-Type, Authorization, X-Requested-With'),
                ('Access-Control-Allow-Credentials', 'true') 
            ]
        else:
            return []

    @http.route('/api/attendance/<int:employee_id>', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_attendance(self, employee_id, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=self.cors_headers()
            )
        
        try:
            employee_attendance = request.env['hr.attendance'].sudo().search([('employee_id', '=', employee_id)])

            if employee_attendance.exists():
                grouped_attendance = defaultdict(list)
                for attendance in employee_attendance:
                    employee_id = attendance.employee_id.id if attendance.employee_id else None
                    employee_name = attendance.employee_id.name if attendance.employee_id else None

                    # Format the attendance data
                    attendance_data = {
                        'id': attendance.id,
                        'check_in': attendance.check_in.strftime('%Y-%m-%d %H:%M:%S') if isinstance(attendance.check_in, datetime) else None,
                        'check_out': attendance.check_out.strftime('%Y-%m-%d %H:%M:%S') if isinstance(attendance.check_out, datetime) else None,
                        'worked_hours': attendance.worked_hours,
                        'overtime_hours': attendance.overtime_hours,
                    }

                    # Group attendances by employee_id and employee name
                    grouped_attendance[(employee_id, employee_name)].append(attendance_data)

                # Convert grouped attendance to a list of dictionaries
                grouped_attendance_list = [
                    {
                        'employee_id': emp_id,
                        'employee': emp_name,
                        'attendances': attendances
                    }
                    for (emp_id, emp_name), attendances in grouped_attendance.items()
                ]

                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'data': grouped_attendance_list
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

    @http.route('/api/attendance/all', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_all_attendances(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=self.cors_headers()
            )

        try:
            attendances = request.env['hr.attendance'].sudo().search([])
            
            grouped_attendance = defaultdict(list)
            for attendance in attendances:
                employee_id = attendance.employee_id.id if attendance.employee_id else None
                employee_name = attendance.employee_id.name if attendance.employee_id else None

                # Format the attendance data
                attendance_data = {
                    'id': attendance.id,
                    'check_in': attendance.check_in.strftime('%Y-%m-%d %H:%M:%S') if isinstance(attendance.check_in, datetime) else None,
                    'check_out': attendance.check_out.strftime('%Y-%m-%d %H:%M:%S') if isinstance(attendance.check_out, datetime) else None,
                    'worked_hours': attendance.worked_hours,
                    'overtime_hours': attendance.overtime_hours,
                }

                # Group attendances by employee_id and employee name
                grouped_attendance[(employee_id, employee_name)].append(attendance_data)

            # Convert grouped attendance to a list of dictionaries
            grouped_attendance_list = [
                {
                    'employee_id': emp_id,
                    'employee': emp_name,
                    'attendances': attendances
                }
                for (emp_id, emp_name), attendances in grouped_attendance.items()
            ]

            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'data': grouped_attendance_list
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
