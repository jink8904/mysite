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

    datos = request.POST
    if datos:
        form = False
        year = datos.get("year")
        args["year"] = year
        periodo = datos.get("periodo")
        rango = {"ini": 1, "fin": 4}
        meses = ["Enero", "Febrero", "Marzo"]
        if int(periodo) == 2:
            rango["ini"] = 4
            rango["fin"] = 7
            meses = ["Abril", "Mayo", "Junio"]
        elif int(periodo) == 3:
            rango["ini"] = 7
            rango["fin"] = 10
            meses = ["Julio", "Agosto", "Septiembre"]
        elif int(periodo) == 3:
            rango["ini"] = 10
            rango["fin"] = 13
            meses = ["Octubre", "Noviembre", "Diciembre"]
        args["meses"] = meses

        mov_list = {}
        prod_list = {}
        productos_list = emp.producto_set.values()
        for prod in productos_list:
            id_prod = prod.get("id")
            nombre = prod.get("nombre")
            codigo = prod.get("codigo")
            mov_list[id_prod] = {}
            mov_list[id_prod]["codigo"] = codigo
            mov_list[id_prod]["nombre"] = nombre
            mes = 0
            for i in range(rango["ini"], rango["fin"]):
                mov_list[id_prod][mes] = get_hist_prod_mes(id_prod, i, emp)
                if mov_list[id_prod][mes]["saldo_inicial"] == 0:
                    if mes > 0:
                        mov_list[id_prod][mes]["saldo_inicial"] = mov_list[id_prod][mes - 1]["saldo_final"]
                        mov_list[id_prod][mes]["saldo_final"] = mov_list[id_prod][mes - 1]["saldo_final"]
                    # else:

                mes += 1

        args['movimientos'] = mov_list

    args['form'] = form
    return render_to_response('resumen_movimientos/main.html', args, context_instance=RequestContext(request))


def get_hist_prod_mes(id_prod, mes, emp):
    saldo_inicial = 0
    saldo_final = 0
    entradas = 0
    salidas = 0

    hist_list = emp.inventariohist_set.filter(producto_id=id_prod)
    hist_list = hist_list.filter(fecha_operacion__month=mes)
    if (hist_list):
        hist_list = hist_list.order_by("id")
        if (hist_list[0].tipo_operacion == "entrada"):
            saldo_inicial = hist_list[0].cantidad_final - hist_list[0].cantidad
        elif (hist_list[0].tipo_operacion == "salida"):
            saldo_inicial = hist_list[0].cantidad_final + hist_list[0].cantidad
        for hist in hist_list:
            if (hist.tipo_operacion == "entrada"):
                entradas += hist.cantidad
            elif (hist.tipo_operacion == "salida"):
                salidas += hist.cantidad
        saldo_final = saldo_inicial + entradas - salidas

    result = {
        "saldo_inicial": saldo_inicial,
        "salidas": salidas,
        "entradas": entradas,
        "saldo_final": saldo_final,
    }
    return result
