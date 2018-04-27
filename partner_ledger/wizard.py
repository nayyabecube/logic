# #-*- coding:utf-8 -*-
# ##############################################################################
# #
# #    OpenERP, Open Source Management Solution
# #    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
# #
# #    This program is free software: you can redistribute it and/or modify
# #    it under the terms of the GNU Affero General Public License as published by
# #    the Free Software Foundation, either version 3 of the License, or
# #    (at your option) any later version.
# #
# #    This program is distributed in the hope that it will be useful,
# #    but WITHOUT ANY WARRANTY; without even the implied warranty of
# #    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# #    GNU Affero General Public License for more details.
# #
# #    You should have received a copy of the GNU Affero General Public License
# #    along with this program.  If not, see <http://www.gnu.org/licenses/>.
# #
# ##############################################################################
from odoo import models, fields, api


class GeneratePartnerLedger(models.Model):
	_name = "partner.ledger"

	form = fields.Date(string="From")
	to = fields.Date(string="To")
	entry_type = fields.Selection([
		('posted', 'Actual Ledger'),
		('all', 'Virtual Ledger'),
		],default='posted',string="Target Moves")
	partner = fields.Many2one('res.partner',string="Partner")


class ResPartnerExt1(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def customer_statement_account(self):
        return {'name': 'Statement of Account',
                'domain': [],
                'res_model': 'partner.ledger',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_partner': self.id},
                'target': 'new', }