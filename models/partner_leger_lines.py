from odoo import models, fields, api


class JournalLedgerLine(models.Model):
    _name = 'journal.ledger.line'
    _description = 'Custom Journal Ledger Line'
    _auto = False  # لأننا نعتمد على SQL View

    partner_id = fields.Many2one('res.partner', string='Partner')  # ✅ تعديل مهم
    journal_id = fields.Many2one('account.journal', string='Journal')  # ✅ تعديل مهم
    debit = fields.Monetary(string='Debit', currency_field='currency_id')
    credit = fields.Monetary(string='Credit', currency_field='currency_id')
    balance = fields.Monetary(string='Balance', currency_field='currency_id')
    negative_balance = fields.Monetary(string='Negative Balance', currency_field='currency_id')
    positive_balance = fields.Monetary(string='Positive Balance', currency_field='currency_id')
    currency_id = fields.Many2one('res.currency', string='Currency')  # نوع العملة

    def init(self):
        self._cr.execute("""
            CREATE OR REPLACE VIEW journal_ledger_line AS (
                SELECT 
                    row_number() OVER () as id,
                    am.partner_id,
                    am.journal_id,
                    SUM(aml.debit) AS debit,
                    SUM(aml.credit) AS credit,
                    SUM(aml.debit - aml.credit) AS balance,
                    c.id as currency_id,
                    CASE 
                        WHEN SUM(aml.debit - aml.credit) >= 0 THEN SUM(aml.debit - aml.credit)
                        ELSE 0 
                    END AS positive_balance,
                    CASE 
                        WHEN SUM(aml.debit - aml.credit) < 0 THEN SUM(aml.debit - aml.credit)
                        ELSE 0 
                    END AS negative_balance
                FROM account_move_line aml 
                JOIN account_move am ON am.id = aml.move_id
                JOIN res_currency c ON c.id = aml.company_currency_id
                 WHERE am.partner_id IS NOT NULL AND am.journal_id IS NOT NULL
                GROUP BY am.partner_id, am.journal_id, c.id
            )
        """)

    def open_journal_detail(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'journal.detail.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_journal_id': self.journal_id.id,
                'journal_id': self.journal_id.id
            }
        }
# from odoo import models, fields, api
#
#
# class JournalLedgerLine(models.Model):
#     _name = 'journal.ledger.line'
#     _description = 'Custom Journal Ledger Line'
#     _auto = False  # لأننا سنعتمد على SQL View
#
#     partner_id = fields.Many2one('account.move', string='Partner')
#     journal_id = fields.Many2one('account.move', string='Journal')
#     debit = fields.Monetary(string='Debit', currency_field='currency_id')
#     credit = fields.Monetary(string='Credit', currency_field='currency_id')
#     balance = fields.Monetary(string='Balance', currency_field='currency_id')
#     negative_balance = fields.Monetary(string='Negative Balance', currency_field='currency_id')
#     positive_balance = fields.Monetary(string='Positive Balance', currency_field='currency_id')
#     currency_id = fields.Many2one('res.currency', string='Currency')   #نوع العملة
#
#     def init(self):
#         self._cr.execute("""
#             CREATE OR REPLACE VIEW journal_ledger_line AS (
#                 SELECT
#                     row_number() OVER () as id,
#                     am.partner_id,
#                     am.journal_id,
#                     SUM(aml.debit) AS debit,
#                     SUM(aml.credit) AS credit,
#                     SUM(aml.debit - aml.credit) AS balance,
#                     c.id as currency_id,
#                     CASE
#                         WHEN SUM(aml.debit - aml.credit) >= 0 THEN SUM(aml.debit - aml.credit)
#                         ELSE 0
#                     END AS positive_balance,
#                     CASE
#                         WHEN SUM(aml.debit - aml.credit) < 0 THEN SUM(aml.debit - aml.credit)
#                         ELSE 0
#                     END AS negative_balance
#                 FROM account_move_line aml
#                 JOIN account_move am ON am.id = aml.move_id
#                 JOIN res_currency c ON c.id = aml.company_currency_id
#                 WHERE am.partner_id IS NOT NULL
#                 GROUP BY am.partner_id, am.journal_id, c.id
#             )
#         """)
#
#     def open_journal_detail(self):
#         return {
#             'type': 'ir.actions.act_window',
#             'res_model': 'journal.detail.wizard',
#             'view_mode': 'form',
#             'target': 'new',
#             'context': {
#                 'default_journal_id': self.journal_id.id,
#                 'journal_id': self.journal_id.id
#             }
#         }

