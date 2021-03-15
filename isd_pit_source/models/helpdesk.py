from odoo import models, fields


class HelpdeskTeam(models.Model):
    _inherit = "helpdesk.team"

    leader_user_id = fields.Many2one(
        'res.users', string='Tem Leader', default=lambda self: self.env.user)