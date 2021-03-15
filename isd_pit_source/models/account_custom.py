from odoo.addons.isd_pit_source.models import amount_to_text_id
from odoo import models, fields, api

class accountmoveCustom(models.Model):
    _inherit = 'account.move'

    def isd_amount_to_text(self, amount, currency='idr'):
        return amount_to_text_id.amount_to_text_id(amount, currency);

class accountpaymentCustom(models.Model):
    _inherit = 'account.payment'

    def isd_amount_to_text(self, amount, currency='idr'):
        return amount_to_text_id.amount_to_text_id(amount, currency);
