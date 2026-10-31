from datetime import UTC, datetime, timedelta

from src.domain import Order, User
from src.security import can_cancel


def test_owner_within_24h():
    now = datetime.now(UTC)
    assert can_cancel("NEW", 1, 1, False, now - timedelta(hours=1), now)

def test_stranger_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 2, False, now, now)

def test_shipped_denied_even_admin():
    now = datetime.now(UTC)
    assert not can_cancel("SHIPPED", 1, 1, True, now, now)

def test_expired_denied():
    now = datetime.now(UTC)
    assert not can_cancel("NEW", 1, 1, False, now - timedelta(hours=25), now)
   
def test_admin_can_cancel_order():
    order = Order(150, status="NEW")
    user = User(role="admin")

    assert order.cancel(user) == True
    assert order.status == "CANCELLED"

def test_owner_cannot_cancel_after_time_limit():
    order = Order(150, status="NEW", hours_elapsed=25) # Pasaron más de 24 horas
    user = User(role="owner", id=1)
    order.owner_id = 1

    import pytest
    with pytest.raises(PermissionError, match="Time limit exceeded"):
        order.cancel(user)
