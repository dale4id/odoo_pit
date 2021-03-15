from odoo import models, fields, api
import requests
import json

from odoo.exceptions import ValidationError
from odoo.tools import GettextAlias


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    isd_total_work_hour = fields.Integer(string='Total Working Hour')
    sts_service_unit = fields.Selection([
        ('0', 'Kecil'),
        ('1', 'Besar')
    ], string="Status Unit", default="0", required=True, tracking=True)