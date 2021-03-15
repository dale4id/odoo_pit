from odoo.addons.isd_pit_source.models import amount_to_text_id
from odoo import models, fields, api

class PurchaseOrderCustom(models.Model):
    _inherit = 'stock.picking'

    name_ref = fields.Char('Reference Name')

    def isd_amount_to_text(self, amount, currency='idr'):
        return amount_to_text_id.amount_to_text_id(amount, currency)