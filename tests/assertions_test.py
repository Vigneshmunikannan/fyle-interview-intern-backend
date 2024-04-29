import pytest
from core.libs.assertions import base_assert, assert_auth, assert_true, assert_valid, assert_found
from core.libs.exceptions import FyleError

def test_base_assert():
    with pytest.raises(FyleError) as exc_info:
        base_assert(401, "Test message")
    assert exc_info.value.status_code == 401
    assert exc_info.value.message == "Test message"

def test_assert_auth():
    with pytest.raises(FyleError) as exc_info:
        assert_auth(False, "Test message")
    assert exc_info.value.status_code == 401
    assert exc_info.value.message == "Test message"

def test_assert_true():
    with pytest.raises(FyleError) as exc_info:
        assert_true(False, "Test message")
    assert exc_info.value.status_code == 403
    assert exc_info.value.message == "Test message"

def test_assert_valid():
    with pytest.raises(FyleError) as exc_info:
        assert_valid(False, "Test message")
    assert exc_info.value.status_code == 400
    assert exc_info.value.message == "Test message"

def test_assert_found():
    with pytest.raises(FyleError) as exc_info:
        assert_found(None, "Test message")
    assert exc_info.value.status_code == 404
    assert exc_info.value.message == "Test message"
