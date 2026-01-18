#--------# 4 დავალება ---------
from turtle import TurtleScreen

import pytest

def check_login(login, password):
    users = {
        "admin": "Admin123!",
        "user": "User123!"
    }

    if login not in users:
        raise ValueError("მომხმარებელი ვერ მოიძებნა")

    if users[login] != password:
        raise ValueError("პაროლი არასწორია")

    return True


def test_correct_login():
    assert check_login("admin", "Admin123!") is True


def test_wrong_password():
    with pytest.raises(ValueError):
        check_login("admin", "wrong")


def test_user_not_found():
    with pytest.raises(ValueError):
        check_login("unknown", "1234")




#---------------5 დავალება ---------------------


def is_valid_email(email):
    if "@" not in email or "." not in email:
        return False
    return True

def test_valid_email():
    assert is_valid_email("test@example.com") is True

def test_email_without_at():
    assert is_valid_email("testexample.com") is False

def test_email_without_dot():
    assert is_valid_email("test@examplecom") is False


def test_empty_string():
    assert is_valid_email("") is False


#--------------6 დავალება ---------------------
















