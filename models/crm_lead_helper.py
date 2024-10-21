# my_module/models/crm_lead_helper.py
from collections import defaultdict
from odoo import models
from datetime import datetime

class CrmLeadHelper(models.AbstractModel):
    _name = 'hulutarget.crm.lead'
    
    def get_all_leads(self):
        leads = self.env['crm.lead'].sudo().search([])
        grouped_leads = defaultdict(list)

        for lead in leads:
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

            company_id = lead.company_id.id if lead.company_id else None
            company_name = lead.company_id.name if lead.company_id else 'No Company'

            grouped_leads[(company_id, company_name)].append(lead_data)

        return [
            {
                'company_id': cmp_id,
                'company_name': cmp_name,
                'leads': leads
            }
            for (cmp_id, cmp_name), leads in grouped_leads.items()
        ]
