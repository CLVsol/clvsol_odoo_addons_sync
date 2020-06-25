# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging

from odoo import fields, models

_logger = logging.getLogger(__name__)


class ExternalSypnScheduleMassEdit(models.TransientModel):
    _description = 'External Sync Schedule Mass Edit'
    _name = 'clv.external_sync.schedule.mass_edit'

    def _default_external_sync_schedule_ids(self):
        return self._context.get('active_ids')
    external_sync_schedule_ids = fields.Many2many(
        comodel_name='clv.external_sync.schedule',
        relation='clv_external_sync_schedule_mass_edit_rel',
        string='External Sync Schedules',
        default=_default_external_sync_schedule_ids
    )

    external_host_id = fields.Many2one(
        comodel_name='clv.external_sync.host',
        string='External Host'
    )
    external_host_id_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='External Host:', default=False, readonly=False, required=False
    )

    max_task = fields.Integer(
        string='Max Task Registers'
    )
    max_task_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Max Task Registers:', default=False, readonly=False, required=False
    )

    disable_identification = fields.Boolean(
        string='Disable Identification'
    )
    disable_identification_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Disable Identification:', default=False, readonly=False, required=False
    )

    disable_check_missing = fields.Boolean(
        string='Disable Check Missing'
    )
    disable_check_missing_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Disable Check Missing:', default=False, readonly=False, required=False
    )

    disable_inclusion = fields.Boolean(
        string='Disable Inclusion'
    )
    disable_inclusion_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Disable Inclusion:', default=False, readonly=False, required=False
    )

    disable_sync = fields.Boolean(
        string='Disable Sync'
    )
    disable_sync_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Disable Sync:', default=False, readonly=False, required=False
    )

    external_last_update_start = fields.Datetime(
        string="Last Update (Start)"
    )
    external_last_update_start_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Last Update (Start):', default=False, readonly=False, required=False
    )

    external_last_update_end = fields.Datetime(
        string="Last Update (End)"
    )
    external_last_update_end_selection = fields.Selection(
        [('set', 'Set'),
         ('remove', 'Remove'),
         ], string='Last Update (End):', default=False, readonly=False, required=False
    )

    # @api.multi
    def _reopen_form(self):
        self.ensure_one()
        action = {
            'type': 'ir.actions.act_window',
            'res_model': self._name,
            'res_id': self.id,
            'view_type': 'form',
            'view_mode': 'form',
            'target': 'new',
        }
        return action

    # @api.multi
    def do_external_sync_schedule_mass_edit(self):
        self.ensure_one()

        for external_sync_schedule in self.external_sync_schedule_ids:

            _logger.info(u'%s %s', '>>>>>', external_sync_schedule.name)

            if self.external_host_id_selection == 'set':
                external_sync_schedule.external_host_id = self.external_host_id.id
            if self.external_host_id_selection == 'remove':
                external_sync_schedule.external_host_id = False

            if self.max_task_selection == 'set':
                external_sync_schedule.max_task = self.max_task
            if self.max_task_selection == 'remove':
                external_sync_schedule.max_task = False

            if self.disable_identification_selection == 'set':
                external_sync_schedule.disable_identification = self.disable_identification
            if self.disable_identification_selection == 'remove':
                external_sync_schedule.disable_identification = False

            if self.disable_check_missing_selection == 'set':
                external_sync_schedule.disable_check_missing = self.disable_check_missing
            if self.disable_check_missing_selection == 'remove':
                external_sync_schedule.disable_check_missing = False

            if self.disable_inclusion_selection == 'set':
                external_sync_schedule.disable_inclusion = self.disable_inclusion
            if self.disable_inclusion_selection == 'remove':
                external_sync_schedule.disable_inclusion = False

            if self.disable_sync_selection == 'set':
                external_sync_schedule.disable_sync = self.disable_sync
            if self.disable_sync_selection == 'remove':
                external_sync_schedule.disable_sync = False

            if self.external_last_update_start_selection == 'set':
                external_sync_schedule.external_last_update_start = self.external_last_update_start
            if self.external_last_update_start_selection == 'remove':
                external_sync_schedule.external_last_update_start = False

            if self.external_last_update_end_selection == 'set':
                external_sync_schedule.external_last_update_end = self.external_last_update_end
            if self.external_last_update_end_selection == 'remove':
                external_sync_schedule.external_last_update_end = False

        return True
