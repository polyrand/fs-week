from app.app import get_hash, verify_hash
import re
import pytest


def test_get_hash():
    assert get_hash("hello") != "hello"
    assert get_hash("strive") != "strive"


def test_bcrypt():

    bcrypt_hash_pattern = r"^\$2[ayb]\$.{56}$"
    pat = re.compile(bcrypt_hash_pattern)

    new_hash = get_hash("Hello")

    assert pat.search(new_hash)


@pytest.mark.parametrize("testing_string", [("hello"), ("strive"), ("asdasd")])
def test_hash_computation(testing_string):
    # testing_string = "hello"
    new_hash = get_hash(testing_string)

    assert verify_hash(testing_string, new_hash)


@pytest.mark.parametrize(
    "email,password", [("hello@hello.com", "asd"), ("strive@strive.com", "asdasd")]
)
def test_user_creation(email, password):
    # TODO
    # examples of what to test
    # 1. verify user is created
    # 2. verify you can validate the hash
    # 3. whatever you come up with
    pass
