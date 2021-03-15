from odoo import models, api, fields
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = "account.move"

    batch_id = fields.Many2one('account.move.batch', string='Batch')
    tgl_giro = fields.Date(string="Giro Date")
    no_cek = fields.Char(string="No Cek/Bg")
    paid_to = fields.Selection([
        ('Cash', 'Cash'),
        ('Giro', 'Giro'),
        ('Transfer', 'Transfer')
    ], default="Cash", string="Paid To")

    def action_invoice_batch(self):
        lstAccountMove = self.env['account.move'].browse(self._context.get('active_ids'))
        for objAccountMove in lstAccountMove:
            if objAccountMove.batch_id.id:
                raise ValidationError("Invoice " + objAccountMove.name + " sudah masuk kedalam batch : " + objAccountMove.batch_id.name)

        strName = "BTC/" + fields.Datetime.now().strftime("%Y/%m/")
        objAccountBatch = self.env['account.move.batch'].sudo().search([], limit=1, order="name desc")
        if objAccountBatch.id:
            strtemp = "00000" + str(int(objAccountBatch.name[-5:]) + 1)
            strName = strName + strtemp[-5:]
        else:
            strName = strName + "00001"

        objDataSo = {
            'name': strName,
            'batch_date': fields.Datetime.now(),
        }
        objBatch = self.env['account.move.batch'].sudo().create(objDataSo)
        for objAccountMove in lstAccountMove:
            objAccountMove.batch_id = objBatch.id

        context = dict(self.env.context)
        #context['form_view_initial_mode'] = 'edit'
        return {
            'name': 'Batch Invoice',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'account.move.batch',
            'res_id': objBatch.id,
            'type': 'ir.actions.act_window',
            'target': 'current',
            'nodestroy': True,
            'context': context,
        }

class BatchAccountMove(models.Model):
    _name = "account.move.batch"

    move_id = fields.One2many('account.move', inverse_name='batch_id', string='Invoice')
    name = fields.Char(string='Batch Name')
    company_id = fields.Many2one(related='move_id.company_id', store=True, readonly=True,
                                 default=lambda self: self.env.company)
    batch_date = fields.Date(string="Date")

    def unlink(self):
        for objAccountMove in self.move_id:
            objAccountMove.batch_id = False
        ret = super(BatchAccountMove, self).unlink()
        return ret