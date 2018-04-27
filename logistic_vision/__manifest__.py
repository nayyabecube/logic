# -*- coding: utf-8 -*-
{
    'name': "Logistic_Invoice",

    'summary': "Logistic_Invoice",

    'description': "Logistic_Invoice",

    'author': "Muhammmad Awais",
    'website': "http://www.bcube.pk",

    # any module necessary for this one to work correctly
    'depends': ['base','account'],
    # always loaded
    'data': [
        'template.xml',
        'views/module_report.xml',
    ],
    'css': ['static/src/css/report.css'],
}
