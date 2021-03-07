import pandas as pd


def get_out_txs(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.amount < 0]


def get_in_txs(df: pd.DataFrame) -> pd.DataFrame:
    return df[df.amount > 0]


def group_by_category(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("category", as_index=False)[['abs_amount', 'amount']].sum()


def group_by_date(df: pd.DataFrame) -> pd.DataFrame:
    return df.groupby("date", as_index=False)[['abs_amount', 'amount']].sum()
