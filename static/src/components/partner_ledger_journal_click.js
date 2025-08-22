odoo.define('a_partner_ledger_local.partner_ledger_journal_click', function (require) {
  'use strict';
  const core = require('web.core');
  const actionService = require('@web/core/action_service');

  document.addEventListener('click', function (ev) {
    const el = ev.target;
    if (el.classList.contains('open-journal-wizard')) {
      ev.preventDefault();
      const jId = el.getAttribute('data-journal-id');
      if (jId) {
        actionService.doAction({
          type: 'ir.actions.act_window',
          res_model: 'journal.details.wizard',
          view_mode: 'form',
          target: 'new',
          context: { default_journal_id: parseInt(jId) },
        });
      }
    }
  });
});