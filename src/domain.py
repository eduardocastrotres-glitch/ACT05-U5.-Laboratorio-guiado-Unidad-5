from dataclasses import dataclass


class User:
    def __init__(self, role: str, id: int | None = None):
        self.role = role
        self.id = id
class CustomerHasDebt(Exception):
    pass

@dataclass
class Order:
    total: float
    vip: bool = False
    status: str = "NEW"
    discount: float = 0.0
    hours_elapsed: int = 0
    owner_id: int = None
    def __init__(self, total: float, status: str = "NEW", vip: bool = False, hours_elapsed: int = 0, owner_id: int | None = None):
        self.total = total
        self.status = status
        self.vip = vip
        self.discount = 0.0
        self.hours_elapsed = hours_elapsed
        self.owner_id = owner_id

    def confirm(self, customer_debt=0):
        if self.status == "CONFIRMED":
            raise ValueError("already confirmed")

        if self.total <= 0:
            raise ValueError("total must be positive")
        if customer_debt > 0:
            raise CustomerHasDebt("outstanding debt")
        self.discount = round(self.total * 0.15, 2) if self.vip else 0.0
        self.status = "CONFIRMED"
        return self.total - self.discount
    
    def cancel(self, user: User) -> bool:
        """Regla de seguridad: Administradores pueden cancelar siempre;
        el propietario solo si no han pasado más de 24 horas."""
        if self.status != "NEW":
            raise ValueError("Order cannot be cancelled")

        if user.role == "admin":
            self.status = "CANCELLED"
            return True

        if user.role == "owner":
            if self.hours_elapsed > 24:
                raise PermissionError("Time limit exceeded")
            self.status = "CANCELLED"
            return True

        raise PermissionError("Unauthorized action")
class PaymentGateway:

    def charge(self, amount: float) -> bool:
        # Método simulado de cobro externo
        pass

def charge_card(amount: float) -> bool:
    """Función externa simulada para la pasarela de pagos."""
