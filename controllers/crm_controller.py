# my_module/controllers/api_controller.py
from odoo import http
from odoo.http import request
import json
from ..utils.cors import CorsHelper

class ApiCRMController(http.Controller):

    @http.route('/api/crm/all', type='http', auth='apikey', methods=['GET', 'OPTIONS'], csrf=False)
    def get_all_crm(self, **kwargs):
        if request.httprequest.method == 'OPTIONS':
            return request.make_response(json.dumps({}), headers=CorsHelper.cors_headers())

        try:
            leads = request.env['hulutarget.crm.lead'].get_all_leads()

            return request.make_response(
                json.dumps({
                    'status': 'success',
                    'data': leads
                }),
                headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers()
            )

        except Exception as e:
            return request.make_response(
                json.dumps({
                    'status': 'error',
                    'message': str(e)
                }),
                headers=[('Content-Type', 'application/json')] + CorsHelper.cors_headers(),
                status=500
            )


