# -*- encoding: utf-8 -*-
{
    'name': "Row Number in tree/list view",
    'version': '10.0.0',
    'summary': 'Show row number in tree/list view.',
    'category': 'Other',
    'description': """By installing this module, user can see row number in Odoo backend tree view.""",
    'author': 'Nilesh Sheliya',
    "depends" : ['web'],
    'data': [
             'views/listview_templates.xml',
             ],
    'qweb': [
           'static/src/xml/base.xml',
            ],  
    
    'installable': True,
    'application'   : True,
    'auto_install'  : False,
}