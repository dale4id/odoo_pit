# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from ast import literal_eval
from lxml import etree
import time

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError, UserError
from odoo.addons.base.models.ir_model import MODULE_UNINSTALL_FLAG


class ProjectWorksheetTemplate(models.Model):
    _inherit = 'project.worksheet.template'

    @api.model
    def create(self, vals):
        template = super().create(vals)


        return template

    def write(self, vals):
        return super(ProjectWorksheetTemplate, self).write(vals)

