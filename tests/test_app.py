from app.app import get_hash


def test_get_hash():
    assert get_hash("hello") != "hello"
