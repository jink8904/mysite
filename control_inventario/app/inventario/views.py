from builtins import print
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import models
import datetime

# ------------ Inventario ------------
def list_p_inv(producto_list):
    for prod in producto_list:
        prod["categoria"] = models.Categoria.objects.get(id=prod.get("categoria_id"))
        prod["tipo"] = models.TipoProducto.objects.get(id=prod.get("tipo_id"))
        prod["unidad"] = models.UnidadProducto.objects.get(id=prod.get("unidad_id"))
        inv = models.Inventario.objects.get(producto=prod.get("id"))
        prod["cantidad"] = inv.cantidad
        prod["costo_unitario"] = inv.costo_unitario
        prod["costo_total"] = inv.costo_unitario * inv.cantidad
    return producto_list;


def inventario_inicial(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    p = emp.producto_set.values()
    args = {}

    datos = request.POST
    if datos:
        if datos.get("id"):
            inv = emp.inventario_set.get(producto=datos.get("id"))
            inv.cantidad = datos.get("cantidad")
            inv.costo_unitario = datos.get("costo_unitario")
            inv.save()
            #salvar hiatorico
            inv_hist = models.InventarioHist(
                fecha_real=datetime.datetime.now(),
                fecha_operacion=datetime.datetime.now(),
                tipo_operacion="inv_inicial",
                cantidad=inv.cantidad,
                cantidad_final=inv.cantidad,
                producto=emp.producto_set.get(id=datos.get("id")),
                empresa=emp
            )
            inv_hist.save()

    producto_list = list_p_inv(p)
    args.update(csrf(request))
    args["productos"] = producto_list

    return render_to_response('inventario_inicial/main.html', args, context_instance=RequestContext(request))
