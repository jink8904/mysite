from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from control_inventario import models
import json

from django.contrib.auth.decorators import login_required


def update_compra_list(emp):
    compra_list = emp.compra_set.values().order_by("fecha")
    for compra in compra_list:
        compra['tipo_comprobante'] = models.TipoComprobante.objects.get(id=compra["tipo_comprobante_id"]).denominacion
        compra['proveedor'] = models.Proveedor.objects.get(id=compra["proveedor_id"]).nombre
    return compra_list


@login_required(login_url='/ingresar')
def resumen_compra(request):
    id_empresa = request.session['empresa']["id"]
    mes = request.session["mes"]
    emp = models.Empresa.objects.get(id=id_empresa)

    comprobante_list = models.TipoComprobante.objects.values()
    cliente_list = emp.cliente_set.values()
    compra_list = update_compra_list(emp)
    tipo_operacion_list = models.TipoOperacion.objects.values()

    args = {}
    args["comprobante_list"] = comprobante_list
    args["cliente_list"] = cliente_list
    args["compra_list"] = compra_list
    args["tipo_operacion_list"] = tipo_operacion_list
    return render_to_response('resumen_compras/main.html', args, context_instance=RequestContext(request))

def detalle_compra(request):
    datos = request.POST
    d_list = []
    if datos:
        id_compra = datos.get("id_compra")
        detalles_list = models.DetalleCompra.objects.filter(compra_id=id_compra).values()
        for i in detalles_list:
            i["valor_unitario"] = float(i['valor_unitario'])
            i["importe"] = float(i['importe'])
            i["igv"] = float(i['igv'])
            i["valor_venta"] = float(i['valor_venta'])
            prod = models.Producto.objects.get(id=i['producto_id'])
            i['codigo'] = prod.codigo
            d_list.append(i)

    args = {}
    args['d_list'] = d_list
    args['success'] = True
    json_data = json.dumps(args)
    return HttpResponse(json_data, mimetype="application/json")
