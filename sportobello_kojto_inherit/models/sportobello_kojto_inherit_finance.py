from odoo import models, fields, api, _
from datetime import timedelta
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class KojtoFinanceInvoicesInherit(models.Model):
    _inherit = "kojto.finance.invoices"

    user_id = fields.Many2one('res.users', string='User', default=lambda self: self.env.user)
    code = fields.Many2one('kojto.commission.codes', string='Code', related='subcode_id.code_id', store=True)
    subcode_is_active = fields.Boolean(string='Subcode is Active', related='subcode_id.active', store=True)

class KojtoFinanceCashflow(models.Model):
    _name = "kojto.finance.cashflow"
    _inherit = "kojto.finance.cashflow"

    @api.onchange("counterparty_bank_account_id", "counterparty_id")
    def _onchange_assign_bank_account_to_contact(self):
        if self.counterparty_bank_account_id and self.counterparty_id:
            if self.counterparty_bank_account_id.contact_id != self.counterparty_id:
                self.counterparty_bank_account_id.contact_id = self.counterparty_id


class KojtoFinanceCashflowAllocation(models.Model):
    _name = "kojto.finance.cashflow.allocation"
    _inherit = "kojto.finance.cashflow.allocation"

    def make_amount_positive(self):
        for record in self:
            if record.amount and record.amount < 0:
                record.amount = abs(record.amount)

class KojtoLandingpage(models.Model):
    _inherit = "kojto.landingpage"

    def open_sportobello_invoice_list_view(self):
        action_id = self.env.ref("kojto_finance.action_kojto_finance_invoices").id
        url = f"/web#action={action_id}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }

    def open_sportobello_cashflow_list_view(self):
        action_id = self.env.ref("kojto_finance.action_kojto_finance_cashflow").id
        url = f"/web#action={action_id}"

        return {
            "type": "ir.actions.act_url",
            "url": url,
            "target": "self",
        }
