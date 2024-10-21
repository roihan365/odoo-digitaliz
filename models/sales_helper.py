from collections import defaultdict
from odoo import models
from datetime import datetime

class SaleHelper(models.AbstractModel):
    _name = 'hulutarget.sale.order'

    def get_sales(self, domain, **kwargs):
        # Query the sale.order model based on the domain
        sales_orders = self.env['sale.order'].sudo().search(domain)

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
                'products': [
                    {'product': line.product_id.name, 'quantity': line.product_uom_qty, 'price': line.price_unit}
                    for line in order.order_line
                ]
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

        return [{
                'total_sales_revenue': total_sales_revenue,
                'total_orders': total_orders,
                'data': grouped_sales_list
            }
        ]
