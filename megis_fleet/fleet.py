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

from openerp.osv import fields, osv
import time
import datetime
from openerp import tools
from openerp.osv.orm import except_orm
from openerp.tools.translate import _
from dateutil.relativedelta import relativedelta

def str_to_datetime(strdate):
    return datetime.datetime.strptime(strdate, tools.DEFAULT_SERVER_DATE_FORMAT)

class vehicle_employee_rel(osv.Model):
    _name = "vehicle.employee.rel"
    _rec_name = "vehicle_id"
    _columns = {
        'driver_id': fields.many2one('hr.employee', 'Employee', ondelete='cascade'),
        'vehicle_id': fields.many2one('fleet.vehicle', 'Voertuig', ondelete='cascade'),
        'date_start': fields.date('Date Start', required=False, help='Date when the driver received the vehicle'),
        'date_end': fields.date('Date End', required=False, help='Date when the driver returned the vehicle'),
    }

class fleet_vehicle(osv.Model):
    """ Inherits fleet.vehicle to change driver_id many2one in many2many hr_employee"""
    _inherit = 'fleet.vehicle'
    _columns = { 
        'driver_ids': fields.many2many('hr.employee','vehicle_employee_rel','vehicle_id','driver_id','Drivers', help='Drivers of the vehicle'),
        }
    
