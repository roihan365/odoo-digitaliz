from collections import defaultdict
from odoo import models
from datetime import datetime

class HrAttendanceHelper(models.AbstractModel):
    _name = 'hulutarget.attendance'

    def get_all_attendances(self):
        attendances = self.env['hr.attendance'].sudo().search([])
        grouped_attendance = defaultdict(list)

        for attendance in attendances:
            attendance_data = {
                'id': attendance.id,
                'check_in': attendance.check_in.strftime('%Y-%m-%d %H:%M:%S') if isinstance(attendance.check_in, datetime) else None,
                'check_out': attendance.check_out.strftime('%Y-%m-%d %H:%M:%S') if isinstance(attendance.check_out, datetime) else None,
                'worked_hours': attendance.worked_hours,
                'overtime_hours': attendance.overtime_hours,
            }

            employee_id = attendance.employee_id.id if attendance.employee_id else None
            employee_name = attendance.employee_id.name if attendance.employee_id else None

            grouped_attendance[(employee_id, employee_name)].append(attendance_data)

        return [
            {
                'employee_id': emp_id,
                'employee': emp_name,
                'attendances': attendances
            }
            for (emp_id, emp_name), attendances in grouped_attendance.items()
        ]

    def get_attendance(self, employee_id):     
        employee_attendance = self.env['hr.attendance'].sudo().search([('employee_id', '=', employee_id)])

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

        return [
            {
                'employee_id': emp_id,
                'employee': emp_name,
                'attendances': attendances
            }
            for (emp_id, emp_name), attendances in grouped_attendance.items()
        ]