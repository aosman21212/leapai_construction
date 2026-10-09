# -*- coding: utf-8 -*-
# =============================================================================
#  LeapAI Construction ERP
# -----------------------------------------------------------------------------
#  Location  : King Abdulaziz Branch Road, Riyadh, Saudi Arabia
#  Email     : sales@leapai.ai
#  Phone     : +966 53 553 3627
#  Website   : https://leapai.ai
#  Developer : Abdulkaraim Osman — Tech Manager | Backend Engineer | DevOps Engineer
#              at Bab International Corp For Specialized Services
#  LinkedIn  : https://www.linkedin.com/in/abdulkaraim-o-385b7a110/
# =============================================================================
{
    'name': 'LeapAI Construction ERP',
    'version': '19.0.1.0.0',
    'category': 'Construction',
    'summary': 'Complete Construction ERP — Projects, Site Ops, HSE, Finance, Scheduling, Documents, Equipment',
    'description': """
LeapAI Construction ERP
========================
Full-stack construction project management tailored for Saudi Arabia
and GCC contractors — from tender through handover.

Key Features
------------
• Projects — Dashboard, KPIs, regional classification, contract value tracking
• Site Operations — RFIs, Daily Logs, NCRs, Shop Drawings, Transmittals
• HSE & Safety — Work Permits, Risk Register, Toolbox Talks, Safety Observations,
  Site Attendance, Visitor Logs
• Finance — Estimates, Budgets, Cost Sheets, Change Orders, IPCs (Interim Payment Certs)
• Scheduling — WBS (Work Breakdown Structure), Milestones
• Documents — Document Register with revision control
• Plant & Equipment — Equipment fleet, Maintenance scheduling
• Saudi Compliance — SAR currency, VAT 15%, regional classification, bilingual Arabic/English

Contact
-------
Location : King Abdulaziz Branch Road, Riyadh, Saudi Arabia
Email    : sales@leapai.ai
Phone    : +966 53 553 3627
Website  : https://leapai.ai/

Developer
---------
Abdulkaraim Osman — Tech Manager | Backend Engineer | DevOps Engineer
Bab International Corp For Specialized Services
LinkedIn : https://www.linkedin.com/in/abdulkaraim-o-385b7a110/
    """,
    'author': 'leapai.ai / Abdulkaraim Osman — Bab International Corp',
    'maintainer': 'Abdulkaraim Osman',
    'support': 'sales@leapai.ai',
    'website': 'https://leapai.ai/',
    'license': 'LGPL-3',
    'application': True,
    'images': [
        'static/description/screen_projects.png',
        'static/description/screen_contract.png',
        'static/description/screen_hse.png',
    ],
    'depends': ['mail', 'hr', 'account'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/construction_project_views.xml',
        'views/construction_site_ops_views.xml',
        'views/construction_hse_views.xml',
        'views/construction_finance_views.xml',
        'views/construction_scheduling_views.xml',
        'views/construction_documents_views.xml',
        'views/construction_equipment_views.xml',
        'views/menu.xml',
    ],
    'demo': ['demo/demo_data.xml'],
    'installable': True,
    'auto_install': False,
}
