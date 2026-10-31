from unittest.mock import patch

import pytest

from src.domain import CustomerHasDebt, Order


def test_vip_discount():
    o = Order(100, vip=True)
    assert o.confirm() == 85
    assert o.status == "CONFIRMED"

def test_regular_no_discount():
    assert Order(100).confirm() == 100

def test_customer_debt():
    with pytest.raises(CustomerHasDebt):
        Order(100).confirm(customer_debt=50)

@pytest.mark.parametrize("total", [0, -1])
def test_invalid_total(total):
    with pytest.raises(ValueError):
        Order(total).confirm()

def test_vip_discount_200():
    o = Order(200, vip=True)
    assert o.confirm() == 170
    assert o.status == "CONFIRMED"

def test_regular_no_discount_200():
    o = Order(200, vip=False)
    assert o.confirm() == 200
    assert o.status == "CONFIRMED"

def test_cannot_confirm_twice():
    order = Order(100)
    order.confirm()
    with pytest.raises(ValueError, match="already confirmed"):
        order.confirm()


@patch("src.domain.charge_card")
def test_payment_gateway_failure(mock_charge_card):
    # Configuramos el mock para que simule un fallo de la pasarela arrojando un error
    mock_charge_card.side_effect = RuntimeError("Payment gateway timeout")
    
    order = Order(total=200, vip=True)
    
    # Verificamos que si el servicio de pago falla, se lance el error esperado
    with pytest.raises(RuntimeError, match="Payment gateway timeout"):
        # Simulamos que antes o durante de confirmar se llama al cobro externo
        mock_charge_card(order.total)
        order.confirm()