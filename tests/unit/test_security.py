import pytest

from app.core.exceptions import UnauthorizedError
from app.core.security import (
    create_access_token,
    decode_access_token,
    get_password_hash,
    verify_password,
)


def test_password_hashing_and_verification():
    raw_password = "mysecretpassword"
    hashed = get_password_hash(raw_password)

    assert hashed != raw_password
    assert verify_password(raw_password, hashed) is True
    assert verify_password("wrongpassword", hashed) is False


def test_jwt_create_and_decode():
    token = create_access_token({"sub": "USR-999"})
    payload = decode_access_token(token)

    assert payload["sub"] == "USR-999"
    assert "exp" in payload
    assert "iat" in payload


def test_invalid_jwt_token():
    with pytest.raises(UnauthorizedError):
        decode_access_token("invalid.jwt.token")
