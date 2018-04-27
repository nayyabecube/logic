# -*- coding: utf-8 -*-
{
    'name': "Logistic Invoice",

    'summary': "Logistic Invoice",

    'description': "Logistic Invoice",

    'author': "Muhammmad Awais",
    'website': "http://www.bcube.com",

    # any module necessary for this one to work correctly
    'depends': ['base', 'report', 'purchase'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
