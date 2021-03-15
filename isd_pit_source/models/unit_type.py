from odoo import api, fields, models
from odoo.exceptions import ValidationError, RedirectWarning, UserError

class pitUnitType(models.Model):
    _name = "unit.type"
    _description = "Master Type Unit"

    name = fields.Char(string="Type Name")
    unit_code = fields.Char('Type Code', index=True)