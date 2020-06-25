# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ExternalSyncBatchMember(models.Model):
    _name = "clv.external_sync.batch.member"
    _inherit = 'clv.external_sync.batch.member', 'clv.abstract.reference'

    ref_method = fields.Char(
        string='Model',
        compute='_compute_refenceable_model_schedule',
        store=True
    )

    @api.depends('ref_id')
    def _compute_refenceable_model_schedule(self):
        for record in self:
            try:
                if record.ref_id:
                    record.ref_method = record.ref_id.method
            except Exception:
                record.ref_method = False
