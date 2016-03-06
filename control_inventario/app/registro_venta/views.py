from django.shortcuts import render_to_response
from django.template import RequestContext
from control_inventario import models
from django.contrib.auth.decorators import login_required


@login_required(login_url='/ingresar')
def registro_ventas(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    estadoPLE_list = models.EstadoPLE.objects.values()
    comprobante_list = models.TipoComprobante.objects.values()
    cliente_list = emp.cliente_set.values()

    args = {}
    args['estadoPLE_list'] = estadoPLE_list
    args['cliente_list'] = cliente_list
    args['comprobante_list'] = comprobante_list
    return render_to_response('registro_ventas/main.html', args, context_instance=RequestContext(request))
