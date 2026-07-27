# -*- coding: utf-8 -*-
from odoo import api, fields, models


class ConstructionDocument(models.Model):
    _name = 'construction.document'
    _description = 'Construction Document'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name desc'

    name = fields.Char(string='Document Reference', required=True, copy=False,
                       readonly=True, default='New')
    project_id = fields.Many2one('construction.project', string='Project', tracking=True)
    document_type = fields.Selection([
        ('drawing', 'Drawing'),
        ('specification', 'Specification'),
        ('report', 'Report'),
        ('contract', 'Contract'),
        ('correspondence', 'Correspondence'),
        ('other', 'Other'),
    ], string='Document Type')
    revision = fields.Char(string='Revision', default='A')
    prepared_by = fields.Many2one('res.users', string='Prepared By',
                                  default=lambda self: self.env.user)
    reviewed_by = fields.Many2one('res.users', string='Reviewed By')
    approved_by = fields.Many2one('res.users', string='Approved By')
    date_prepared = fields.Date(string='Date Prepared', default=fields.Date.today)
    date_expires = fields.Date(string='Expiry Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('under_review', 'Under Review'),
        ('approved', 'Approved'),
        ('superseded', 'Superseded'),
    ], string='Status', default='draft', tracking=True)
    description = fields.Text(string='Description')
    attachment_ids = fields.Many2many(
        'ir.attachment', 'construction_document_attachment_rel',
        'document_id', 'attachment_id',
        string='Attachments'
    )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('construction.document') or 'New'
        return super().create(vals_list)
