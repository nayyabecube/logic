# -*- coding: utf-8 -*- 
from odoo import models, fields, api

class FilterWizard(models.Model):
	_name = "filters.wizard"

	bl = fields.Char(string="BL Number")
	ref = fields.Char(string="Customer Ref")
	bn = fields.Char(string="Bayan Number")
	c_n = fields.Char(string="Container Number")
	m_name = fields.Char(string="Model")
	
	@api.multi
	def get_result(self):
		if not self.bl:
			self.bl = "^"
		if not self.ref:
			self.ref = "^"
		if not self.bn:
			self.bn = "^"
		if not self.c_n:
			self.c_n = "^"

		if self.c_n and self.m_name == 'export.logic':
			records = self.env[self.m_name].search([])
			if records:
				for x in records:
					x.tick = False
					if x.export_id:
						for y in x.export_id:
							if y.crt_no == self.c_n:
								x.tick = True

		if self.c_n and self.m_name == 'import.logic':
			records = self.env[self.m_name].search([])
			if records:
				for x in records:
					x.tick = False
					if x.import_id:
						for y in x.import_id:
							if y.crt_no == self.c_n:
								x.tick = True

		return {
		'type': 'ir.actions.act_window',
		'name': 'Custom Search',
		'res_model': self.m_name,
		'view_type': 'form',
		'view_mode': 'tree,form',
		'domain': (['|','|','|',('tick','=',True),('bill_no','=',self.bl),('customer_ref','=',self.ref),('bayan_no','=',self.bn)]),
		}