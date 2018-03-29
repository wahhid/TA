from openerp.osv import fields, osv
import logging
import string
import random


_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [    
    ('open','Open'),
    ('active','Active'),    
    ('done','Closed'),
]

class im_trans(osv.osv):
    _name = "im.trans"
    _description = "Incident Management - Transaction"
    
    def get_trans(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        return self.browse(cr, uid, trans_id, context=context)
    
    def trans_close(self, cr, uid, ids, context=None):
        values = {}
        values.update({'state': 'done'})
        self.write(cr, uid, ids, values, context=context)
            
    def close(self, cr, uid, ids, values, context=None):
        return super(im_trans,self).write(cr, uid, ids, values, context=context)
                
    def trans_print(self, cr, uid, ids, context=None):
        _logger.info("Print Receipt for ID : " + str(ids))        
        id = ids[0]   
        config = self.pool.get('im.config').get_config(cr, uid, context=context)
        serverUrl = 'http://' + config.report_server + ':' + config.report_server_port +'/jasperserver'
        j_username = 'imuser'
        j_password = 'imuser'
        ParentFolderUri = '/Incident_Management'
        reportUnit = '/Incident_Management/trans_detail'
        url = serverUrl + '/flow.html?_flowId=viewReportFlow&standAlone=true&_flowId=viewReportFlow&ParentFolderUri=' + ParentFolderUri + '&reportUnit=' + reportUnit + '&ID=' +  str(id) + '&decorate=no&j_username=' + j_username + '&j_password=' + j_password + '&output=pdf'
        return {
            'type':'ir.actions.act_url',
            'url': url,
            'nodestroy': True,
            'target': 'new' 
        }        
        
    def _id_generator(self,cr,uid,context=None):
        size = 10
        chars= string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))
    
    _columns = {
        'trans_number': fields.char("Trans #", size=20, readonly=True),
        'trans_date_time': fields.datetime("Date and Time of Incident", required=True),                    
        'name': fields.char('Description', size=100, required=True),
        'location': fields.char('Location', size=100, required=True),
        'category_id': fields.many2one('im.category','Category'),
        'priority_id': fields.many2one('im.priority','Priority'),
        'is_claimed': fields.boolean('Claimed'),
        'trans_detail_ids': fields.one2many("im.trans.detail","trans_id","Details"),
        'state' : fields.selection(AVAILABLE_STATES, "State"),                                    
    }
    
    _defaults =  {
        'state': lambda *a: 'open',
    }
    
    def create(self, cr, uid ,values, context=None):
        trans_number = self._id_generator(cr, uid, context=context)
        values.update({'trans_number': trans_number})
        result = super(im_trans,self).create(cr, uid, values, context=context)
        return result
   
    def write(self, cr, uid, ids, values, context=None):
        trans = self.get_trans(cr, uid, ids, context=context)            
        
        if trans.state == 'done':
            raise osv.except_osv(_('Warning'),_('Transaction Already Closed.'))
        
        if 'state' in values.keys():
            if values.get('state') == 'done':
                return self.close(cr, uid, ids, values, context=context)
                
            
        return super(im_trans,self).write(cr, uid, ids, values, context=context)
         
        
        
im_trans()

class im_trans_detail(osv.osv):
    _name = "im.trans.detail"
    _description = "Incident Management - Transaction Detail"
    _columns = {
        'trans_id': fields.many2one("im.trans","Trans ID"),
        'reported_by': fields.char("Reported By", size=100, required=True),
        'witnessed_by': fields.char("Witnessed By", size=100, required=True),
        'id_number': fields.char("ID Number", size=20, required=True),
        'mobile_phone': fields.char("Telephone (Cellular)", size=20, required=True),
        'address': fields.char("Home Address", size=200),
        'company_name': fields.char("Company's Name", size=100),
        'chro_file': fields.binary("Attachment"),
        'trans_detail_chro_ids': fields.one2many("im.trans.detail.chro","trans_detail_id","Chronologies"),            
    }
    
im_trans_detail()

class im_trans_detail_chro(osv.osv):
    _name = "im.trans.detail.chro"
    _description = "Incident Management - Transaction Detail Chronology"
    _columns = {
        'trans_detail_id': fields.many2one("im.trans.detail","Trans Detail ID"),
        'chro_date_time': fields.datetime("Date and Time", required=True),
        'description': fields.text("Description", required=True),
    }
    
im_trans_detail_chro()