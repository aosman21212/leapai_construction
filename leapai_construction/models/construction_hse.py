# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConstructionPermitType(models.Model):
    _name = 'construction.permit.type'
    _description = 'Work Permit Type'
    _order = 'name'

    name = fields.Char(string='Name', required=True)
    code = fields.Char(string='Code')
    description = fields.Text(string='Description')


class ConstructionWorkPermit(models.Model):
    _name = 'construction.work.permit'
    _description = 'Work Permit'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Permit Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    permit_type_id = fields.Many2one('construction.permit.type', string='Permit Type')
    contractor_id = fields.Many2one('res.partner', string='Contractor')
    location = fields.Char(string='Location')
    work_description = fields.Text(string='Work Description')
    start_datetime = fields.Datetime(string='Start Date/Time')
    end_datetime = fields.Datetime(string='End Date/Time')
    issued_by = fields.Many2one('res.users', string='Issued By',
                                default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)
    risk_level = fields.Selection([
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ], string='Risk Level')
    safety_measures = fields.Text(string='Safety Measures')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.work.permit') or 'New'
        return super().create(vals_list)


class ConstructionRiskRegister(models.Model):
    _name = 'construction.risk.register'
    _description = 'Risk Register'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'risk_score desc'

    name = fields.Char(string='Risk Name', required=True, tracking=True)
    project_id = fields.Many2one('construction.project', string='Project')
    category = fields.Selection([
        ('safety', 'Safety'),
        ('environmental', 'Environmental'),
        ('financial', 'Financial'),
        ('technical', 'Technical'),
        ('schedule', 'Schedule'),
        ('legal', 'Legal'),
    ], string='Category')
    description = fields.Text(string='Description')
    likelihood = fields.Selection([
        ('1', '1 - Rare'),
        ('2', '2 - Unlikely'),
        ('3', '3 - Possible'),
        ('4', '4 - Likely'),
        ('5', '5 - Almost Certain'),
    ], string='Likelihood')
    severity = fields.Selection([
        ('1', '1 - Negligible'),
        ('2', '2 - Minor'),
        ('3', '3 - Moderate'),
        ('4', '4 - Major'),
        ('5', '5 - Catastrophic'),
    ], string='Severity')
    risk_score = fields.Integer(string='Risk Score', compute='_compute_risk_score', store=True)
    risk_level = fields.Char(string='Risk Level', compute='_compute_risk_level', store=True)
    mitigation_plan = fields.Text(string='Mitigation Plan')
    responsible_id = fields.Many2one('res.users', string='Responsible')
    status = fields.Selection([
        ('open', 'Open'),
        ('mitigated', 'Mitigated'),
        ('closed', 'Closed'),
    ], string='Status', default='open', tracking=True)
    review_date = fields.Date(string='Review Date')

    @api.depends('likelihood', 'severity')
    def _compute_risk_score(self):
        for rec in self:
            if rec.likelihood and rec.severity:
                rec.risk_score = int(rec.likelihood) * int(rec.severity)
            else:
                rec.risk_score = 0

    @api.depends('risk_score')
    def _compute_risk_level(self):
        for rec in self:
            score = rec.risk_score
            if score <= 4:
                rec.risk_level = 'Low'
            elif score <= 9:
                rec.risk_level = 'Medium'
            elif score <= 19:
                rec.risk_level = 'High'
            else:
                rec.risk_level = 'Critical'


class ConstructionToolboxTalk(models.Model):
    _name = 'construction.toolbox.talk'
    _description = 'Toolbox Talk'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'date desc'

    name = fields.Char(string='Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    topic = fields.Char(string='Topic', required=True)
    date = fields.Date(string='Date', default=fields.Date.today)
    conducted_by = fields.Many2one('res.users', string='Conducted By',
                                   default=lambda self: self.env.user)
    location = fields.Char(string='Location')
    content = fields.Html(string='Content')
    attendee_ids = fields.Many2many('hr.employee', string='Attendees')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('conducted', 'Conducted'),
        ('signed_off', 'Signed Off'),
    ], string='Status', default='draft', tracking=True)
    attendee_count = fields.Integer(string='Attendee Count', compute='_compute_attendee_count', store=True)

    @api.depends('attendee_ids')
    def _compute_attendee_count(self):
        for rec in self:
            rec.attendee_count = len(rec.attendee_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.toolbox.talk') or 'New'
        return super().create(vals_list)


class ConstructionSafetyObservation(models.Model):
    _name = 'construction.safety.observation'
    _description = 'Safety Observation'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    observation_type = fields.Selection([
        ('unsafe_act', 'Unsafe Act'),
        ('unsafe_condition', 'Unsafe Condition'),
        ('near_miss', 'Near Miss'),
        ('positive', 'Positive Observation'),
    ], string='Observation Type')
    description = fields.Text(string='Description')
    location = fields.Char(string='Location')
    observed_by = fields.Many2one('res.users', string='Observed By',
                                  default=lambda self: self.env.user)
    date_observed = fields.Date(string='Date Observed', default=fields.Date.today)
    assigned_to = fields.Many2one('res.users', string='Assigned To')
    date_due = fields.Date(string='Date Due')
    state = fields.Selection([
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('closed', 'Closed'),
    ], string='Status', default='open', tracking=True)
    corrective_action = fields.Text(string='Corrective Action')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.safety.observation') or 'New'
        return super().create(vals_list)


class ConstructionSiteAttendance(models.Model):
    _name = 'construction.site.attendance'
    _description = 'Site Attendance'
    _order = 'date desc'

    name = fields.Char(string='Reference', compute='_compute_name', store=True)
    project_id = fields.Many2one('construction.project', string='Project')
    date = fields.Date(string='Date', default=fields.Date.today)
    employee_id = fields.Many2one('hr.employee', string='Employee')
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')
    hours_worked = fields.Float(string='Hours Worked', compute='_compute_hours_worked', store=True)
    trade = fields.Char(string='Trade')
    contractor = fields.Char(string='Contractor')

    @api.depends('employee_id', 'date')
    def _compute_name(self):
        for rec in self:
            emp = rec.employee_id.name or ''
            date = str(rec.date) if rec.date else ''
            rec.name = f'{emp} - {date}' if emp or date else 'New'

    @api.depends('check_in', 'check_out')
    def _compute_hours_worked(self):
        for rec in self:
            if rec.check_in and rec.check_out:
                delta = rec.check_out - rec.check_in
                rec.hours_worked = delta.seconds / 3600.0 + delta.days * 24
            else:
                rec.hours_worked = 0.0


class ConstructionVisitorLog(models.Model):
    _name = 'construction.visitor.log'
    _description = 'Visitor Log'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Reference', copy=False, readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project')
    visitor_name = fields.Char(string='Visitor Name', required=True)
    company = fields.Char(string='Company')
    purpose = fields.Char(string='Purpose')
    host_id = fields.Many2one('res.users', string='Host')
    check_in = fields.Datetime(string='Check In')
    check_out = fields.Datetime(string='Check Out')
    id_type = fields.Selection([
        ('national_id', 'National ID'),
        ('passport', 'Passport'),
        ('driving_license', 'Driving License'),
    ], string='ID Type')
    id_number = fields.Char(string='ID Number')
    badge_number = fields.Char(string='Badge Number')
    state = fields.Selection([
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
    ], string='Status', default='checked_in', tracking=True)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.visitor.log') or 'New'
        return super().create(vals_list)
