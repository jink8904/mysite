from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.context_processors import csrf
from control_inventario import forms, models
from django.contrib.auth.decorators import login_required
import json


def list_cliente(cliente_list):
    for cliente in cliente_list:
        cliente["tipo_id"] = models.TipoId.objects.get(id=cliente.get("tipo_id_id"))
    return cliente_list


@login_required(login_url='/ingresar')
def reporte_cliente(request, tipo):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    args = {}
    args["tipo"] = tipo

    cliente_list = emp.cliente_set.values()
    cliente_list = list_cliente(cliente_list)

    args["form"] = True
    args["cliente_list"] = cliente_list
    datos = request.POST
    det_venta_list = []
    if (datos):
        args["form"] = False
        fecha = datos.get("fecha")
        id = datos.get("identificador")
        args["cliente"] = emp.cliente_set.get(id=id).nombre

        if (tipo == "diario"):
            venta_list = emp.venta_set.filter(fecha=fecha)
            venta_list = venta_list.filter(cliente_id=id)

        for venta in venta_list.values():
            comp_id = venta.get("tipo_comprobante_id")
            venta["comprobante"] = models.TipoComprobante.objects.get(id=comp_id).denominacion
            det_list = get_detalle_venta_diario(venta)
            det_venta_list += det_list
    print(det_venta_list)
    args["det_venta_list"] = det_venta_list
    return render_to_response('reportes_cliente/main.html', args, context_instance=RequestContext(request))


def get_detalle_venta_diario(venta):
    id = venta.get("id")
    det_list = models.DetalleVenta.objects.filter(venta_id=id).values()
    for det in det_list:
        det["serie"] = venta.get("serie")
        det["numero"] = venta.get("numero")
        det["fecha"] = venta.get("fecha")
        det["tipo"] = venta.get("comprobante")

        prod = models.Producto.objects.get(id=det.get("producto_id"))
        det["codigo"] = prod.codigo
        det["producto"] = prod.nombre

    return det_list
