from odoo.http import request

class CorsHelper:
    
    @staticmethod
    def cors_headers():
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
        return []
