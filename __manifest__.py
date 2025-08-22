# -*- coding: utf-8 -*-
{
    'name': "partner_ledger",

    'summary': "Using To can show data Of Partner Leger in wizard",

    'description': """
Long description of module's purpose
    """,

    'author': "Eng/Mohamed Elgarhy and Eng/Mohamed El-Nayed",
    'website': "https://www.yourcompany.com",

    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'accountant'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/partner_leger_lines_view.xml',
        'views/wizard_journal_view.xml',
    ],
    # 'assets': {
    #     'web.assets_backend': [
    #         'a_partner_ledger\static\src\components\partner_ledger_journal_click.js',
    #     ],
    # },
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False
}
