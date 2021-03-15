from odoo import models, fields

class Addcompanytax(models.Model):
    _inherit = 'res.company'

    fax_isdcustom = fields.Char('Fax company')
    address_line = fields.One2many('isd.delivery.address', 'company_id', string='Address Lines', copy=True)

class Addcontactpartner(models.Model):
    _inherit = 'res.partner'

    isd_contact_person = fields.Char('Contact Person')

class Addsaleorder(models.Model):
    _inherit = 'sale.order'

    isd_phone = fields.Char('Phone')
    isd_pic = fields.Char('PIC')

class Addpurchaseorder(models.Model):
    _inherit = 'purchase.order'
#
#     isd_no_mpb_or_pr = fields.Char('No. MPB / No. PR')
#     isd_street_pengiriman = fields.Char('Street')
#     isd_city_pengiriman = fields.Char('City')
    isd_address_pengiriman = fields.Many2one('isd.delivery.address', string="Delivery Address")

