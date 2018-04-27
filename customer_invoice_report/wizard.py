#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2011 OpenERP SA (<http://openerp.com>). All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from openerp import models, fields, api


class InvoiceWiseDetail(models.Model):
    _name = "cust.invoice"

    customer = fields.Many2one('res.partner', string="Customer", required=True)
    by_customer = fields.Many2one('by.customer', string="By Customer", requried=True)
    site = fields.Many2one('import.site', string="Site", requried=True)
    date_from = fields.Date("Date From", required=True)
    date_to = fields.Date("Date To", required=True)



class ResPartnerExt(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def customer_invoice_account(self):
        return {'name': 'Customer Invoice Account',
                'domain': [],
                'res_model': 'cust.invoice',
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'view_type': 'form',
                'context': {'default_customer': self.id},
                'target': 'new', }