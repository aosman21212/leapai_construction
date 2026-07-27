# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConstructionEstimateLine(models.Model):
    _name = 'construction.estimate.line'
    _description = 'Estimate Line'

    estimate_id = fields.Many2one('construction.estimate', string='Estimate', ondelete='cascade')
    currency_id = fields.Many2one(related='estimate_id.currency_id', store=True)
    description = fields.Char(string='Description', required=True)
    uom = fields.Char(string='Unit of Measure')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_price = fields.Monetary(string='Unit Price', currency_field='currency_id')
    amount = fields.Monetary(string='Amount', compute='_compute_amount', store=True,
                             currency_field='currency_id')

    @api.depends('quantity', 'unit_price')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.quantity * rec.unit_price


class ConstructionEstimate(models.Model):
    _name = 'construction.estimate'
    _description = 'Cost Estimate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Estimate Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    client_id = fields.Many2one('res.partner', string='Client')
    date = fields.Date(string='Date', default=fields.Date.today)
    validity_date = fields.Date(string='Valid Until')
    prepared_by = fields.Many2one('res.users', string='Prepared By',
                                  default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    line_ids = fields.One2many('construction.estimate.line', 'estimate_id', string='Lines')
    subtotal = fields.Monetary(string='Subtotal', compute='_compute_subtotal', store=True,
                               currency_field='currency_id')
    notes = fields.Html(string='Notes')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    @api.depends('line_ids.amount')
    def _compute_subtotal(self):
        for rec in self:
            rec.subtotal = sum(rec.line_ids.mapped('amount'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.estimate') or 'New'
        return super().create(vals_list)


class ConstructionBudgetLine(models.Model):
    _name = 'construction.budget.line'
    _description = 'Budget Line'

    budget_id = fields.Many2one('construction.budget', string='Budget', ondelete='cascade')
    currency_id = fields.Many2one(related='budget_id.currency_id', store=True)
    category = fields.Selection([
        ('labour', 'Labour'),
        ('material', 'Material'),
        ('equipment', 'Equipment'),
        ('subcontract', 'Subcontract'),
        ('overhead', 'Overhead'),
        ('contingency', 'Contingency'),
    ], string='Category')
    description = fields.Char(string='Description')
    uom = fields.Char(string='Unit of Measure')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit_cost = fields.Monetary(string='Unit Cost', currency_field='currency_id')
    budgeted_amount = fields.Monetary(string='Budgeted Amount', compute='_compute_budgeted',
                                      store=True, currency_field='currency_id')
    actual_amount = fields.Monetary(string='Actual Amount', currency_field='currency_id')
    variance = fields.Monetary(string='Variance', compute='_compute_variance', store=True,
                               currency_field='currency_id')

    @api.depends('quantity', 'unit_cost')
    def _compute_budgeted(self):
        for rec in self:
            rec.budgeted_amount = rec.quantity * rec.unit_cost

    @api.depends('budgeted_amount', 'actual_amount')
    def _compute_variance(self):
        for rec in self:
            rec.variance = rec.budgeted_amount - rec.actual_amount


class ConstructionBudget(models.Model):
    _name = 'construction.budget'
    _description = 'Project Budget'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Budget Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', required=True, tracking=True)
    budget_type = fields.Selection([
        ('initial', 'Initial'),
        ('revised', 'Revised'),
        ('final', 'Final'),
    ], string='Budget Type', default='initial')
    approved_by = fields.Many2one('res.users', string='Approved By')
    approved_date = fields.Date(string='Approved Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    line_ids = fields.One2many('construction.budget.line', 'budget_id', string='Lines')
    total_budgeted = fields.Monetary(string='Total Budgeted', compute='_compute_totals', store=True,
                                     currency_field='currency_id')
    total_actual = fields.Monetary(string='Total Actual', compute='_compute_totals', store=True,
                                   currency_field='currency_id')
    total_variance = fields.Monetary(string='Total Variance', compute='_compute_totals', store=True,
                                     currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    @api.depends('line_ids.budgeted_amount', 'line_ids.actual_amount', 'line_ids.variance')
    def _compute_totals(self):
        for rec in self:
            rec.total_budgeted = sum(rec.line_ids.mapped('budgeted_amount'))
            rec.total_actual = sum(rec.line_ids.mapped('actual_amount'))
            rec.total_variance = sum(rec.line_ids.mapped('variance'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.budget') or 'New'
        return super().create(vals_list)


class ConstructionCostSheetLine(models.Model):
    _name = 'construction.cost.sheet.line'
    _description = 'Cost Sheet Line'

    cost_sheet_id = fields.Many2one('construction.cost.sheet', string='Cost Sheet', ondelete='cascade')
    currency_id = fields.Many2one(related='cost_sheet_id.currency_id', store=True)
    cost_type = fields.Selection([
        ('labour', 'Labour'),
        ('material', 'Material'),
        ('equipment', 'Equipment'),
        ('subcontract', 'Subcontract'),
        ('overhead', 'Overhead'),
    ], string='Cost Type')
    description = fields.Char(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    unit = fields.Char(string='Unit')
    unit_cost = fields.Monetary(string='Unit Cost', currency_field='currency_id')
    amount = fields.Monetary(string='Amount', compute='_compute_amount', store=True,
                             currency_field='currency_id')

    @api.depends('quantity', 'unit_cost')
    def _compute_amount(self):
        for rec in self:
            rec.amount = rec.quantity * rec.unit_cost


class ConstructionCostSheet(models.Model):
    _name = 'construction.cost.sheet'
    _description = 'Cost Sheet'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Cost Sheet Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    prepared_by = fields.Many2one('res.users', string='Prepared By',
                                  default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('approved', 'Approved'),
    ], string='Status', default='draft', tracking=True)
    line_ids = fields.One2many('construction.cost.sheet.line', 'cost_sheet_id', string='Lines')
    total_labour = fields.Monetary(string='Total Labour', compute='_compute_totals', store=True,
                                   currency_field='currency_id')
    total_material = fields.Monetary(string='Total Material', compute='_compute_totals', store=True,
                                     currency_field='currency_id')
    total_equipment = fields.Monetary(string='Total Equipment', compute='_compute_totals', store=True,
                                      currency_field='currency_id')
    total_subcontract = fields.Monetary(string='Total Subcontract', compute='_compute_totals', store=True,
                                        currency_field='currency_id')
    total_overhead = fields.Monetary(string='Total Overhead', compute='_compute_totals', store=True,
                                     currency_field='currency_id')
    grand_total = fields.Monetary(string='Grand Total', compute='_compute_totals', store=True,
                                  currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    @api.depends('line_ids.amount', 'line_ids.cost_type')
    def _compute_totals(self):
        for rec in self:
            lines = rec.line_ids
            rec.total_labour = sum(lines.filtered(lambda l: l.cost_type == 'labour').mapped('amount'))
            rec.total_material = sum(lines.filtered(lambda l: l.cost_type == 'material').mapped('amount'))
            rec.total_equipment = sum(lines.filtered(lambda l: l.cost_type == 'equipment').mapped('amount'))
            rec.total_subcontract = sum(lines.filtered(lambda l: l.cost_type == 'subcontract').mapped('amount'))
            rec.total_overhead = sum(lines.filtered(lambda l: l.cost_type == 'overhead').mapped('amount'))
            rec.grand_total = sum(lines.mapped('amount'))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.cost.sheet') or 'New'
        return super().create(vals_list)


class ConstructionChangeOrder(models.Model):
    _name = 'construction.change.order'
    _description = 'Change Order'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Change Order Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    subject = fields.Char(string='Subject', required=True, tracking=True)
    reason = fields.Text(string='Reason')
    submitted_by = fields.Many2one('res.users', string='Submitted By',
                                   default=lambda self: self.env.user)
    date_submitted = fields.Date(string='Date Submitted', default=fields.Date.today)
    approved_by = fields.Many2one('res.users', string='Approved By')
    date_approved = fields.Date(string='Date Approved')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft', tracking=True)
    cost_impact = fields.Monetary(string='Cost Impact', currency_field='currency_id')
    time_impact_days = fields.Integer(string='Time Impact (Days)')
    description = fields.Html(string='Description')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.change.order') or 'New'
        return super().create(vals_list)


class ConstructionIPC(models.Model):
    _name = 'construction.ipc'
    _description = 'Interim Payment Certificate'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='IPC Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    client_id = fields.Many2one('res.partner', string='Client')
    ipc_number = fields.Integer(string='IPC Number')
    date = fields.Date(string='Date', default=fields.Date.today)
    period_from = fields.Date(string='Period From')
    period_to = fields.Date(string='Period To')
    prepared_by = fields.Many2one('res.users', string='Prepared By',
                                  default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('certified', 'Certified'),
        ('approved', 'Approved'),
        ('paid', 'Paid'),
    ], string='Status', default='draft', tracking=True)
    contract_value = fields.Monetary(string='Contract Value', currency_field='currency_id')
    total_claimed = fields.Monetary(string='Total Claimed', currency_field='currency_id')
    retention_percentage = fields.Float(string='Retention (%)', default=10.0)
    retention_amount = fields.Monetary(string='Retention Amount', compute='_compute_retention',
                                       store=True, currency_field='currency_id')
    net_certified = fields.Monetary(string='Net Certified', compute='_compute_net_certified',
                                    store=True, currency_field='currency_id')
    currency_id = fields.Many2one(
        'res.currency', string='Currency',
        default=lambda self: self.env.company.currency_id
    )

    @api.depends('total_claimed', 'retention_percentage')
    def _compute_retention(self):
        for rec in self:
            rec.retention_amount = rec.total_claimed * (rec.retention_percentage / 100.0)

    @api.depends('total_claimed', 'retention_amount')
    def _compute_net_certified(self):
        for rec in self:
            rec.net_certified = rec.total_claimed - rec.retention_amount

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.ipc') or 'New'
        return super().create(vals_list)
