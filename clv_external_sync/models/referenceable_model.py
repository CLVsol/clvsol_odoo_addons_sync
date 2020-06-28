# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class ExternalSyncBatchMember(models.Model):
    _name = "clv.external_sync.batch.member"
    _inherit = 'clv.external_sync.batch.member', 'clv.abstract.reference'

    ref_method = fields.Char(
        string='Method',
        compute='_compute_refenceable_model_schedule',
        store=True
    )

    ref_disable_identification = fields.Boolean(
        string='Disable Identification',
        compute='_compute_refenceable_model_schedule',
        store=True
    )
    ref_disable_identification_suport = fields.Boolean(
        string='Disable Identification:',
        compute='_compute_refenceable_model_schedule',
        store=False,
        compute_sudo=True
    )

    ref_disable_inclusion = fields.Boolean(
        string='Disable Inclusion',
        compute='_compute_refenceable_model_schedule',
        store=True
    )
    ref_disable_inclusion_suport = fields.Boolean(
        string='Disable Inclusion:',
        compute='_compute_refenceable_model_schedule',
        store=False,
        compute_sudo=True
    )

    ref_disable_sync = fields.Boolean(
        string='Disable Sync',
        compute='_compute_refenceable_model_schedule',
        store=True
    )
    ref_disable_sync_suport = fields.Boolean(
        string='Disable Sync:',
        compute='_compute_refenceable_model_schedule',
        store=False,
        compute_sudo=True
    )

    @api.depends('ref_id')
    def _compute_refenceable_model_schedule(self):
        for record in self:
            try:
                if record.ref_id:
                    record.ref_method = record.ref_id.method
                    record.ref_disable_identification = record.ref_id.disable_identification
                    record.ref_disable_inclusion = record.ref_id.disable_inclusion
                    record.ref_disable_sync = record.ref_id.disable_sync
                    record.ref_disable_identification_suport = record.ref_id.disable_identification
                    record.ref_disable_inclusion_suport = record.ref_id.disable_inclusion
                    record.ref_disable_sync_suport = record.ref_id.disable_sync
            except Exception:
                record.ref_method = False
                record.ref_disable_identification = False
                record.ref_disable_inclusion = False
                record.ref_disable_sync = False
                record.ref_disable_identification_suport = False
                record.ref_disable_inclusion_suport = False
                record.ref_disable_sync_suport = False
