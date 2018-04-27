# -*- coding: utf-8 -*-
from odoo import models, fields, api

class AccountMoveLineInher(models.Model):
	_inherit = 'sale.order.line'

	crt_no           = fields.Char('Container Number')
	project_no       = fields.Char('Project Number')
	form             = fields.Many2one('from.qoute',string="From")
	to               = fields.Many2one('to.quote',string="To")
	fleet_type       = fields.Many2one('fleet',string="Fleet Type")
	product_id       = fields.Many2one('product.product',string='Product', required=False)

	@api.onchange('form','to','fleet_type')
	def add_charges(self):
		""" Calculating Charges As per Transporter, To, From, and fleet_type for selected customer"""

		if self.order_id.partner_id.id and self.form.id and self.to.id and self.fleet_type:
			trans = self.env['res.partner'].search([('id','=',self.order_id.partner_id.id)])
			for x in trans.route_id:
				if self.form.id == x.form.id and self.to.id == x.to.id and self.fleet_type == x.fleet_type:
					self.price_unit = x.trans_charges

class TransportInfo(models.Model):
	_inherit = 'sale.order'

	suppl_name    = fields.Many2one('res.partner', string = "Supplier Name",required=True)
	suppl_freight = fields.Char(string='Supplier Freight')
	by_customer   = fields.Many2one('by.customer', string="By Customer")
	bill_type     = fields.Char(string='Billing Type')
	bill_no       = fields.Char(string='B/L Number')
	inv_chk       = fields.Boolean(string="inv")
	pod_chk       = fields.Boolean(string="pod")
	freight_link  = fields.Many2one('freight.forward',string='Freight Forwarding',readonly=True)
	trans_link    = fields.Many2one('freight.forward',string='Freight Link',readonly=True)
	acc_link      = fields.Many2one('account.invoice',string='Invoice',readonly=True)
	inter_num     = fields.Integer(string="Internal Number")
	driver        = fields.Char(string = "Driver")
	driver_num    = fields.Char(string = "Driver Number")
	form_t        = fields.Many2one('from.qoute',string="From")
	to_t          = fields.Many2one('to.quote',string="To")
	fleet_type    = fields.Many2one('fleet',string="Fleet Type")
	upload_date   = fields.Date(string="Loading Date")
	delivery_date = fields.Date(string="Arrival Date")
	return_date   = fields.Date(string="Return Date")
	stuff_date    = fields.Date(string="Stuffing Date")
	recive_name   = fields.Char(string="Receiver Name")
	recive_mob    = fields.Char(string="Receiver Mobile")
	sales_id      = fields.Many2one('export.logic')
	sales_imp_id  = fields.Many2one('import.logic')

	our_job = fields.Char(string="Our Job No", required=False, )
	sr_no = fields.Char(string="Sr No", required=False, )
	customer_ref = fields.Char(string="Customer Ref", required=False, )
	custom_dec = fields.Char(string="Custom Dec", required=False, )
	bayan_no = fields.Char(string="Bayan No", required=False, )
	final_date = fields.Date(string="Final Date", required=False, )
	customer_site = fields.Many2one('import.site',string="Site", required=False, )

	state         = fields.Selection([
					('draft', 'Quotation'),
					('sent', 'Quotation Sent'),
					('sale', 'Sales Order'),
					('done', 'Locked'),
					('cancel', 'Cancelled'),
					('rec', 'Received POD'),
					], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')


	@api.onchange('partner_id')
	def get_bill(self):
		"""Get Billing Type of selected Customer"""
		if self.partner_id:
			self.bill_type = self.partner_id.bill_type

	@api.multi
	def receive(self):
		"""Creating Vendor bills from Transportation Orders"""
		if self.pod_chk == False:
			self.state = "rec"
			self.pod_chk = True
			account = self.env['account_journal.configuration'].search([])
			purchase_order = self.env['sale.order'].search([('name','=',self.name)])
			invoice = self.env['account.invoice'].search([])
			invoice_lines = self.env['account.invoice.line'].search([])

			if purchase_order:
				create_invoice = invoice.create({
					'journal_id': account.t_vendor_journal.id,
					'partner_id':self.suppl_name.id,
					'date_invoice' : purchase_order.date_order,
					'customer_site' : self.to_t.id,
					'type':"in_invoice",
					})
				for x in purchase_order.order_line:
					create_invoice_lines= invoice_lines.create({
						'product_id':1,
						'quantity':x.product_uom_qty,
						'price_unit':purchase_order.suppl_freight,
						'crt_no':x.crt_no,
						'account_id': account.t_vendor_account.id,
						'name' : x.name,
						'invoice_id' : create_invoice.id
						})

	@api.multi
	def action_invoice_create(self):
		"""Adding By_customer To Invoice"""
		new_record = super(TransportInfo, self).action_invoice_create()
		records = self.env['account.invoice'].search([('origin','=',self.name)])
		if records:
			records.by_customer = self.by_customer.id
			records.our_job = self.our_job
			records.sr_no = self.sr_no
			records.customer_ref = self.customer_ref
			records.custom_dec = self.custom_dec
			records.bayan_no = self.bayan_no
			records.customer_site = self.customer_site.id
			records.final_date = self.final_date
			self.acc_link = records.id
		return new_record

	@api.multi
	def somethinghappens(self):
		"""Creates invoices"""
		self.inv_chk = True
		self.state = "rec"
		self.action_confirm()
		self.action_invoice_create()


	@api.onchange('form','to','fleet_type')
	def add_charges(self):
		""" Calculating Charges As per Transporter, To, From, and fleet_type for selected Supplier"""

		if self.suppl_name and self.form_t.id and self.to_t.id and self.fleet_type:
			trans = self.env['res.partner'].search([('id','=',self.suppl_name.id)])
			for x in trans.route_id:
				if self.form_t.id == x.form.id and self.to_t.id == x.to.id and self.fleet_type == x.fleet_type:
					self.suppl_freight = x.trans_charges


class AccountInvoiceTree(models.Model):
	_inherit = 'account.invoice.line'
	crt_no       = fields.Char('Container No.')


class AccountInvoiceForm(models.Model):
	_inherit = 'account.invoice'
	acount_link = fields.Many2one('freight.forward',string='link')
	broker_link = fields.Many2one('export.logic',string=' Broker link')
	customer_id = fields.Many2one('res.partner',string='Customer')
	check = fields.Boolean()


	@api.onchange('partner_id')
	def get_cust(self):
		if self.partner_id:
			if "Custom Duty" in self.partner_id.name:
				self.check = True
			else:
				self.check = False


	@api.multi
	def reg_payment(self):
		return {'name': 'Payments',
				'domain': [],
				'res_model': 'customer.payment.bcube',
				'type': 'ir.actions.act_window',
				'view_mode': 'form', 'view_type': 'form',
				'context': {
				'default_partner_id':self.partner_id.id,
				'default_receipts':False,
				'default_invoice_link':self.id,
				'default_amount':self.residual},
				'target': 'new', }


