from openerp.osv import fields, osv
import logging

_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [    
    ('open','Open'),
    ('active','Active'),    
    ('done','Closed'),
]

class im_category(osv.osv):
    _name = "im.category"
    _description = "Incident Management - Category"
    _columns = {        
        'name': fields.char('Name', size=20, required=True),                            
    }
        
im_category

class im_priority(osv.osv):
    _name = "im.priority"
    _description = "Incident Management - Priority"
    _columns = {        
        'name': fields.char('Name', size=20, required=True),                            
    }
        
im_category