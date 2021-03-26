{
    'name': 'PITaaa',
    'author': 'Andryanus',
    'version': '0.1',
    'depends': [
        'project', 'project_enterprise',
        'timesheet_grid', 'base_geolocalize',
        'helpdesk_fsm', 'industry_fsm_sale'
    ],
    'data': [
        'security/ir.model.access.csv',

        'views/account_move_views.xml',
        'views/fsm_views.xml',
        'views/helpdesk_team_views.xml',
        'views/project_portal_templates.xml',
        'views/product_template_views.xml',


        'views/project_views.xml',
        'views/product_unit.xml',
        'views/product_unit_type.xml',
        'views/SJ_custom.xml',
        'views/SJ_vw_custom.xml',
        'views/stock_picking_custom.xml',
        'views/SP_custom.xml',
        'views/SP_vw_custom.xml',
        'views/PO_custom.xml',
        'views/PO_vw_custom.xml',
        'views/PURA_custom.xml',
        'views/PURA_vw_custom.xml',
        'views/INVO_custom.xml',
        'views/INVO_vw_custom.xml',
        'views/KB_custom.xml',
        'views/KB_vw_custom.xml',
        'views/BPB_custom.xml',
        'views/BPB_vw_custom.xml',
        'views/res_city_view.xml',
        'data/sequence.xml',
        'views/res_city.xml',
        'views/isd_report_menu.xml',
        'views/isd_report_lpu.xml',
        'views/report_BPB_menu.xml',
        'views/report_BPB_template.xml',
    ],
    'qweb': [

    ],
    'sequence': 1,
    'auto_install': False,
    'installable': True,
    'application': True,
    'category': 'PIT Part 1',
    'summary': 'PIT',
    'license': 'OPL-1',
    'website': 'https://www.isdigital.co.id/',
    'description': '-'
}
