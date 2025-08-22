/** ملف JS داخل مجلد static/src/js */

odoo.define('a_partner_ledger_local.open_journal_wizard', function (require) {
    "use strict";

    const ListController = require('web.ListController');
    const viewRegistry = require('web.view_registry');
    const ListView = require('web.ListView');
    const rpc = require('web.rpc');

    const JournalListController = ListController.extend({
        _onRowClicked: function (event) {
            const $target = $(event.target);

            if ($target.closest('td[data-name="journal_id"]').length) {
                const recordId = this.getSelectedIds()[0];

                rpc.query({
                    model: 'journal.details.wizard',
                    method: 'open_journal_details',
                    args: [recordId],
                }).then(action => {
                    this.do_action(action);
                });
            } else {
                this._super.apply(this, arguments);
            }
        }
    });

    const JournalListView = ListView.extend({
        config: _.extend({}, ListView.prototype.config, {
            Controller: JournalListController,
        }),
    });

    viewRegistry.add('journal_list_clickable', JournalListView);

});