from odoo import http
from odoo.http import request
import json
from datetime import datetime
from ..utils.cors import CorsHelper

class ApiSalesController(http.Controller):

    @http.route('/api/sales/<int:employee_id>', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_sales(self, employee_id, start_date=None, end_date=None, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=CorsHelper.cors_headers()
            )

        try:
            # Domain filtering by employee
            domain = [('user_id', '=', employee_id)]

            # Parse and apply date filters if provided
            if start_date:
                try:
                    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                    domain.append(('date_order', '>=', start_date_obj))
                except ValueError:
                    return request.make_response(
                        json.dumps({'status': 'error', 'message': 'Invalid start_date format. Use YYYY-MM-DD.'}),
                        headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
                    )

            if end_date:
                try:
                    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                    domain.append(('date_order', '<=', end_date_obj))
                except ValueError:
                    return request.make_response(
                        json.dumps({'status': 'error', 'message': 'Invalid end_date format. Use YYYY-MM-DD.'}),
                        headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
                    )

            # Query sales using the helper
            sales_data = request.env['hulutarget.sale.order'].get_sales(domain)

            if sales_data:
                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'total_sales_revenue': sales_data[0]['total_sales_revenue'],
                        'total_orders': sales_data[0]['total_orders'],
                        'data': sales_data[0]['data']
                    }),
                    headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
                )
            else:
                return request.make_response(
                    json.dumps({'status': 'error', 'message': 'No sales orders found for the employee'}),
                    headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers(),
                    status=404
                )

        except Exception as e:
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}),
                headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers(),
                status=500
            )

    @http.route('/api/sales/all', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_all_sales(self, start_date=None, end_date=None, salesperson_id=None, sales_team_id=None, order_status=None, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=CorsHelper.cors_headers()
            )

        try:
            # Build the domain based on filters
            domain = []
            if start_date:
                try:
                    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                    domain.append(('date_order', '>=', start_date_obj))
                except ValueError:
                    return request.make_response(
                        json.dumps({'status': 'error', 'message': 'Invalid start_date format. Use YYYY-MM-DD.'}),
                        headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
                    )

            if end_date:
                try:
                    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                    domain.append(('date_order', '<=', end_date_obj))
                except ValueError:
                    return request.make_response(
                        json.dumps({'status': 'error', 'message': 'Invalid end_date format. Use YYYY-MM-DD.'}),
                        headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
                    )

            if salesperson_id:
                domain.append(('user_id', '=', salesperson_id))
            if sales_team_id:
                domain.append(('team_id', '=', sales_team_id))
            if order_status:
                domain.append(('state', '=', order_status))

            # Query sales using the helper
            sales_data = request.env['hulutarget.sale.order'].get_sales(domain)

            if sales_data:
                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'total_sales_revenue_global': sales_data[0]['total_sales_revenue'],
                        'total_orders': sales_data[0]['total_orders'],
                        'data': sales_data[0]['data']
                    }),
                    headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
                )
            else:
                return request.make_response(
                    json.dumps({'status': 'error', 'message': 'No sales orders found'}),
                    headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers(),
                    status=404
                )

        except Exception as e:
            return request.make_response(
                json.dumps({'status': 'error', 'message': str(e)}),
                headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers(),
                status=500
            )
