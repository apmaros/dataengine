from dataengine.model.item_group import ItemGroup


def test_item_group_is_not_empty_when_contains_items():
    under_test = ItemGroup('my-key', [])
    assert under_test.is_empty()


def test_item_group_is_empty_when_contains_no_items():
    under_test = ItemGroup('my-key', ['my-item'])
    assert not under_test.is_empty()
