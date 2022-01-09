# -*- coding: utf-8 -*-
{
    'name': "hr_egypt_payroll_minds",

    'summary': """
        Egypt Payroll """,

    'description': """
        Long description of module's purpose
    """,

    'author': "Minds Solutions",
    'website': "http://www.mindseg.com",

    'category': 'hr',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base','hr_extend_minds','hr_payroll'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'data/payroll_config.xml',
        'views/pivot.xml',
        'views/views.xml',
        'views/ir.ui.menu.xml',
        'views/templates.xml',
        'views/hr_contract_view.xml',
        'views/payroll_employee_pages.xml',
        'views/salary_menu_items.xml',
        'views/hr_payslip.xml',
        'security/payroll_extend_access.xml',
        'security/ir.model.access.csv',
        'data/allowance.xml',
        'data/deduction.xml',
        'data/subscription.xml',
        'data/data.xml',
        'data/salary_degree.xml',
        'data/employee_group.xml',
        'data/employee_group_child.xml',
        'data/job_incentive.xml',
        'data/extra_incentive.xml',
        'report/report_payslip_templates.xml',
        'views/search.xml',
        
    ],
    # only loaded in demonstration mode
    # 'demo': [
    #     'demo/demo.xml',
    # ],
    'installable': True,
    'auto_install': False,
    'application': True,
}