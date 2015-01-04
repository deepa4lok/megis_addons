# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2009 EduSense BV (<http://www.edusense.nl>).
#              (C) 2011 - 2013 Therp BV (<http://therp.nl>).
#              (C) 2013 Eurogroup Consulting BV (http://www.eurogroupconsulting.nl)    
#            
#    All other contributions are (C) by their respective contributors
#
#    All Rights Reserved
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#############################################################################

from openerp.osv import orm, fields
from openerp.tools.translate import _

class payment_order_create(orm.TransientModel):
    _inherit = 'payment.order.create'

#    def extend_payment_order_domain(
#            self, cr, uid, payment_order, domain, context=None):
#        if payment_order.payment_order_type == 'payment':
#            domain += [
#                ('account_id.type', '=', 'payable'),
#                ('amount_to_pay', '>', 0)
#                ('invoice.state', '=', 'auth')
#                ]
#        return True

    def search_entries(self, cr, uid, ids, context=None):
        """
        This method taken from account_banking_payment module.
        We adapt the domain based on the invoice status (must be 'auth')
        """
        line_obj = self.pool.get('account.move.line')
        mod_obj = self.pool.get('ir.model.data')
        if context is None:
            context = {}
        data = self.read(cr, uid, ids, ['duedate'], context=context)[0]
        search_due_date = data['duedate']
        
        ### start account_banking_payment ###
        payment = self.pool.get('payment.order').browse(
            cr, uid, context['active_id'], context=context)
        # Search for move line to pay:
        domain = [
            ('move_id.state', '=', 'posted'),
            ('reconcile_id', '=', False),
            ('company_id', '=', payment.mode.company_id.id),
            ('invoice.state', '=', 'auth'),
            ]

        # apply payment term filter
        if payment.mode.payment_term_ids:
            domain += [
                ('invoice.payment_term', 'in', 
                 [term.id for term in payment.mode.payment_term_ids]
                 )
                ]
        self.extend_payment_order_domain(
            cr, uid, payment, domain, context=context)
        ### end account_direct_debit ###

        domain = domain + [
            '|', ('date_maturity', '<=', search_due_date),
            ('date_maturity', '=', False)
            ]
        line_ids = line_obj.search(cr, uid, domain, context=context)
        context.update({'line_ids': line_ids})
        model_data_ids = mod_obj.search(
            cr, uid,[
                ('model', '=', 'ir.ui.view'),
                ('name', '=', 'view_create_payment_order_lines')],
            context=context)
        resource_id = mod_obj.read(
            cr, uid, model_data_ids, fields=['res_id'],
            context=context)[0]['res_id']
        return {'name': _('Entry Lines'),
                'context': context,
                'view_type': 'form',
                'view_mode': 'form',
                'res_model': 'payment.order.create',
                'views': [(resource_id, 'form')],
                'type': 'ir.actions.act_window',
                'target': 'new',
        }
   