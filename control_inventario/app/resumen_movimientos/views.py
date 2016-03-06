from django.shortcuts import render_to_response
from django.template import RequestContext
from control_inventario import models
from django.contrib.auth.decorators import login_required

@login_required(login_url='/ingresar')
def resumen_mov(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    args = {}
    form = True
    detalle_venta_list = {}
    datos = request.POST
    if datos:
        year = datos.get("year")
        args["year"] = year
        periodo = datos.get("periodo")
        rango = {"ini": 1, "fin": 5}
        meses = ["Enero", "Febrero", "Marzo", "Abril"]
        if periodo == 2:
            rango["ini"] = 5
            rango["fin"] = 9
            meses = ["Mayo", "Junio", "Julio", "Agosto"]
        elif periodo == 3:
            rango["ini"] = 9
            rango["fin"] = 13
            meses = ["Septiembre", "Ocyubre", "Noviembre", "Diciembre"]
        args["meses"] = meses

        form = False
        for mes in range(rango["ini"], rango["fin"]):
            ventas = emp.venta_set.filter(fecha__year=year, fecha__month=mes)
            if ventas:
                for venta in ventas:
                    detalle_v = venta.detalleventa_set.values()
                    detalle_venta_list[mes] = detalle_v
    args['form'] = form
    args['detalle_venta_list'] = detalle_venta_list
    return render_to_response('resumen_movimientos/main.html', args, context_instance=RequestContext(request))