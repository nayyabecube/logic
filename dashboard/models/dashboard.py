from odoo import models, fields, api
import datetime



class Dashboard(models.Model):
    _name = 'dashboard.dashboard'
    
    def has_active(self,model):
        for field in model.field_id:
            if field.name=='active':
                return True
        return False
    def _compute_field_list(self):
        dashboard=self.env['dashboard.settings'].search([],limit=1,order='id desc')
        lists = dashboard.line_ids
        last_slices_list=[]
        for list in lists:
            if list.display:
                action = self.env['ir.actions.act_window'].search([('res_model','=',list.model_id.model),('view_type','=','form')],limit=1)
                requete_action="Select id as id from "+list.model_id.model.replace('.','_') 
                if list.type=='money':  
                    requete="SELECT sum("+list.field_id.name+") as field FROM "+list.model_id.model.replace('.','_')
                else:
                    requete="SELECT count("+list.field_id.name+") as field FROM "+list.model_id.model.replace('.','_')
                
                if self.has_active(list.model_id) and list.filter: 
                    requete+=" Where active=true And "+list.filter
                    requete_action+=" Where active=true And "+list.filter
                elif self.has_active(list.model_id):
                    requete+=" Where active=true "
                    requete_action+=" Where active=true "
                elif list.filter:
                    requete+=" Where "+list.filter
                    requete_action+=" Where "+list.filter
                    
                
                print '----------------------------requete',requete
                self.env.cr.execute(requete.replace('"',"'"))
                result = self.env.cr.dictfetchall()[0]
                field=result['field']
                self.env.cr.execute(requete_action.replace('"',"'"))
                result_ids = self.env.cr.dictfetchall()
                res_ids=[]
                for res in result_ids:
                    res_ids.append(res['id'])
                last_slices_list.append([field,list.name or list.field_id.field_description,list.color,list.icon,action.id,res_ids])
        return last_slices_list
    
        
    def _get_default_chart(self):
        chart_list=[]
        dashboard=self.env['dashboard.settings'].search([],limit=1,order='id desc')
        chart_ids=self.env['dashboard.settings.chart'].search([('dashboard_id','=',dashboard.id)],order='sequence')
        for list in chart_ids:
            if list.display :
                if list.display_type=='area':
                    chart_list.append([list.id,list.name,1])
                else:
                    chart_list.append([list.id,list.name,2])
        return chart_list
    
    
    name = fields.Char('Name')
    company_id = fields.Many2one('res.company', string='Company', required=True, readonly=True,
                                 default=lambda self: self.env.user.company_id)
    currency_id = fields.Many2one('res.currency', related='company_id.currency_id', store=True, string="Currency")
    field_list = fields.Selection('_compute_field_list',string='Slices names')
    chart_list=fields.Selection('_get_default_chart',string='Charts')
    
    @api.multi
    def action_setting(self):
        
        action = self.env.ref('dashboard.action_dashboard_config').read()[0]

        setting = self.env['dashboard.settings'].search([],limit=1,order='id desc').id
        action['views'] = [(self.env.ref('dashboard.dashboard_config_settings').id, 'form')]
        action['res_id'] = setting
        return action
    
    
    
    @api.multi
    def view_details(self):
        action = self.env['ir.actions.act_window'].search([('id','=',self.env.context['action_id'])],limit=1)
        result = {
            'name': action.name,
            'help': action.help,
            'type': action.type,
            'view_mode': 'tree',
            'target': action.target,
            'domain':[('id','in',self.env.context['active_ids'])],
            'context': {},
            'res_model': action.res_model,
        }
        return result