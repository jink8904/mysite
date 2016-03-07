from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('control_inventario.app',
   url(r'^$', 'auth.views.index', name='index'),
   #login
   url(r'^ingresar/$','auth.views.ingresar', name='ingresar'),
   url(r'^cerrar/$','auth.views.cerrar_session', name='cerrar'),
   # urls-empresa
    url(r'^empresa/$', 'empresa.views.empresa', name='empresa'),
    url(r'^empresa/del$', 'empresa.views.del_empresa', name='del_empresa'),
    url(r'^select-empresa$', 'empresa.views.select_empresa', name='select_empresa'),
   # urls-categoria
    url(r'^categorias/$', 'categoria.views.categoria', name='categoria'),
    url(r'^categorias/del$', 'categoria.views.del_categoria', name='del_categoria'),
   # urls-productos
    url(r'^productos/$', 'producto.views.producto', name='producto'),
    url(r'^productos/del$', 'producto.views.del_producto', name='del_producto'),
   # urls-proveedor
    url(r'^proveedor/$', 'proveedor.views.proveedor', name='proveedor'),
    url(r'^proveedor/del$', 'proveedor.views.del_proveedor', name='del_proveedor'),
   # urls-proveedor
    url(r'^cliente/$', 'cliente.views.cliente', name='cliente'),
    url(r'^cliente/del$', 'cliente.views.del_cliente', name='del_cliente'),
   # urls-inventario inicial
    url(r'^inventario/$', 'inventario.views.inventario_inicial', name='inventario'),
   # urls-salida de mercancia
    url(r'^salida/$', 'salida_mercancia.views.salida_mercancia', name='salida_mercancia'),
    url(r'^salida/add$', 'salida_mercancia.views.add_salida_mercancia', name='add_salida_mercancia'),
    url(r'^salida/detalles$', 'salida_mercancia.views.detalle_venta', name='detalle_venta'),
   # urls-entrada de mercancia
    url(r'^entrada/$', 'entrada_mercancia.views.entrada_mercancia', name='entrada_mercancia'),
    url(r'^entrada/add$', 'entrada_mercancia.views.add_entrada_mercancia', name='add_entrada_mercancia'),
    url(r'^entrada/detalles$', 'entrada_mercancia.views.detalle_compra', name='detalle_compra'),
   # urls-registo de ventas
    url(r'^registro-ventas/$', 'registro_venta.views.registro_ventas', name='registro_ventas'),
   # urls-resumen de movimientos
    url(r'^resumen-movimientos/$', 'resumen_movimientos.views.resumen_mov', name='resumen_mov'),
   # urls-stock disponible
    url(r'^stock-disponible/$', 'stock_disponible.views.stock_disponible', name='stock_disponible'),
   # urls-resumen de ventas
    url(r'^resumen-ventas/$', 'resumen_ventas.views.resumen_venta', name='resumen_venta'),
    url(r'^resumen-ventas/detalles$', 'resumen_ventas.views.detalle_venta', name='detalle_venta'),
   # urls-resumen de compra
    url(r'^resumen-compras/$', 'resumen_compras.views.resumen_compra', name='resumen_compra'),
    url(r'^resumen-compras/detalles$', 'resumen_compras.views.detalle_compra', name='detalle_compra'),
   # exportar a excel
   #  url(r'^export/$', 'control_inventario.views.export', name='export'),


)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)