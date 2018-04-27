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
###################################################
from datetime import date
from num2words import num2words
from odoo import models, fields, api


class SampleDevelopmentReport(models.AbstractModel):
    _name = 'report.customer_invoice_report.module_report'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('customer_invoice_report.module_report')
        active_wizard = self.env['cust.invoice'].search([])
        emp_list = []
        for x in active_wizard:
            emp_list.append(x.id)
        emp_list = emp_list
        emp_list_max = max(emp_list)

        record_wizard = self.env['cust.invoice'].search([('id','=',emp_list_max)])

        record_wizard_del = self.env['cust.invoice'].search([('id', '!=', emp_list_max)])
        record_wizard_del.unlink()
        date_from = record_wizard.date_from
        date_to = record_wizard.date_to
        customer = record_wizard.customer
        by_customer = record_wizard.by_customer
        site = record_wizard.site

        if site:
            rec = self.env['account.invoice'].search([('date_invoice', '>=', date_from), ('date_invoice', '<=', date_to),
                                                  ('partner_id', '=', customer.id), ('by_customer', '=', by_customer.id),
                                                  ('type', '=', 'out_invoice'),('state', '=', 'open'),('customer_site', '=', site.id)])
        if not site:
            rec = self.env['account.invoice'].search([('date_invoice', '>=', date_from), ('date_invoice', '<=', date_to),
                                                  ('partner_id', '=', customer.id), ('by_customer', '=', by_customer.id),
                                                  ('type', '=', 'out_invoice'),('state', '=', 'open')])

        def get_terminal_cost(rec_id):
            for xx in rec:
                if xx.id == rec_id:
                    for y in xx.invoice_line_ids:
                        if 'Custom Examination charges' in y.account_id.name:
                            return y.price_subtotal
                    else:
                        return 0.0

        def get_custom_cost(rec_id):
            for xx in rec:
                if xx.id == rec_id:
                    for y in xx.invoice_line_ids:
                        if 'Custom Clearance Charges' in y.account_id.name:
                            return y.price_subtotal
                    else:
                        return 0.0

        def get_duty_cost(rec_id):
            for xx in rec:
                if xx.id == rec_id:
                    for y in xx.invoice_line_ids:
                        if 'Gov. Custom Duty Payables' in y.account_id.name:
                            return y.price_subtotal
                    else:
                        return 0.0

        def get_other_charges(rec_id):
            for xx in rec:
                if xx.id == rec_id:
                    for y in xx.invoice_line_ids:
                        if 'Gov. Custom Duty Payables' not in y.account_id.name and 'Custom Clearance Charges' \
                                not in y.account_id.name and 'Custom Examination charges' not in y.account_id.name:
                            return y.price_subtotal
                    else:
                        return 0.0

        def number_to_spell(attrb):
            word = num2words((attrb))
            word = word.title() + " " + "SAR Only"
            return word

        def getname():
            name = self.env['res.users'].search([('id', '=', self._uid)]).name
            return name

        docargs = {
            'doc_ids': docids,
            'doc_model': 'res.partner',
            'rec': rec,
            'get_terminal_cost':get_terminal_cost,
            'get_custom_cost': get_custom_cost,
            'get_duty_cost': get_duty_cost,
            'get_other_charges': get_other_charges,
            'customer':customer.name,
            'by_customer':by_customer.name,
            'date':date.today(),
            'number_to_spell':number_to_spell,
            'customer_id':customer.id,
            'getname':getname,
        }

        return report_obj.render('customer_invoice_report.module_report', docargs)


