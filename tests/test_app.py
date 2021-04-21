from app.app import get_hash, verify_hash, db
import os
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

    db.conn.execute("DELETE FROM users")
    db.conn.execute("COMMIT")

    user_id = db.create_user(email, password)

    # here I'm using the internal DB connection in the class to send a custom
    # SQL query
    # I'm doing this to get the email and the hashed password of the user we just
    # created. The email should be the same one we have used in the
    # db.create_user() function
    result = db.conn.execute(
        "SELECT * from users where user_id = ?", (user_id,)
    ).fetchone()

    # result is a tuple with 3 elements:
    # (user_id, email, hashed_password)

    user_id = result[0]
    new_user_email = result[1]
    hashed_password = result[2]

    # make sure the emails match
    assert new_user_email == email

    assert db.validate_password(email, password)

    # TODO
    # examples of what to test
    # 1. verify user is created
    # 2. verify you can validate the hash
    # 3. whatever you come up with
    pass
