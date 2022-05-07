import typing as t
from dataclasses import dataclass

from dataengine.monzo.model.Merchant import Merchant, build_merchant


@dataclass
class Transaction:
    id: str
    name: str
    type: str
    created_at: str
    time: str
    category: str
    amount: int
    abs_amount: int
    currency: str
    notes: str
    description: str
    address: t.Optional[str]
    merchant: t.Optional[Merchant] = None

    def to_plot_dict(self):
        return {
            'time': self.created_at,
            'date': self.created_at.split("T")[0],
            'amount': self.amount / 100,
            'name': self.name,
            'category': self.category if self.category else 'unknown',
            'abs_amount': abs(self.amount) / 100,
            'type': "CREDIT" if self.amount > 0 else "DEBIT"
        }


def build_transaction(raw_transaction):
    raw_merchant = raw_transaction.get('merchant', {})
    merchant = build_merchant(raw_merchant) if raw_merchant else None

    return Transaction(
        id=raw_transaction['id'],
        name=raw_transaction['description'],
        type="CREDIT" if raw_transaction['amount'] > 0 else "DEBIT",
        created_at=raw_transaction['created'],
        time=raw_transaction['created'],
        category=raw_transaction.get('category', 'unknown'),
        amount=raw_transaction['amount'] / 100,
        abs_amount=abs(raw_transaction['amount']) / 100,
        currency=raw_transaction['currency'],
        notes=raw_transaction['notes'],
        description=None,
        address=None,
        merchant=merchant
    )
