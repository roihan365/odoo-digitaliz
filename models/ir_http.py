# models/ir_http.py

from odoo import models
from odoo.http import request
from werkzeug.exceptions import BadRequest

class IrHttp(models.AbstractModel):
    _inherit = "ir.http"

    @classmethod
    def _auth_method_apikey(cls):
        api_key = request.httprequest.headers.get("Authorization")
        if not api_key:
            raise BadRequest("Authorization header with API key missing")

        # Strip 'Bearer ' prefix if present
        if api_key.startswith("Bearer "):
            api_key = api_key[len("Bearer "):]

        # Check the API key against the database
        user_id = request.env["res.users.apikeys"]._check_credentials(scope="rpc", key=api_key)
        if not user_id:
            raise BadRequest("API key invalid")

        # Update the environment with the user ID
        request.update_env(user=user_id)
