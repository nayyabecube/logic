# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import datetime


class AccountMoveLineInher(models.Model):
    _inherit = 'res.partner'

    route_id = fields.One2many('route.transport', 'route_trans')
    bl_id = fields.One2many('bl.tree', 'bl_tree')
    cont_id = fields.One2many('bl.tree', 'bl_tree')
    charge_id = fields.One2many('charg.vender', 'charge_tree')
    brooker = fields.Boolean(string="Broker")
    bl_num = fields.Boolean(string="B/l Number")
    checks = fields.Boolean(string="check")
    cont_num = fields.Boolean(string="Cont Wise")
    bill_type = fields.Selection([('B/L Number', 'B/L Number'), ('Container Wise', 'Container Wise')],
                                 string="Billing Type")
    types = fields.Selection(
        [('trnas', 'Transporter'), ('freight_fwd', 'Freight Forwarder'), ('ship_line', 'Shipping Line'),
         ('storage', 'Storage')], string="Type")
    by_customer = new_field_ids = fields.One2many(comodel_name="by.customer", inverse_name="main_class",
                                                  string="By Customer", required=False, )

    @api.onchange('bill_type')
    def get_bl(self):
        if self.bill_type == "B/L Number":
            self.bl_num = True
            self.cont_num = False

    @api.onchange('bill_type')
    def get_cont(self):
        if self.bill_type == "Container Wise":
            self.cont_num = True
            self.bl_num = False

    @api.onchange('types')
    def get_trans(self):
        if self.types == "freight_fwd":
            self.checks = True
        else:
            self.checks = False


class ByCustomer(models.Model):
    _name = 'by.customer'
    _rec_name = 'name'
    _description = 'By Customers of Customer'

    name = fields.Char()
    customer = fields.Many2one(comodel_name="res.partner", string="Customer", required=False, )

    main_class = new_field_id = fields.Many2one(comodel_name="res.customer", string="By Customer", required=False, )

    @api.onchange('name')
    def onchange_name(self):
        if self.name:
            self.customer = self.main_class.id


class BlnumberTree(models.Model):
    _name = 'bl.tree'

    charges_serv = fields.Float(string="Service Charges")
    charges_type = fields.Many2one('serv.types', string="Service Type")
    by_customer = fields.Many2one('by.customer', string="By Customer")

    bl_tree = fields.Many2one('res.partner')


class BlnumberTree(models.Model):
    _name = 'bl.tree'

    charges_serv = fields.Float(string="Service Charges")
    charges_type = fields.Many2one('serv.types', string="Service Type")
    by_customer = fields.Many2one('by.customer', string="By Customer")
    service_type = fields.Selection([('import', 'Import'), ('export', 'Export')], string="Service Name")
    cont_type = fields.Selection([('20 ft', '20 ft'), ('40 ft', '40 ft')], string="Container Size")

    bl_tree = fields.Many2one('res.partner')


class transport_info(models.Model):
    _name = 'route.transport'
    # _rec_name   = 'company_name'

    form = fields.Many2one('from.qoute', string="From")
    to = fields.Many2one('to.quote', string="To")
    fleet_type = fields.Many2one('fleet', string="Fleet Type")
    service_type = fields.Selection([('import', 'Import'), ('export', 'Export')], string="Service Name")
    trans_charges = fields.Float(string="Charges")
    by_customer = fields.Many2one('by.customer', string="By Customer")


    route_trans = fields.Many2one('res.partner')


class ChargesVender(models.Model):
    _name = 'charg.vender'

    charges_vend = fields.Char(string="Charges")
    contain_type = fields.Selection([('20 ft', '20 ft'), ('40 ft', '40 ft')], string="Container Type")

    charge_tree = fields.Many2one('res.partner')


class From(models.Model):
    _name = 'from.qoute'

    name = fields.Char('name')


class To(models.Model):
    _name = 'to.quote'

    name = fields.Char('name')


class Fleet(models.Model):
    _name = 'fleet'

    name = fields.Char('Fleet Type')


class AccountExtend(models.Model):
    _inherit = 'account.invoice'

    billng_type = fields.Char(string="Billing Type")
    by_customer = fields.Many2one('by.customer', string="By Customer")
    customer_site = fields.Many2one('import.site', string="Site")
    bill_num = fields.Char(string="B/L Number")
    acount_link = fields.Many2one('freight.forward', string='link')
    our_job = fields.Char(string="Our Job No", required=False, )
    sr_no = fields.Char(string="Sr No", required=False, )
    customer_ref = fields.Char(string="Customer Ref", required=False, )
    custom_dec = fields.Char(string="Custom Dec", required=False, )
    bayan_no = fields.Char(string="Bayan No", required=False, )
    final_date = fields.Date(string="Final Date", required=False, )

    @api.multi
    def reg_pay(self):
        return {'name': 'Receipt',
                'domain': [],
                'res_model': 'customer.payment.bcube',
                'type': 'ir.actions.act_window',
                'view_mode': 'form', 'view_type': 'form',
                'context': {
                'default_partner_id':self.partner_id.id,
                'default_receipts':True,
                'default_invoice_link':self.id,
                'default_amount':self.residual},
                'target': 'new', }



class AccountTreeExtend(models.Model):
    _inherit = 'account.invoice.line'

    crt_no = fields.Char(string="Container No.")
    service_type = fields.Char(string="Service Name")


class Charges_service(models.Model):
    _name = 'serv.types'

    name = fields.Char(string="Service Type")


class FreightForwarding(models.Model):
    _name = 'freight.forward'
    _rec_name = 'sr_no'

    customer = fields.Many2one('res.partner', string="Customer", required=True)
    s_supplier = fields.Many2one('res.partner', string="Shipping Line")
    sr_no = fields.Char(string="SR No", readonly=True)
    book_date = fields.Date(string="Booking Date")
    eta_date = fields.Date(string="ETA Date")
    etd_date = fields.Date(string="ETD Date")
    cro = fields.Integer(string="CRO")
    cro_date = fields.Date(string="CRO Date")
    no_of_con = fields.Integer(string="No of Containers")
    form = fields.Many2one('from.qoute', string="Country of Origin")
    to = fields.Many2one('to.quote', string="Destination")
    acct_link = fields.Many2one('account.invoice', string="Invoice", readonly=True)
    implink = fields.Many2one('import.logic', string="Import Link", readonly=True)
    explink = fields.Many2one('export.logic', string="Export Link", readonly=True)
    freight = fields.Boolean(string="Freight Forwarding")
    trans = fields.Boolean(string="Transportation")
    smart = fields.Boolean(string="Smart")
    store = fields.Boolean(string="Storage")
    custm = fields.Boolean(string="Custom Clearance")
    inv_chk = fields.Boolean(string="Invoice")
    frieght_id = fields.One2many('freight.tree', 'freight_tree')
    status = fields.Many2one('import.status', string="Status")
    trans_order = fields.Many2one('sale.order', string="Transport Order")
    recharge_count = fields.Integer(string="Recharge", compute='act_show_log_recharge_trip')
    customer_site = fields.Many2one('import.site', string="Site")

    types = fields.Selection([
        ('imp', 'Import'),
        ('exp', 'Export')
    ], string="Type")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], default='draft')
    btn_stage = fields.Selection([
        ('trans', 'Trans'),
        ('custom', 'custom'),
        ('invoice', 'invoice'),
        ('done', 'done'),
    ], default='trans')

    pname = fields.Char(compute='act_show_log_recharge_trip')

    @api.one
    def act_show_log_recharge_trip(self):
        self.recharge_count = self.env['sale.order'].search_count([('trans_link', '=', self.id)])

    @api.model
    def create(self, vals):
        vals['sr_no'] = self.env['ir.sequence'].next_by_code('freight.forward')
        new_record = super(FreightForwarding, self).create(vals)

        return new_record

    @api.multi
    def done(self):
        self.state = 'done'

    @api.multi
    def create_order(self):
        self.btn_stage = 'custom'
        self.smart = True
        prev_rec = self.env['sale.order'].search([('trans_link', '=', self.id)])
        for x in prev_rec:
            if x.state == 'sale':
                x.state = 'draft'
                x.unlink()

        value = 0
        get_id = self.env['product.template'].search([])
        for x in get_id:
            if x.name == "Container":
                value = x.id

        for data in self.frieght_id:
            records = self.env['sale.order'].create({
                'partner_id': self.customer.id,
                'suppl_name': self.s_supplier.id,
                'trans_link': self.id,
                'state': 'sale',
            })

            records.order_line.create({
                'product_id': value,
                'name': 'Transport Order',
                'product_uom_qty': 1.0,
                'price_unit': 1,
                'crt_no': data.cont_no,
                'product_uom': 1,
                'order_id': records.id,
            })

    @api.multi
    def create_invoice(self):
        account = self.env['account_journal.configuration'].search([])
        self.btn_stage = 'done'
        self.inv_chk = True
        prev_rec = self.env['account.invoice'].search([('acount_link', '=', self.id)])
        prev_rec.unlink()

        records = self.env['account.invoice'].create({
            'partner_id': self.customer.id,
            'date_invoice': self.book_date,
            'type': "out_invoice",
            'journal_id':account.p_invoice_journal.id,
            'acount_link': self.id,
            'customer_site': self.customer_site.id,
        })

        self.acct_link = records.id

        for data in self.frieght_id:
            if data.frt_charg != 0:
                records.invoice_line_ids.create({
                    'name': 'Freight Charges',
                    'qunatity': 1,
                    'account_id': account.freight_invoice_account.id ,
                    'price_unit': data.frt_charg,
                    'crt_no': data.cont_no,
                    'service_type': data.cont_type,
                    'invoice_id': records.id,
                })

        for line in self.frieght_id:
            if data.str_charg != 0:
                records.invoice_line_ids.create({
                    'name': 'Storage Charges',
                    'qunatity': 1,
                    'account_id': account.storage_invoice_account.id,
                    'price_unit': line.str_charg,
                    'crt_no': line.cont_no,
                    'service_type': line.cont_type,
                    'invoice_id': records.id,
                })

        if self.types == 'imp':
            if not self.implink.acc_link:
                self.implink.acc_link = records.id
                for line in self.implink.import_serv:
                    records.invoice_line_ids.create({
                        'name': 'Custom Clearance Import Charges',
                        'quantity': 1,
                        'price_unit': line.charge_serv,
                        'account_id': account.i_custom_invoice_account.id,
                        'service_type': line.type_serv.name,
                        'invoice_id': records.id,
                    })

        if self.types == 'exp':
            if not self.explink.acc_link:
                self.explink.acc_link = records.id
                for line in self.explink.export_serv:
                    records.invoice_line_ids.create({
                        'name': 'Custom Clearance Export Charges',
                        'quantity': 1,
                        'price_unit': line.sevr_charge,
                        'account_id': account.e_custom_invoice_account.id,
                        'service_type': line.sevr_type.name,
                        'invoice_id': records.id,
                    })
                for data in self.explink.export_link:
                    records.invoice_line_ids.create({
                        'name': 'Custom Examination Export Charges',
                        'quantity': 1,
                        'price_unit': data.amt_paid,
                        'account_id': account.e_custom_exm_invoice_account.id,
                        'crt_no': data.container_no,
                        'invoice_id': records.id,
                    })

        data = self.env['sale.order'].search([('trans_link', '=', self.id)])
        for x in data:
            x.acc_link = records.id
            for y in x.order_line:
                records.invoice_line_ids.create({
                    'name': 'Transport Order Charges',
                    'quantity': 1,
                    'price_unit': y.price_unit,
                    'account_id': account.transport_invoice_account.id,
                    'crt_no': y.crt_no,
                    'invoice_id': records.id,
                })

    @api.multi
    def create_custm(self):
        self.btn_stage = 'invoice'
        if self.types == 'imp':
            prev_rec = self.env['import.logic'].search([('fri_id', '=', self.id)])
            prev_rec.unlink()

            records = self.env['import.logic'].create({
                'customer': self.customer.id,
                'fri_id': self.id,
            })

            self.implink = records.id

            for x in self.frieght_id:
                records.import_id.create({
                    'crt_no': x.cont_no,
                    'types': x.cont_type,
                    # 'trans_charge': x.str_charg,
                    # 'transporter': x.str_supp.id,
                    'crt_tree': records.id,
                })

        if self.types == 'exp':
            prev_rec = self.env['export.logic'].search([('fri_id', '=', self.id)])
            prev_rec.unlink()

            records = self.env['export.logic'].create({
                'customer': self.customer.id,
                'fri_id': self.id,
            })

            self.explink = records.id

            for x in self.frieght_id:
                records.export_id.create({
                    'crt_no': x.cont_no,
                    'types': x.cont_type,
                    # 'trans_charge': x.str_charg,
                    # 'transporter': x.str_supp.id,
                    'crt_tree': records.id,
                })


class FreightTree(models.Model):
    _name = 'freight.tree'

    cont_no = fields.Char(string="Container No")
    str_charg = fields.Float(string="Storage Charges")
    frt_charg = fields.Float(string="Freight Charges")
    str_supp = fields.Many2one('res.partner', string="Storage Supplier")
    cont_type = fields.Selection([('20 ft', '20 ft'), ('40 ft', '40 ft')], string="Container Size")

    freight_tree = fields.Many2one('freight.forward')
