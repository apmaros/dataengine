import uuid

from dataengine.model.dao.sentiment import Sentiment


def test_blank_returns_true_when_all_sentiment_values_are_none():
    under_test = Sentiment(
        id=uuid.uuid4(),
        user_id='some_id',
        parent_id='some_id',
        sad=None,
        anxiety=None,
        stress=None,
        happiness=None,
        energy=None,
        creativity=None,
    )

    assert under_test.blank()


def test_blank_returns_true_when_all_sentiment_values_are_zero():
    under_test = Sentiment(
        id=uuid.uuid4(),
        user_id='some_id',
        parent_id='some_id',
        sad=0,
        anxiety=0,
        stress=0,
        happiness=0,
        energy=0,
        creativity=0,
    )

    assert under_test.blank()


def test_blank_returns_false_if_any_value_is_non_zero():
    under_test = Sentiment(
        id=uuid.uuid4(),
        user_id='some_id',
        parent_id='some_id',
        sad=None,
        anxiety=None,
        stress=None,
        happiness=9,
        energy=None,
        creativity=None,
    )

    assert not under_test.blank()
