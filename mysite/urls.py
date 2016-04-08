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
    url(r'^select-periodo$', 'empresa.views.select_periodo', name='select_periodo'),
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
   # urls-inventario
    url(r'^inventario/$', 'inventario.views.inventario_inicial', name='inventario'),
    url(r'^inventario-inicial/$', 'inventario.views.inventario_inicial_consulta', name='inventario'),
   # urls-salida de mercancia
    url(r'^salida/$', 'salida_mercancia.views.salida_mercancia', name='salida_mercancia'),
    url(r'^salida/del$', 'salida_mercancia.views.del_venta', name='del_venta'),
    url(r'^salida/add$', 'salida_mercancia.views.add_salida_mercancia', name='add_salida_mercancia'),
    url(r'^salida/detalles$', 'salida_mercancia.views.detalle_venta', name='detalle_venta'),
   # urls-entrada de mercancia
    url(r'^entrada/$', 'entrada_mercancia.views.entrada_mercancia', name='entrada_mercancia'),
    url(r'^entrada/add$', 'entrada_mercancia.views.add_entrada_mercancia', name='add_entrada_mercancia'),
    url(r'^entrada/del$', 'entrada_mercancia.views.del_compra', name='del_venta'),
    url(r'^entrada/detalles$', 'entrada_mercancia.views.detalle_compra', name='detalle_compra'),
   # urls-registo de ventas
    url(r'^registro-ventas/$', 'registro_venta.views.registro_ventas', name='registro_ventas'),
   # urls-resumen de movimientos
   #  url(r'^resumen-mov/$', 'resumen_movimientos.views.resumen_mov', name='resumen_mov'),
    url(r'^resumen-movimientos-productos/$', 'resumen_movimientos_prod.views.resumen_mov', name='resumen_mov'),
    url(r'^resumen-movimientos-productos/export-excel$', 'resumen_movimientos_prod.views.export_excel'),
    url(r'^resumen-movimientos-productos/export-pdf$', 'resumen_movimientos_prod.views.export_pdf'),
   # urls-stock disponible
    url(r'^stock-disponible/$', 'stock_disponible.views.stock_disponible', name='stock_disponible'),
    url(r'^stock-disponible/export-excel$', 'stock_disponible.views.export_excel'),
    url(r'^stock-disponible/export-pdf$', 'stock_disponible.views.export_pdf'),
   # urls-resumen de ventas
    url(r'^resumen-ventas/$', 'resumen_ventas.views.resumen_venta', name='resumen_venta'),
    url(r'^resumen-ventas/detalles$', 'resumen_ventas.views.detalle_venta', name='detalle_venta'),
   # urls-resumen de compra
    url(r'^resumen-compras/$', 'resumen_compras.views.resumen_compra', name='resumen_compra'),
    url(r'^resumen-compras/detalles$', 'resumen_compras.views.detalle_compra', name='detalle_compra'),
   # reporte de clientes
    url(r'^reporte-cliente-diario/', 'reportes_cliente.views.reporte_cliente', {"tipo":"diario"}),


)

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)