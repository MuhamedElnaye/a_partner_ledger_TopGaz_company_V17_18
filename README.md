# Journal Ledger Line (Custom Odoo Module)

## Overview
This module introduces a **custom SQL view model** in Odoo that summarizes journal ledger data per **Partner** and **Journal**.  
It allows accountants and users to quickly see debit, credit, and balance information, with additional support for positive and negative balances.

## Technical Details
The model is defined as:

- **Model Name:** `journal.ledger.line`  
- **Type:** SQL View (`_auto = False`)  

The SQL View aggregates data from:
- `account_move_line`
- `account_move`
- `res_currency`

### Fields
- **partner_id** (`Many2one → res.partner`) – Partner related to the journal entry  
- **journal_id** (`Many2one → account.journal`) – Journal  
- **debit** (`Monetary`) – Total debit  
- **credit** (`Monetary`) – Total credit  
- **balance** (`Monetary`) – Debit - Credit  
- **positive_balance** (`Monetary`) – Positive part of balance (if ≥ 0)  
- **negative_balance** (`Monetary`) – Negative part of balance (if < 0)  
- **currency_id** (`Many2one → res.currency`) – Currency  

### SQL View
The view groups journal entries by **partner** and **journal**, computing totals for debit, credit, and balance.  

```sql
SELECT 
    row_number() OVER () as id,
    am.partner_id,
    am.journal_id,
    SUM(aml.debit) AS debit,
    SUM(aml.credit) AS credit,
    SUM(aml.debit - aml.credit) AS balance,
    c.id as currency_id,
    CASE WHEN SUM(aml.debit - aml.credit) >= 0 THEN SUM(aml.debit - aml.credit) ELSE 0 END AS positive_balance,
    CASE WHEN SUM(aml.debit - aml.credit) < 0 THEN SUM(aml.debit - aml.credit) ELSE 0 END AS negative_balance
FROM account_move_line aml
JOIN account_move am ON am.id = aml.move_id
JOIN res_currency c ON c.id = aml.company_currency_id
WHERE am.partner_id IS NOT NULL AND am.journal_id IS NOT NULL
GROUP BY am.partner_id, am.journal_id, c.id
