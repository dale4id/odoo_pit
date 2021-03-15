from odoo import tools
from odoo import api, fields, models
from odoo.exceptions import ValidationError, RedirectWarning, UserError

class pitUnit(models.Model):
    _name = "product.unit"
    _description = "Unit Product"

    @tools.ormcache()
    def _get_default_uom_id(self):
        return self.env.ref('uom.product_uom_unit')

    name = fields.Char(string='Name', compute='_compute_combi_name', readonly=True, store=True)
    description = fields.Char(string='Description', compute='_compute_combi_name', readonly=True, store=True)
    company_id = fields.Many2one('res.company', 'Company', index=1)
    serial = fields.Char(string="Serial Number", required=True)
    model = fields.Char(string="Model", required=True)
    merk = fields.Char(string="Merk")
    unit_type = fields.Many2one('unit.type', string="Unit Type", required=True)
    logo = fields.Char(string="Branding")
    owner = fields.Many2one('res.partner', string="Owner")
    location = fields.Char(string="Location")
    no_tlp = fields.Char(string="No Hp")
    pic = fields.Char(string="PIC")
    alamat = fields.Text(string="Alamat")
    city = fields.Many2one('res.city', string="Kota")
    kode_pos = fields.Char(string="Kode Pos", related="city.zipcode", readonly=True)
    uom_id = fields.Many2one('uom.uom', 'Unit of Measure', default=_get_default_uom_id, readonly="true")
    image = fields.Binary(string="Image", store=True)
    no_reges = fields.Char(string="No Registrasi")
    no_reges_change = fields.Char(string="No Registrasi Unit Pengganti")
    unit_categ = fields.Selection([
        ('0', 'Unit Kecil'),
        ('1', 'Unit Besar')
    ], default="0", string="Unit Category")
    # unit_origin = fields.Selection([
    #     ('0', 'Sadhana'),
    #     ('1', 'Others')
    # ], default="0", string="Unit Origin")
    tgl_buy = fields.Date(string="Tgl Pembelian")
    tgl_exp = fields.Date(string="Tgl Exp Garansi")
    unit_customer_id = fields.Many2one('res.partner', string="Unit Origin")


    @api.depends('serial', 'unit_type', 'model')
    def _compute_combi_name(self):
        for record in self:
            getType = record.unit_type.name[:3]
            getModel = record.model[:2]

            record.description = record.serial + getModel.upper() + getType.upper()
            record.name = record.description + " - " + record.model

            
    



