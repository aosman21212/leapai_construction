# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConstructionEquipment(models.Model):
    _name = 'construction.equipment'
    _description = 'Construction Equipment'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Equipment Name', required=True)
    ref = fields.Char(string='Equipment ID', copy=False, readonly=True, default='New')
    equipment_type = fields.Selection([
        ('crane', 'Crane'),
        ('excavator', 'Excavator'),
        ('bulldozer', 'Bulldozer'),
        ('concrete_mixer', 'Concrete Mixer'),
        ('generator', 'Generator'),
        ('dump_truck', 'Dump Truck'),
        ('compactor', 'Compactor'),
        ('pump', 'Pump'),
        ('scaffolding', 'Scaffolding'),
        ('other', 'Other'),
    ], string='Equipment Type')
    manufacturer = fields.Char(string='Manufacturer')
    model_no = fields.Char(string='Model No.')
    serial_no = fields.Char(string='Serial No.')
    year = fields.Integer(string='Year')
    project_id = fields.Many2one('construction.project', string='Current Project')
    status = fields.Selection([
        ('available', 'Available'),
        ('deployed', 'Deployed'),
        ('under_maintenance', 'Under Maintenance'),
        ('out_of_service', 'Out of Service'),
    ], string='Status', default='available', tracking=True)
    last_maintenance_date = fields.Date(string='Last Maintenance Date')
    next_maintenance_date = fields.Date(string='Next Maintenance Date')
    daily_rate = fields.Monetary(string='Daily Rate', currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    notes = fields.Text(string='Notes')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'New') == 'New':
                vals['ref'] = self.env['ir.sequence'].next_by_code('construction.equipment') or 'New'
        return super().create(vals_list)


class ConstructionEquipmentMaintenance(models.Model):
    _name = 'construction.equipment.maintenance'
    _description = 'Equipment Maintenance'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Maintenance Reference', copy=False, readonly=True, default='New')
    equipment_id = fields.Many2one('construction.equipment', string='Equipment', tracking=True)
    project_id = fields.Many2one('construction.project', string='Project')
    maintenance_type = fields.Selection([
        ('preventive', 'Preventive'),
        ('corrective', 'Corrective'),
        ('emergency', 'Emergency'),
    ], string='Maintenance Type')
    date_reported = fields.Date(string='Date Reported', default=fields.Date.today)
    date_completed = fields.Date(string='Date Completed')
    reported_by = fields.Many2one('res.users', string='Reported By',
                                  default=lambda self: self.env.user)
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    description = fields.Text(string='Description')
    resolution = fields.Text(string='Resolution')
    cost = fields.Monetary(string='Cost', currency_field='currency_id')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.equipment.maintenance') or 'New'
        return super().create(vals_list)
