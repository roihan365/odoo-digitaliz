from odoo import http
from odoo.http import request
import json
from datetime import datetime
from collections import defaultdict

class ApiSalesController(http.Controller):

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

    @http.route('/api/sales/<int:employee_id>', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_sales(self, employee_id, start_date=None, end_date=None, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=self.cors_headers()
            )

        try:
            # Date filtering (if provided)
            domain = [('user_id', '=', employee_id)]

            # Parse and apply date filters if provided
            if start_date:
                try:
                    start_date_obj = datetime.strptime(start_date, '%Y-%m-%d')
                    domain.append(('date_order', '>=', start_date_obj))
                except ValueError:
                    return request.make_response(
                        json.dumps({'status': 'error', 'message': 'Invalid start_date format. Use YYYY-MM-DD.'}),
                        headers=[('Content-Type', 'application/json')] + self.cors_headers()
                    )

            if end_date:
                try:
                    end_date_obj = datetime.strptime(end_date, '%Y-%m-%d')
                    domain.append(('date_order', '<=', end_date_obj))
                except ValueError:
                    return request.make_response(
                        json.dumps({'status': 'error', 'message': 'Invalid end_date format. Use YYYY-MM-DD.'}),
                        headers=[('Content-Type', 'application/json')] + self.cors_headers()
                    )
            # Query sale.order model
            sales_orders = request.env['sale.order'].sudo().search(domain)

            if sales_orders.exists():
                grouped_sales = defaultdict(list)
                total_sales_revenue = 0
                total_orders = 0

                for order in sales_orders:
                    total_sales_revenue += order.amount_total
                    total_orders += 1

                    # Format the sales order data
                    sales_data = {
                        'id': order.id,
                        'date_order': order.date_order.strftime('%Y-%m-%d %H:%M:%S') if isinstance(order.date_order, datetime) else None,
                        'amount_total': order.amount_total,
                        'salesperson': order.user_id.name if order.user_id else None,
                        'sales_team': order.team_id.name if order.team_id else None,
                        'status': order.state,
                        'products': [{'product': line.product_id.name, 'quantity': line.product_uom_qty, 'price': line.price_unit}
                                     for line in order.order_line]
                    }

                    # Group sales by employee_id and employee name
                    grouped_sales[(order.user_id.id, order.user_id.name)].append(sales_data)

                # Convert grouped sales to a list of dictionaries
                grouped_sales_list = [
                    {
                        'salesperson_id': emp_id,
                        'salesperson': emp_name,
                        'sales_orders': sales_orders
                    }
                    for (emp_id, emp_name), sales_orders in grouped_sales.items()
                ]

                return request.make_response(
                    json.dumps({
                        'status': 'success',
                        'total_sales_revenue': total_sales_revenue,
                        'total_orders': total_orders,
                        'data': grouped_sales_list
                    }),
                    headers=[('Content-Type', 'application/json')] + self.cors_headers()
                )
            else:
                return request.make_response(
                    json.dumps({
                        'status': 'error',
                        'message': 'No sales orders found for the employee'
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

    @http.route('/api/sales/all', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_all_sales(self, start_date=None, end_date=None, salesperson_id=None, sales_team_id=None, order_status=None, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=self.cors_headers()
            )

        try:
            # Build the domain based on filters
            domain = []
            if start_date:
                domain.append(('date_order', '>=', start_date))
            if end_date:
                domain.append(('date_order', '<=', end_date))
            if salesperson_id:
                domain.append(('user_id', '=', salesperson_id))
            if sales_team_id:
                domain.append(('team_id', '=', sales_team_id))
            if order_status:
                domain.append(('state', '=', order_status))

            # Query sale.order model
            sales_orders = request.env['sale.order'].sudo().search(domain)

            grouped_sales = defaultdict(lambda: {'sales_orders': [], 'total_sales_revenue': 0})
            total_sales_revenue_global = 0
            total_orders = 0

            for order in sales_orders:
                total_sales_revenue_global += order.amount_total
                total_orders += 1

                # Format the sales order data
                sales_data = {
                    'id': order.id,
                    'date_order': order.date_order.strftime('%Y-%m-%d %H:%M:%S') if isinstance(order.date_order, datetime) else None,
                    'amount_total': order.amount_total,
                    'salesperson': order.user_id.name if order.user_id else None,
                    'sales_team': order.team_id.name if order.team_id else None,
                    'status': order.state,
                    'products': [{'product': line.product_id.name, 'quantity': line.product_uom_qty, 'price': line.price_unit}
                                 for line in order.order_line]
                }

                # Group sales by salesperson
                sales_group = grouped_sales[(order.user_id.id, order.user_id.name)]
                sales_group['sales_orders'].append(sales_data)
                sales_group['total_sales_revenue'] += order.amount_total

            # Convert grouped sales to a list of dictionaries
            grouped_sales_list = [
                {
                    'salesperson_id': emp_id,
                    'salesperson': emp_name,
                    'total_sales_revenue': group_data['total_sales_revenue'],
                    'sales_orders': group_data['sales_orders']
                }
                for (emp_id, emp_name), group_data in grouped_sales.items()
            ]

            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'total_sales_revenue_global': total_sales_revenue_global,
                    'total_orders': total_orders,
                    'data': grouped_sales_list
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
