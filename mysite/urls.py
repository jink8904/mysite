from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'django_projects.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

   url(r'^ingresar/$','control_inventario.views.ingresar', name='ingresar'),
   url(r'^cerrar/$','control_inventario.views.cerrar_session', name='cerrar'),

    url(r'^$', 'control_inventario.views.index', name='index'),
   # urls-empresa
    url(r'^empresa/$', 'control_inventario.views.empresa', name='empresa'),
    url(r'^empresa/del$', 'control_inventario.views.del_empresa', name='del_empresa'),
    # url(r'^selempresa$', 'control_inventario.views.sel_empresa', name='sel_empresa'),
    url(r'^select-empresa$', 'control_inventario.views.select_empresa', name='select_empresa'),
   # urls-categoria
    url(r'^categorias/$', 'control_inventario.views.categoria', name='categoria'),
    url(r'^categorias/del$', 'control_inventario.views.del_categoria', name='del_categoria'),
   # urls-productos
    url(r'^productos/$', 'control_inventario.views.producto', name='producto'),
    url(r'^productos/del$', 'control_inventario.views.del_producto', name='del_producto'),
   # urls-proveedor
    url(r'^proveedor/$', 'control_inventario.views.proveedor', name='proveedor'),
    url(r'^proveedor/del$', 'control_inventario.views.del_proveedor', name='del_proveedor'),
   # urls-proveedor
    url(r'^cliente/$', 'control_inventario.views.cliente', name='cliente'),
    url(r'^cliente/del$', 'control_inventario.views.del_cliente', name='del_cliente'),
   # urls-inventario inicial
    url(r'^inventario/$', 'control_inventario.views.inventario_inicial', name='inventario'),
   # urls-salida de mercancia
    url(r'^salida/$', 'control_inventario.views.salida_mercancia', name='salida_mercancia'),
    url(r'^salida/add$', 'control_inventario.views.add_salida_mercancia', name='add_salida_mercancia'),
    url(r'^salida/detalles$', 'control_inventario.views.detalle_venta', name='detalle_venta'),
   # urls-entrada de mercancia
    url(r'^entrada/$', 'control_inventario.views.entrada_mercancia', name='entrada_mercancia'),
    url(r'^entrada/add$', 'control_inventario.views.add_entrada_mercancia', name='add_entrada_mercancia'),
    url(r'^entrada/detalles$', 'control_inventario.views.detalle_compra', name='detalle_venta'),
   # urls-registo de ventas
    url(r'^registro-ventas/$', 'control_inventario.views.registro_ventas', name='registro_ventas'),
   # exportar a excel
   #  url(r'^export/$', 'control_inventario.views.export', name='export'),



    url(r'^admin/', include(admin.site.urls)),
)
