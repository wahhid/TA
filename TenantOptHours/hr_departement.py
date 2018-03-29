from openerp.osv import fields,osv

class hr_department(osv.osv):    
    _name = 'hr.department'
    _inherit = 'hr.department'    
    _columns = {
        'department_code': fields.char('Department Code', size=4),
        'company_id': fields.many2one('cs.company','ID Company', required=True),            
    }
    
hr_department() 