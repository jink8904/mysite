from builtins import print
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
# from django.http import HttpResponseRedirect, HttpResponse
from control_inventario import models
from django.contrib.auth.decorators import login_required

@login_required(login_url='/ingresar')
def stock_disponible(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    producto_list = emp.producto_set.values()
    producto_list=producto_list.order_by("inventario")
    for prod in producto_list:
        print(prod)
        stock_disp = emp.inventario_set.get(producto_id=prod.get("id")).cantidad
        categoria = emp.categoria_set.get(id=prod.get("categoria_id")).denominacion
        tipo = models.TipoProducto.objects.get(id=prod.get("tipo_id")).denominacion
        unidad = models.UnidadProducto.objects.get(id=prod.get("unidad_id")).denominacion
        prod["stock_disp"] = stock_disp
        prod["categoria"] = categoria
        prod["tipo"] = tipo
        prod["unidad"] = unidad
    args = {}
    args["producto_list"] = producto_list
    return render_to_response('stock_disponible/main.html', args, context_instance=RequestContext(request))
