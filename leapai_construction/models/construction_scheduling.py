# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConstructionMilestone(models.Model):
    _name = 'construction.milestone'
    _description = 'Project Milestone'
    _order = 'planned_date'

    name = fields.Char(string='Milestone Name', required=True)
    project_id = fields.Many2one('construction.project', string='Project')
    wbs_id = fields.Many2one('construction.wbs', string='WBS Item')
    planned_date = fields.Date(string='Planned Date')
    actual_date = fields.Date(string='Actual Date')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('achieved', 'Achieved'),
        ('delayed', 'Delayed'),
    ], string='Status', default='pending')
    description = fields.Text(string='Description')


class ConstructionWBS(models.Model):
    _name = 'construction.wbs'
    _description = 'Work Breakdown Structure'
    _order = 'sequence, name'

    name = fields.Char(string='WBS Name', required=True)
    code = fields.Char(string='Code')
    project_id = fields.Many2one('construction.project', string='Project', required=True)
    parent_id = fields.Many2one('construction.wbs', string='Parent WBS')
    child_ids = fields.One2many('construction.wbs', 'parent_id', string='Sub-items')
    sequence = fields.Integer(string='Sequence', default=10)
    responsible_id = fields.Many2one('res.users', string='Responsible')
    planned_start = fields.Date(string='Planned Start')
    planned_end = fields.Date(string='Planned End')
    actual_start = fields.Date(string='Actual Start')
    actual_end = fields.Date(string='Actual End')
    progress = fields.Float(string='Progress (%)', default=0.0)
    budget_amount = fields.Monetary(string='Budget Amount', currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id
    )
    milestone_ids = fields.One2many('construction.milestone', 'wbs_id', string='Milestones')
