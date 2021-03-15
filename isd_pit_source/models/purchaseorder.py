
from odoo import models, fields, api
from odoo.exceptions import ValidationError
from odoo.tools.safe_eval import pytz


class IrActionsReport(models.Model):
    _inherit = "ir.actions.report"

    @api.model
    def _render_qweb_html(self, docids, data=None):
        # function tambahan untuk counter report

        #if docids == None: raise ValidationError("No document to show")
        if self.report_name == 'isd_pit_source.report_po_custom':
            data_counter_print = self.env['purchase.order'].browse(docids)
            for obj in data_counter_print:
                if obj.state != "purchase": raise ValidationError("Purchase order belum terconfirm")

        return super(IrActionsReport, self)._render_qweb_html(docids, data)
