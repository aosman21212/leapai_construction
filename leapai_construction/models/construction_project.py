# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConstructionProjectType(models.Model):
    _name = 'construction.project.type'
    _description = 'Construction Project Type'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')


class ConstructionProject(models.Model):
    _name = 'construction.project'
    _description = 'Construction Project'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'ref desc'

    name = fields.Char(string='Project Name', required=True, tracking=True)
    ref = fields.Char(string='Reference', copy=False, readonly=True, default='New')
    project_type_id = fields.Many2one('construction.project.type', string='Project Type')
    client_id = fields.Many2one('res.partner', string='Client', tracking=True)
    site_address = fields.Text(string='Site Address')
    start_date = fields.Date(string='Planned Start Date')
    end_date = fields.Date(string='Planned End Date')
    actual_start = fields.Date(string='Actual Start Date')
    actual_end = fields.Date(string='Actual End Date')
    project_manager_id = fields.Many2one('res.users', string='Project Manager', tracking=True)
    site_engineer_id = fields.Many2one('res.users', string='Site Engineer')
    team_ids = fields.Many2many('res.users', string='Project Team')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    contract_value = fields.Monetary(string='Contract Value', currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    description = fields.Html(string='Description')
    image = fields.Binary(string='Image', attachment=True)

    # Smart button counts
    rfi_count = fields.Integer(string='RFIs', compute='_compute_rfi_count')
    ncr_count = fields.Integer(string='NCRs', compute='_compute_ncr_count')
    permit_count = fields.Integer(string='Permits', compute='_compute_permit_count')
    document_count = fields.Integer(string='Documents', compute='_compute_document_count')
    budget_count = fields.Integer(string='Budgets', compute='_compute_budget_count')
    attendance_count = fields.Integer(string='Attendance', compute='_compute_attendance_count')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('ref', 'New') == 'New':
                vals['ref'] = self.env['ir.sequence'].next_by_code('construction.project') or 'New'
        return super().create(vals_list)

    def _compute_rfi_count(self):
        for rec in self:
            rec.rfi_count = self.env['construction.rfi'].search_count([('project_id', '=', rec.id)])

    def _compute_ncr_count(self):
        for rec in self:
            rec.ncr_count = self.env['construction.ncr'].search_count([('project_id', '=', rec.id)])

    def _compute_permit_count(self):
        for rec in self:
            rec.permit_count = self.env['construction.work.permit'].search_count([('project_id', '=', rec.id)])

    def _compute_document_count(self):
        for rec in self:
            rec.document_count = self.env['construction.document'].search_count([('project_id', '=', rec.id)])

    def _compute_budget_count(self):
        for rec in self:
            rec.budget_count = self.env['construction.budget'].search_count([('project_id', '=', rec.id)])

    def _compute_attendance_count(self):
        for rec in self:
            rec.attendance_count = self.env['construction.site.attendance'].search_count([('project_id', '=', rec.id)])

    def action_set_in_progress(self):
        self.write({'state': 'in_progress'})

    def action_set_on_hold(self):
        self.write({'state': 'on_hold'})

    def action_set_completed(self):
        self.write({'state': 'completed'})

    def action_set_cancelled(self):
        self.write({'state': 'cancelled'})

    def action_set_draft(self):
        self.write({'state': 'draft'})

    def action_view_rfis(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'RFIs',
            'res_model': 'construction.rfi',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_ncrs(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'NCRs',
            'res_model': 'construction.ncr',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_permits(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Work Permits',
            'res_model': 'construction.work.permit',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_documents(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Documents',
            'res_model': 'construction.document',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_budgets(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Budgets',
            'res_model': 'construction.budget',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }

    def action_view_attendance(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Site Attendance',
            'res_model': 'construction.site.attendance',
            'view_mode': 'list,form',
            'domain': [('project_id', '=', self.id)],
            'context': {'default_project_id': self.id},
        }
