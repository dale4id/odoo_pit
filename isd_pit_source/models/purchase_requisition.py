from odoo import models, api


class PurchaseRequisitionLine(models.Model):
    _inherit = "purchase.requisition.line"

    def _prepare_purchase_order_line(self, name, product_qty=0.0, price_unit=0.0, taxes_ids=False):
        res = super(PurchaseRequisitionLine, self)._prepare_purchase_order_line(name, product_qty, price_unit, taxes_ids)
        res['product_qty'] -= self.qty_ordered

        return res

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('requisition_id')
    def _onchange_requisition_id(self, arrTemp=None):
        super(PurchaseOrder, self)._onchange_requisition_id()

        child_list = list()
        for objOrder_line in self.order_line:
            if objOrder_line.product_qty != 0:
                val = {
                    'name': objOrder_line.name,
                    'product_id': objOrder_line.product_id.id,
                    'product_uom': objOrder_line.product_uom.id,
                    'product_qty': objOrder_line.product_qty,
                    'price_unit': objOrder_line.price_unit,
                    'date_planned': objOrder_line.date_planned,
                    'account_analytic_id': objOrder_line.account_analytic_id.id,
                    'analytic_tag_ids': objOrder_line.analytic_tag_ids.ids,
                }
                if objOrder_line.taxes_id.id:
                    val['taxes_id'] = [(6, 0, objOrder_line.taxes_id.id)]
                child_list.append((0, 0, val))

        self.order_line.unlink()
        self.order_line = child_list

