# -*- coding: utf-8 -*- 
from openerp import models, fields, api
from openerp.exceptions import Warning
from openerp.exceptions import ValidationError

class CustomerPayment(models.Model): 
	_name = 'customer.payment.bcube' 
	_rec_name = 'number'

	number = fields.Char()
	amount = fields.Float(string="Paid Amount" )
	date = fields.Date(string="Date", required = True ,default=fields.Date.context_today) 
	e_amount = fields.Float(string="Advance Amount")
	t_amount = fields.Float(string="Total Amount")
	reference = fields.Char(string="Payment Ref")
	name = fields.Char(string="Memo")
	total = fields.Float('Total Amount', compute='invoice_total' ,store=True)
	t_total = fields.Float('Total Tax', compute='tax_total' ,store=True)
	adjustable = fields.Float('Adjustable', compute='compute_adjustable')
	# period_id = fields.Many2one('account.period', string="Period")
	customer_tree  = fields.One2many( 'customer.payment.tree','customer_payment_link')
	account_id  = fields.Many2one('account.account',string="Account" , required=False)
	journal_id  = fields.Many2one('account.journal',string="Payment Method" , required=True)
	tax_link = fields.One2many('account.invoice.tax','payment_link')
	partner_id = fields.Many2one('res.partner',string="Customer / Supplier" , required=True)
	journal_entry_id = fields.Many2one('account.move',string="Journal Entry ID")
	# taxes = fields.Many2many('account.tax', string="Taxes")
	invoice_link = fields.Many2one('account.invoice', string="Invoice Link")
	receipts = fields.Boolean()
	state = fields.Selection([('draft', 'Draft'),('post', 'Posted'),('cancel', 'Cancel')], string='Status', readonly=True, copy=False, index=True, track_visibility='onchange', default='draft')
	# active_user = fields.Char(string="Active User")

	sales_man_id = fields.Many2one('res.users',"Sales Man")
	sales_man_commission = fields.Float(string = "Sales Man Commission (%)")

	@api.model
	def create(self, vals):
		new_record = super(CustomerPayment, self).create(vals)
		if new_record.receipts == True:
			new_record.number = self.env['ir.sequence'].next_by_code('customer.payment.bcube')
		else:
			new_record.number = self.env['ir.sequence'].next_by_code('supplier.payment.bcube')

		return new_record

	@api.onchange('journal_id')
	def get_account(self):
		if self.journal_id.default_debit_account_id:
			self.account_id = self.journal_id.default_debit_account_id.id


	def check_payment(self):
		if self.invoice_link:
			if self.amount > self.invoice_link.residual:
				raise ValidationError('Reconciled Amount is not Correct')



	@api.multi
	def create_journal_entry(self):
		
		self.check_payment()
		self.state = 'post'

		journal_entries = self.env['account.move']
		journal_entries_lines = self.env['account.move.line']
		if not self.journal_entry_id:	
			create_journal_entry = journal_entries.create({
					'journal_id': self.journal_id.id,
					'date':self.date,
					'id': self.journal_entry_id.id,
					'ref' : self.reference,						
					})

			self.journal_entry_id = create_journal_entry.id
			if self.receipts == True:
				create_debit = self.create_entry_lines(self.account_id.id,self.amount,0,create_journal_entry.id)
				create_credit = self.create_entry_lines(self.partner_id.property_account_receivable_id.id,0,self.amount,create_journal_entry.id)
			if self.receipts == False:
				create_debit = self.create_entry_lines(self.partner_id.property_account_payable_id.id,self.amount,0,create_journal_entry.id)
				create_credit = self.create_entry_lines(self.account_id.id,0,self.amount,create_journal_entry.id)
			self.reconcile_invoices()



	def create_entry_lines(self,account,debit,credit,entry_id):
		self.env['account.move.line'].create({
				'account_id':account,
				'partner_id':self.partner_id.id,
				'name':self.partner_id.name,
				'debit':debit,
				'credit':credit,
				'move_id':entry_id,
				})


	@api.multi
	def cancel_voucher_bcube(self):
		self.state = 'draft'
		self.journal_entry_id.unlink()
		payments = self.env['invoice.payment.tree'].search([('payment_id','=',self.id)])
		for pay in payments:
			pay.unlink()


	def reconcile_invoices(self):
		if self.receipts == True:
			if self.invoice_link:
				open_invoices = self.invoice_link
			else:
				open_invoices = self.env['account.invoice'].search([('state','=',"open"),('partner_id','=',self.partner_id.id),('type','=',"out_invoice")])
		if self.receipts == False:
			if self.invoice_link:
				open_invoices = self.invoice_link
			else:
				open_invoices = self.env['account.invoice'].search([('state','=',"open"),('partner_id','=',self.partner_id.id),('type','=',"in_invoice")])


		open_invoices = open_invoices.sorted(key=lambda r:r.date_invoice)
		amount_available = self.amount
		for inv in open_invoices:
			if amount_available > 0:
				if inv.residual >= amount_available:
					adjusted_amount = amount_available
				if inv.residual < amount_available:
					adjusted_amount = inv.residual
				amount_available = amount_available - adjusted_amount
				create_payment_lines = self.env['invoice.payment.tree'].create({
				'date':self.date,
				'amount':adjusted_amount,
				'invoice_id':inv.id,
				'payment_id':self.id,
				})

	@api.multi
	def compute_adjustable(self):
		total = 0
		payments = self.env['invoice.payment.tree'].search([('payment_id','=',self.id)])
		for pay in payments:
			total = total + pay.amount

		self.adjustable = self.amount - total


			





		
class AccountMoveRemoveValidation(models.Model):
	_inherit = "account.move"
	@api.multi
	def assert_balanced(self):
		if not self.ids:
						return True
		prec = self.env['decimal.precision'].precision_get('Account')

		self._cr.execute("""\
						SELECT      move_id
						FROM        account_move_line
						WHERE       move_id in %s
						GROUP BY    move_id
						HAVING      abs(sum(debit) - sum(credit)) > %s
						""", (tuple(self.ids), 10 ** (-max(5, prec))))
		
		return True

# class AccountMoveLineInher(models.Model):
# 	_inherit = "account.move.line"

# 	identify = fields.Char('Identify')

class taxtest(models.Model):
	_inherit = "account.tax"

	with_holding = fields.Boolean('Withholding')


	wh_type =fields.Selection([
		('income_tax', 'Income Tax'),('sales_tax','Sales Tax'),],
		 string='Withholding Type',default='income_tax')

class CustomerPaymentTree(models.Model):

	_name = 'customer.payment.tree'
	
	invoice =fields.Char('Invoice #')
	date=fields.Date('Date')
	due_amount =fields.Float('Due Amount')
	reconcile = fields.Boolean('Reconcile')
	reconciled_amount=fields.Float('Reconciled Amount')
	customer_payment_link=fields.Many2one('customer.payment.bcube')
	invoice_id=fields.Many2one('account.invoice')




	@api.multi
	@api.constrains('reconciled_amount','due_amount')
	def _check_reconciliation(self):
		if self.reconciled_amount > self.due_amount:
			raise ValidationError('Reconciled Amount is not Correct')


	@api.onchange('due_amount','reconciled_amount')
	def reconcile_tick(self):
		if self.due_amount == self.reconciled_amount:
			self.reconcile = True


class InvoicePaymentTree(models.Model):

	_name = 'invoice.payment.tree'
	
	date=fields.Date('Date')
	amount =fields.Float('Amount')
	payment_id = fields.Many2one('customer.payment.bcube', string = "Payment Id")
	
	invoice_id=fields.Many2one('account.invoice')



class Coustomer_Tax(models.Model):
	_inherit = 'account.invoice.tax'

	payment_link = fields.Many2one('customer.payment.bcube')

class ABSModification(models.Model):
	_inherit = 'account.bank.statement'
	bcube_pid 			= fields.Many2one('res.partner', 'Partner')
	randp_ids		    = fields.One2many('receipts.and.payment', 'cash_reg_id')
	receipts_amount     = fields.Float(compute='_compute_amount',string="Receipt")

	def _compute_amount(self):
		self.receipts_amount = sum(line.amount for line in self.randp_ids if line.amount > 0)

class ABSModification(models.Model):
	_name = 'receipts.and.payment'
	date 				= fields.Date('Date')
	communication	    = fields.Char('Communication')
	partner_id		    = fields.Many2one('res.partner', 'Partner')
	reference		    = fields.Char('Reference')
	amount  		    = fields.Float('Amount')
	cash_reg_id		    = fields.Many2one('account.bank.statement','Cash Reg Id', ondelete='cascade')
	cus_pay_bc_id		= fields.Many2one('customer.payment.bcube','CustomerPayment Id', ondelete='cascade')



class AccountHeadExtension(models.Model):
	_inherit = 'account.account'
	bank 	= fields.Boolean(string ='Bank & Cash')


	@api.onchange('user_type_id')
	def get_bank(self):
		if self.user_type_id.name == "Bank and Cash":
			self.bank = True
		else:
			self.bank = False
	

class InvoicePaymentExtension(models.Model):
	_inherit = 'account.invoice'
	payments 	= fields.One2many('invoice.payment.tree','invoice_id')
	
	@api.one
	@api.depends(
		'state', 'currency_id', 'invoice_line_ids.price_subtotal',
		'move_id.line_ids.amount_residual',
		'move_id.line_ids.currency_id','payments','move_id.ref')
	def _compute_residual(self):
		residual = 0.0
		residual_company_signed = 0.0
		# sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
		# for line in self.sudo().move_id.line_ids:
		# 	if line.account_id.internal_type in ('receivable', 'payable'):
		# 		residual_company_signed += line.amount_residual
		# 		if line.currency_id == self.currency_id:
		# 			residual += line.amount_residual_currency if line.currency_id else line.amount_residual
		# 		else:
		# 			from_currency = (line.currency_id and line.currency_id.with_context(date=line.date)) or line.company_id.currency_id.with_context(date=line.date)
		# 			residual += from_currency.compute(line.amount_residual, self.currency_id)
		total_payments = 0
		for lines in self.payments:
			total_payments = total_payments + lines.amount 
		self.residual_company_signed = self.amount_total - total_payments
		self.residual_signed = self.amount_total - total_payments
		self.residual = self.amount_total - total_payments
		# digits_rounding_precision = self.currency_id.rounding
		# if float_is_zero(self.residual, precision_rounding=digits_rounding_precision):
		if self.residual == 0:
			self.reconciled = True
		else:
		    self.reconciled = False


	@api.multi
	def action_invoice_open(self):
		res = super(InvoicePaymentExtension, self).action_invoice_open()
		payments = self.env['customer.payment.bcube'].search([('adjustable','>',0),('partner_id','=',self.partner_id.id)])
		for rec in payments:
			rec.reconcile_invoices()

		return res
