from odoo import models, fields, api

class JournalDetailWizard(models.TransientModel):
    _name = 'journal.detail.wizard'
    _description = 'Journal Detail Wizard'
    _log_access = True

    journal_id = fields.Many2one('account.journal', string="Journal")
    move_line_ids = fields.One2many('journal.detail.line', 'wizard_id', string="Journal Items")

    @api.model
    def default_get(self, fields):
        res = super().default_get(fields)
        journal_id = self.env.context.get('journal_id')
        if journal_id:
            lines = self.env['account.move.line'].search([('journal_id', '=', journal_id)])
            line_vals = [(0, 0, {
                'name': l.name,
                'partner_id': l.partner_id.id,
                'debit': l.debit,
                'credit': l.credit,
                'amount_currency': l.amount_currency,
            }) for l in lines]
            res.update({
                'journal_id': journal_id,
                'move_line_ids': line_vals
            })
        return res

class JournalDetailLine(models.TransientModel):
    _name = 'journal.detail.line'
    _description = 'Journal Detail Line'
    _log_access = True
    wizard_id = fields.Many2one('journal.detail.wizard')
    name = fields.Char()
    partner_id = fields.Many2one('res.partner')
    debit = fields.Float()
    credit = fields.Float()
    amount_currency = fields.Float()