{
    'name' : 'Incident Management System',
    'version' : '1.0',
    'author' : 'Jakc Labs',
    'category' : 'Generic Modules/Incident Management System',
    'depends' : ['base_setup','base','hr'],
    'init_xml' : [],
    'data' : [
        'security/jakc_im_security.xml',
        'security/ir.model.access.csv',
        'jakc_im_view.xml',                                                        
        'jakc_im_transaction_view.xml',
        'jakc_im_menu.xml',        
        'jakc_im_config_view.xml',
        'jakc_im_config_menu.xml',
    
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}