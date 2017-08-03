# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
##############################################################################


# from openerp.osv import fields, osv
# from openerp import tools
# from openerp.tools.translate import _
#
# class account_analytic_line(osv.osv):
#     _inherit = 'account.analytic.line'
#     _description = 'Analytic Line'
#     _columns = {
#         'regel_naar_slam': fields.boolean('Regel is naar SLAM'),
#         'datum_naar_slam': fields.date('Datum regel naar SLAM', 'required=False'),
#     }
#
# account_analytic_line()
#
# class account_journal(osv.osv):
#     _inherit = 'account.journal'
#     _description = 'Journal'
#     _columns = {
#         'slam_relevant': fields.boolean('Slam Export', help='If the journal entries of theis journal should be exported to SLAM'),
#     }
#
#     _defaults = {
#         'slam_relevant': False,
#     }
#
# account_journal()


from odoo import api, fields, models, _


class AnalyticLine(models.Model):
    _inherit = 'account.analytic.line'

    regel_naar_slam = fields.Boolean('Regel is naar SLAM')
    datum_naar_slam = fields.Date('Datum regel naar SLAM', required=False)


class Journal(models.Model):
    _inherit = 'account.journal'

    slam_relevant = fields.Boolean('Slam Export', default=False, help='If the journal entries of theis journal should be exported to SLAM')

