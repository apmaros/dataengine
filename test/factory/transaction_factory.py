from random import randint

from dataengine.common.util import random_str, current_time_sec
from dataengine.monzo.model.Transaction import Transaction
from factory.util import rand

TX_CATEGORY_SAMPLE = ['shopping', 'eating-out', 'travel']
TX_TYPE = ['CREDIT', 'DEBIT']
TX_NAME_SAMPLE = [
    'Padella Shoreditch',
    'Deliveroo',
    'ClassPass',
    'Mega Food And Wine',
    'Eloisa Campos',
    'TOPUP DEC',
]


def make_raw_transaction(
    monzo_id: int = random_str(),
    time: int = current_time_sec(),
    category: str = rand(TX_CATEGORY_SAMPLE),
    name: str = rand(TX_NAME_SAMPLE),
    amount: int = randint(-1000, 1000),
    notes: str = random_str()
):
    return {
        'id': monzo_id,
        'description': name,
        'created': time,
        'category': category,
        'amount': amount,
        'currency': 'GBP',
        'notes': notes
    }


def make_raw_merchant(
    group_id: random_str(),
    name: random_str(),
    category: rand(TX_CATEGORY_SAMPLE)
):
    return {
        'id': id,
        'group_id': group_id,
        'name': name,
        'logo': None,
        'emoji': None,
        'category': category,
    }


def make_transaction(
    monzo_id: int = random_str(),
    time: int = current_time_sec(),
    category: str = rand(TX_CATEGORY_SAMPLE),
    monzo_type: str = rand(TX_TYPE),
    name: str = rand(TX_NAME_SAMPLE),
    amount: int = randint(-1000, 1000),
    notes: str = random_str()
):
    return Transaction(
        id=monzo_id,
        name=name,
        type=monzo_type,
        created_at=time,
        time=time,
        category=category,
        amount=amount,
        abs_amount=abs(amount),
        currency='GBP',
        notes=notes,
        description=name,
        address=None,
        merchant=None
    )
