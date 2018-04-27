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
from num2words import num2words
import re
class PacificCommercialInvoice(models.AbstractModel):
    _name = 'report.logistic_vision.logistic_invoice'

    @api.model
    def render_html(self,docids, data=None):
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('logistic_vision.logistic_invoice')
        records = self.env['account.invoice'].browse(docids)

        users = self.env['res.users'].search([])
        def getname():
            active_user = self._uid
            for x in users:
                if active_user == x.id:
                    return x.name

        enter = []
        count = 0
        for x in records.invoice_line_ids:
            count = count + 1
            enter.append(x)


        number = []
        for x in range(9 - len(enter)):
            number.append(x)



        def number_to_spell(attrb):
            word = num2words((attrb))
            word = word.title() + " " + " SR Only"
            return word

        docargs = {
            'doc_ids': docids,
            'doc_model': 'account.invoice',
            'docs': records,
            'getname': getname,
            'number': number,
            'count': count,
            'number_to_spell':number_to_spell,
            }

        return report_obj.render('logistic_vision.logistic_invoice', docargs)