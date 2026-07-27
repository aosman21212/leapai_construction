# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConstructionRFI(models.Model):
    _name = 'construction.rfi'
    _description = 'Request for Information'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='RFI Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    subject = fields.Char(string='Subject', required=True, tracking=True)
    description = fields.Html(string='Description')
    requested_by = fields.Many2one('res.users', string='Requested By',
                                   default=lambda self: self.env.user)
    assigned_to = fields.Many2one('res.users', string='Assigned To', tracking=True)
    date_requested = fields.Date(string='Date Requested', default=fields.Date.today)
    date_required = fields.Date(string='Date Required')
    date_responded = fields.Date(string='Date Responded')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('responded', 'Responded'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High'),
        ('2', 'Urgent'),
    ], string='Priority', default='0')
    response = fields.Html(string='Response')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.rfi') or 'New'
        return super().create(vals_list)


class ConstructionDailyLogManpower(models.Model):
    _name = 'construction.daily.log.manpower'
    _description = 'Daily Log Manpower'

    log_id = fields.Many2one('construction.daily.log', string='Daily Log', ondelete='cascade')
    trade = fields.Char(string='Trade')
    contractor = fields.Char(string='Contractor')
    count = fields.Integer(string='Count')
    hours = fields.Float(string='Hours')


class ConstructionDailyLogEquipment(models.Model):
    _name = 'construction.daily.log.equipment'
    _description = 'Daily Log Equipment'

    log_id = fields.Many2one('construction.daily.log', string='Daily Log', ondelete='cascade')
    equipment_name = fields.Char(string='Equipment Name')
    type = fields.Char(string='Type')
    count = fields.Integer(string='Count')
    hours = fields.Float(string='Hours')


class ConstructionDailyLog(models.Model):
    _name = 'construction.daily.log'
    _description = 'Daily Site Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(string='Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    weather = fields.Selection([
        ('sunny', 'Sunny'),
        ('partly_cloudy', 'Partly Cloudy'),
        ('cloudy', 'Cloudy'),
        ('rainy', 'Rainy'),
        ('stormy', 'Stormy'),
        ('foggy', 'Foggy'),
    ], string='Weather')
    temperature = fields.Float(string='Temperature (°C)')
    prepared_by = fields.Many2one('res.users', string='Prepared By',
                                   default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
    ], string='Status', default='draft', tracking=True)
    activities_summary = fields.Text(string='Activities Summary')
    safety_remarks = fields.Text(string='Safety Remarks')
    manpower_ids = fields.One2many('construction.daily.log.manpower', 'log_id', string='Manpower')
    equipment_ids = fields.One2many('construction.daily.log.equipment', 'log_id', string='Equipment')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.daily.log') or 'New'
        return super().create(vals_list)


class ConstructionNCR(models.Model):
    _name = 'construction.ncr'
    _description = 'Non-Conformance Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='NCR Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    subject = fields.Char(string='Subject', required=True, tracking=True)
    description = fields.Html(string='Description')
    raised_by = fields.Many2one('res.users', string='Raised By',
                                default=lambda self: self.env.user)
    assigned_to = fields.Many2one('res.users', string='Assigned To', tracking=True)
    date_raised = fields.Date(string='Date Raised', default=fields.Date.today)
    date_due = fields.Date(string='Date Due')
    date_closed = fields.Date(string='Date Closed')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ], string='Status', default='draft', tracking=True)
    severity = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ], string='Severity', tracking=True)
    root_cause = fields.Text(string='Root Cause')
    corrective_action = fields.Text(string='Corrective Action')
    preventive_action = fields.Text(string='Preventive Action')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.ncr') or 'New'
        return super().create(vals_list)


class ConstructionTransmittalLine(models.Model):
    _name = 'construction.transmittal.line'
    _description = 'Transmittal Line'

    transmittal_id = fields.Many2one('construction.transmittal', string='Transmittal', ondelete='cascade')
    document_ref = fields.Char(string='Document Ref')
    description = fields.Char(string='Description')
    revision = fields.Char(string='Revision')
    copies = fields.Integer(string='Copies')
    document_type = fields.Char(string='Document Type')


class ConstructionTransmittal(models.Model):
    _name = 'construction.transmittal'
    _description = 'Document Transmittal'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Transmittal Ref', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    transmittal_date = fields.Date(string='Transmittal Date', default=fields.Date.today)
    to_company = fields.Char(string='To Company')
    to_contact = fields.Char(string='To Contact')
    from_user_id = fields.Many2one('res.users', string='From',
                                   default=lambda self: self.env.user)
    subject = fields.Char(string='Subject')
    purpose = fields.Selection([
        ('for_approval', 'For Approval'),
        ('for_review', 'For Review'),
        ('for_information', 'For Information'),
        ('for_record', 'For Record'),
    ], string='Purpose')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('acknowledged', 'Acknowledged'),
    ], string='Status', default='draft', tracking=True)
    line_ids = fields.One2many('construction.transmittal.line', 'transmittal_id', string='Documents')
    remarks = fields.Text(string='Remarks')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.transmittal') or 'New'
        return super().create(vals_list)


class ConstructionShopDrawing(models.Model):
    _name = 'construction.shop.drawing'
    _description = 'Shop Drawing'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    drawing_number = fields.Char(string='Drawing Number')
    title = fields.Char(string='Title', required=True)
    revision = fields.Char(string='Revision')
    discipline = fields.Selection([
        ('architectural', 'Architectural'),
        ('structural', 'Structural'),
        ('mechanical', 'Mechanical'),
        ('electrical', 'Electrical'),
        ('plumbing', 'Plumbing'),
        ('civil', 'Civil'),
    ], string='Discipline')
    submitted_date = fields.Date(string='Submitted Date')
    review_date = fields.Date(string='Review Date')
    status = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('approved_as_noted', 'Approved As Noted'),
        ('rejected', 'Rejected'),
        ('resubmit', 'Resubmit'),
    ], string='Status', default='draft', tracking=True)
    reviewer_id = fields.Many2one('res.users', string='Reviewer')
    comments = fields.Text(string='Comments')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.shop.drawing') or 'New'
        return super().create(vals_list)
