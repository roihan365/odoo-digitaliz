# -*- coding: utf-8 -*-
from odoo import fields, models

class Digitaliz(models.Model):
    _name = 'digitaliz'
    _description = 'Digitaliz module'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description') 