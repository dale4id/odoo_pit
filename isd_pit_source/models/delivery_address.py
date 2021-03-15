from odoo import models, fields, api

class Deliveryaddress(models.Model):
    _name = 'isd.delivery.address'

    company_id = fields.Many2one('res.company', string='Company')
    name = fields.Char(string='Address Name')
    isd_street_pengiriman = fields.Char('Street')
    isd_city_pengiriman = fields.Char('City')
    isd_country_id_pengiriman = fields.Many2one('res.country', string="Country")