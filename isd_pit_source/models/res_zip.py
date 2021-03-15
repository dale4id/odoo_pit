# Copyright 2018 Aitor Bouzas <aitor.bouzas@adaptivecity.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models, api


class ResCityZip(models.Model):
    """City/locations completion object"""

    _name = "res.city.zip"
    _description = __doc__
    _order = "name asc"
    _rec_name = "name"

    name = fields.Char("ZIP", required=True)

    city_id = fields.Many2one(
        "res.city",
        "City",
        required=True,
        auto_join=True,
        ondelete="cascade",
        index=True,
    )
    display_name = fields.Char(
        compute="_compute_new_display_name", store=True, index=True
    )


    @api.depends("name", "city_id")
    def _compute_new_display_name(self):
        for rec in self:
            name = [rec.name, rec.city_id.name]
            if rec.city_id.state_id:
                name.append(rec.city_id.state_id.name)
            if rec.city_id.country_id:
                name.append(rec.city_id.country_id.name)
            rec.display_name = ", ".join(name)


class City(models.Model):
    _name = "res.city"

    state = fields.Char("state")
    name = fields.Char("name")
    zipcode = fields.Char("zipcode")
    zip_ids = fields.One2many("res.city.zip", "city_id", string="Zips in this city")

