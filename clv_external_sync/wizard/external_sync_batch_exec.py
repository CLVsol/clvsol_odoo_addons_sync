# -*- coding: utf-8 -*-
# Copyright (C) 2013-Today  Carlos Eduardo Vercelino - CLVsol
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
from functools import reduce

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


def secondsToStr(t):
    return "%d:%02d:%02d.%03d" % reduce(lambda ll, b: divmod(ll[0], b) + ll[1:], [(t * 1000,), 1000, 60, 60])


class ExternalSyncBatchExec(models.TransientModel):
    _description = 'External Sync Batch Exec'
    _name = 'clv.external_sync.batch.exec'

    def _default_batch_ids(self):
        return self._context.get('active_ids')
    batch_ids = fields.Many2many(
        comodel_name='clv.external_sync.batch',
        relation='clv_external_sync_batch_exec_rel',
        string='Batchs to Execute',
        default=_default_batch_ids)
    count_batches = fields.Integer(
        string='Number of Batchs',
        compute='_compute_count_batches',
        store=False
    )

    # @api.multi
    @api.depends('batch_ids')
    def _compute_count_batches(self):
        for r in self:
            r.count_batches = len(r.batch_ids)

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
    def do_external_sync_batch_exec(self):
        self.ensure_one()

        from time import time
        start = time()

        sync_log = False

        for batch in self.batch_ids:

            _logger.info(u'%s %s', '>>>>>', batch.name)

            if sync_log is False:
                sync_log = '########## ' + batch.name + ' ##########\n'
            else:
                sync_log += '\n########## ' + batch.name + ' ##########\n'

            for external_sync_batch_member in batch.external_sync_batch_member_ids:

                if external_sync_batch_member.enabled:

                    schedule = external_sync_batch_member.ref_id

                    _logger.info(u'%s %s', '>>>>>', schedule.name)

                    model = schedule.model
                    _logger.info(u'%s %s [%s]', '>>>>>', schedule.name, model)

                    # method_call = False
                    # if schedule.method == '_object_external_sync':
                    #     method_call = 'self.env["clv.external_sync"].' + schedule.method + '(schedule)'
                    # elif schedule.method == '_object_external_recognize':
                    #     method_call = 'self.env["clv.external_sync"].' + schedule.method + '(schedule)'

                    method_call = 'self.env["clv.external_sync"].' + schedule.method + '(schedule)'

                    _logger.info(u'%s %s %s', '>>>>>>>>>>', schedule.method, method_call)

                    if method_call:

                        schedule.sync_log = 'method: ' + str(schedule.method) + '\n\n'
                        schedule.sync_log +=  \
                            'external_host: ' + str(schedule.external_host_id.name) + '\n' + \
                            'external_dbname: ' + str(schedule.external_host_id.external_dbname) + '\n\n' + \
                            'max_task: ' + str(schedule.max_task) + '\n' + \
                            'enable_identification: ' + \
                            str(schedule.enable_identification) + '\n' + \
                            'enable_check_missing: ' + \
                            str(schedule.enable_check_missing) + '\n' + \
                            'enable_inclusion: ' + str(schedule.enable_inclusion) + '\n' + \
                            'enable_sync: ' + str(schedule.enable_sync) + '\n' + \
                            'external_last_update_args: ' + str(schedule.external_last_update_args()) + '\n\n' + \
                            'enable_sequence_code_sync: ' + str(schedule.enable_sequence_code_sync) + '\n\n'

                        exec(method_call)

                    sync_log += '\n########## ' + schedule.name + ' ##########\n'
                    sync_log += schedule.sync_log

                    self.env.cr.commit()

            sync_log += '\n############################################################'
            sync_log +=  \
                '\nExecution time: ' + str(secondsToStr(time() - start)) + '\n'

            batch.sync_log = sync_log

            _logger.info(u'%s %s', '>>>>> Execution time: ', secondsToStr(time() - start))

        return True
        # return self._reopen_form()
