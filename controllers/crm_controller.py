from odoo import http
from odoo.http import request
import json
from collections import defaultdict

class ApiCRMController(http.Controller):

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

    @http.route('/api/crm/all', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_all_crm(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(
                json.dumps({}),
                headers=self.cors_headers()
            )

        try:
            leads = request.env['crm.lead'].sudo().search([])

            grouped_leads = defaultdict(list)
            for lead in leads:
                company_id = lead.company_id.id if lead.company_id else None
                company_name = lead.company_id.name if lead.company_id else 'No Company'
                lead_data = {
                    'id': lead.id,
                    'name': lead.name,
                    'contact_name': lead.contact_name,
                    'email_from': lead.email_from,
                    'phone': lead.phone,
                    'stage': lead.stage_id.name if lead.stage_id else None,
                    'expected_revenue': lead.expected_revenue,
                    'probability': lead.probability,
                    'salesperson_id': lead.user_id.id if lead.user_id else None,
                    'salesperson_name': lead.user_id.name if lead.user_id else None,
                    'date_deadline': lead.date_deadline.strftime('%Y-%m-%d') if lead.date_deadline else None,
                }

                # Group leads by company and nyame (you can adjust the grouping criteria)
                grouped_leads[(company_id, company_name)].append(lead_data)

            # Convert grouped leads to a list of dictionaries
            grouped_leads_list = [
                {
                    'company_id': cmp_id,
                    'company_name': cmp_name,
                    'leads': leads
                }
                for (cmp_id, cmp_name), leads in grouped_leads.items()
            ]

            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'data': grouped_leads_list
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
