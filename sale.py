class Venta:
    def __init__(self, id_vendedor: int, id_cliente: int, productos: list[dict], fecha: str, idVenta: str = None, total: float = None) -> None:
        self.id_vendedor = id_vendedor
        self.id_cliente = id_cliente
        self.productos = productos
        self.fecha = fecha
        self.idVenta = idVenta
        self.total = total
    
    @staticmethod
    def from_dict(data: dict) -> 'Venta':
        return Venta(**data)