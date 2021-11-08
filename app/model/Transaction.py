from dataclasses import dataclass


@dataclass
class Transaction:
    id: str
    name: str
    type: str
    created_at: str
    time: str
    category: str
    amount: int
    currency: str
    notes: str
    description: str
    address: str

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
    return Transaction(
        raw_transaction['id'],
        raw_transaction['description'],
        'Unknown',
        raw_transaction['created'],
        raw_transaction['created'],
        raw_transaction['category'],
        raw_transaction['amount'],
        raw_transaction['currency'],
        raw_transaction['notes'],
        None,
        None
    )