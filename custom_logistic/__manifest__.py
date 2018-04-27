# -*- coding: utf-8 -*-
{
    'name': "Import / Export Logistic",

    'summary': """Provides The Import and Export Logistics Facility
        """,

    'description': """
       Provides The Import and Export Logistics Facility  
    """,

    'author': "Nayyab & Muhammad Awais",
    'website': "http://www.bcuube.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.8s',

    # any module necessary for this one to work correctly
    'depends': ['base','sale','account','sale_stock'],

    # always loaded
    'data': [
        'views.xml',
        'quote.xml',
        'supplier.xml',
        'report.xml',
        'security/security.xml',
        'security/ir.model.access.csv'],
    'installable': True,
    'auto_install': False

}