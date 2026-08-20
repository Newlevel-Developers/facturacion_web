from .auth import login, index, user_logout_view,profile, editar_perfil
from .product import productos, crear_producto,editar_producto,eliminar_producto,crear_categoria,editar_categoria,eliminar_categoria
from .sale_order import nueva_venta, registrar_compra
from .client import clientes, registrar_clientes
from .billing import facturas,billing,crear_factura,detalle_factura,anular_factura
from .users import usuarios, registrar_usuario, editar_usuario ,crear_rol,editar_rol,eliminar_rol