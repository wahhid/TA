from openerp.osv import fields, osv

class cs_category(osv.osv):
    _name = "cs.category"
    _description = "Category"
    _columns = {            
        'name': fields.char('Name', size=5, required=True),             
    }    
cs_category()

class cs_level(osv.osv):
    _name = "cs.level"
    _description = "Level"
    _columns = {            
        'name': fields.char('Level', size=100, required=True),             
    }    
cs_level()

class cs_tenant(osv.osv):
    _name = "cs.tenant"
    _description = "Tenant"
    _columns = {          
        'name': fields.char('Shop Name', size=100, required=True),
        'suite':fields.char('Level',size=10, required=True),
        'phone':fields.char('Phone',size=30),
        'information':fields.many2one('cs.category','Category'),
        'image_finding': fields.binary('Image'),
        #'profile_item_detail_ids': fields.one2many('cs.profile.item.detail','tenant_id','Details'),
        #'tenant_event_ids':fields.one2many('cs.tenant.event','tenant_id','Evens'),                 
    }    
cs_tenant()

class cs_tenant_event(osv.osv):
    _name = "cs.tenant.event"
    _description = "Tenant Event"
    _columns = {
        'tenant_id': fields.many2one('res.partner','Partner'),  
        'name': fields.char('Event Name', size=100),
        'start_date': fields.date('Start Date'),
        'end_date': fields.date('End Date'),
    }
    
cs_tenant_event()

class cs_profile_item_detail(osv.osv):
    _name = "cs.profile.item.detail"
    _description = "Profile"
    _columns ={
        #'tenant_id': fields.many2one('res.partner','Tenant'),
        'partner_id': fields.many2one('res.partner','Partner'),     
        'profile_date':fields.datetime('Date',required=True),
        'profile_history':fields.char('Profile Note History',size=100),
    }
    
    def send_mail(self, cr, uid, ids, values, context=None):
        profil_id = ids[0]
        email_obj = self.pool.get('email.template')
        search_domain = [('name', '=', 'Profile Note')] 
        template_ids= self.pool['email.template'].search(cr, uid, search_domain, context=context)[0]
        email = email_obj.browse(cr, uid, template_ids) 
        email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                'email_to': email.email_to,
                                                'subject': email.subject,
                                                'body_html': email.body_html,
                                                'email_recipients': email.email_recipients})
        email_obj.send_mail(cr, uid, template_ids, profil_id, True, context=context)
        return True
    
cs_profile_item_detail()

class cs_case(osv.osv):
    _name = "cs.case"
    _description = "Tenant_Operation_Hours"
    _columns = {
        'trans_id': fields.char('Transaction ID', size=20,readonly=True),
        'trans_date': fields.date('Case Date',size=40),
        'state':fields.selection([('late_open','Late Open'),('early_open','Early Open'),('not_trading','Not Trading')],'Status', required=True),   
        'tenant':fields.many2one('cs.tenant','Shop'),
        'level': fields.many2one('cs.level','Level', size=5, required=True),
        #'level':fields.selection([('p2','P 2'),('ground','G'),('uper_ground','U G'),('l1','L 1'),('l2','L 2'),('l3','L 3'),('l4','L 4')],'Level', required=True),
        'employee':fields.many2one('hr.employee','Customer Service',required=True),                      
    }
    
    #_defaults = {
    #    'trans_date': lambda *a: fields.datetime.now(),
    #}
    
    def create(self, cr, uid, values, context=None):
        # Create ID Auto Number
        trans_id = self.pool.get('ir.sequence').get(cr, uid, 'cs.trans.sequence')
        values.update({'trans_id':trans_id})        
        result_id =  super(cs_case,self).create(cr, uid, values, context=context)
        #Send Email
        email_obj = self.pool.get('email.template')
        search_domain = [('name', '=', 'Case Tenant Operation Hours')] 
        template_ids= self.pool['email.template'].search(cr, uid, search_domain, context=context)[0]
        email = email_obj.browse(cr, uid, template_ids) 
        email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                'email_to': email.email_to,
                                                'subject': email.subject,
                                                'body_html': email.body_html,
                                                'email_recipients': email.email_recipients})
        email_obj.send_mail(cr, uid, template_ids, result_id, True, context=context)
        return result_id       

    #def unlink(self,cr,uid,ids, context=None):
    #    raise osv.except_osv(('Warning'), ('Delete not allowed...........')) 
    #    return True
    
cs_case()


class res_partner(osv.osv):
    _name = 'res.partner'
    _inherit = 'res.partner'
    _columns = {
        'suite':fields.char('Level',size=10, required=True),
        'shop_phone':fields.char('Shop Phone',size=30),
        'tenant_category_id': fields.many2one('cs.category','Category'),        
        'profile_item_detail_ids': fields.one2many('cs.profile.item.detail','partner_id','Details'),
        'tenant_event_ids': fields.one2many('cs.tenant.event','tenant_id','Events'),            
    }
    
res_partner()


