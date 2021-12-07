{
    'name': 'HR_EXTEND_MINDS',
    'description': 'HR_EXTEND_MINDS',
    'author': 'Minds Solutions',
    'depends': ['base','hr','documents','hr_holidays','hr_contract'],
    'application': True,

    'data': [
        'report/custom_internal_layout.xml',
        'views/ir_actions_act_window.xml',
        'report/report_hr_statement_document.xml',
        'report/report_hr_letter_document.xml',
        'report/job_structure_document.xml',
        'report/hiring_document.xml',
        'wizards/hr_statement_document_view.xml',
        'wizards/hr_letter_document_view.xml',
        'views/ir_ui_view.xml',
        'views/ir_ui_view2.xml',
        'views/ir_ui_menu.xml',
        'security/hr_extend_access.xml',
        'security/ir.model.access.csv',
        'data/job_degree.xml',
        'data/document_folder.xml',
        'data/hr_leave_type.xml',
    ],

    # 'qweb': [
    #     'report/custom_internal_layout.xml',
    # ],

    'installable':True,
    'application':True
}
