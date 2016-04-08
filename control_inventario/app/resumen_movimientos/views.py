# _*_ coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from control_inventario import models
from django.contrib.auth.decorators import login_required

from control_inventario.app.export.pdf import PdfPrint
from XlsxWriter import xlsxwriter
import io


@login_required(login_url='/ingresar')
def resumen_mov(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    producto_list = emp.producto_set
    mes = request.session.get("mes")
    year = request.session.get("empresa").get("anno_inicio")
    mes_list = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
                "octubre", "noviembre", "diciembre"]
    mov_list = []
    for producto in producto_list.values():
        id_prod = producto.get("id")
        movs = get_hist_prod_mes(id_prod, mes, emp, year)
        movs["id"] = producto.get("id")
        movs["nombre"] = producto.get("nombre")
        movs["codigo"] = producto.get("codigo")
        mov_list.append(movs)

    args = {}
    args["mov_list"] = mov_list
    args["mes"] = mes_list[int(mes) - 1]
    return render_to_response('resumen_movimientos/main.html', args, context_instance=RequestContext(request))


def resumen_mov_local(datos):
    emp = datos.get("emp")

    producto_list = emp.producto_set
    mes = datos.get("mes")
    year = datos.get("year")
    mes_list = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre",
                "octubre", "noviembre", "diciembre"]
    mov_list = []
    for producto in producto_list.values():
        id_prod = producto.get("id")
        movs = get_hist_prod_mes(id_prod, mes, emp, year)
        movs["id"] = producto.get("id")
        movs["nombre"] = producto.get("nombre")
        movs["codigo"] = producto.get("codigo")
        mov_list.append(movs)

    args = {}
    args["mov_list"] = mov_list
    args["mes"] = mes_list[int(mes) - 1]
    return args


def get_hist_prod_mes(id_prod, mes, emp, year):
    saldo_inicial = 0
    saldo_final = 0
    entradas = 0
    salidas = 0

    hist_list = emp.inventariohist_set.filter(producto_id=id_prod)
    hist_list = hist_list.filter(fecha_operacion__year=year)
    hist_list_mes = hist_list.filter(fecha_operacion__month=mes)

    if (hist_list_mes):
        hist_list_mes = hist_list_mes.order_by("id")
        if (hist_list_mes[0].tipo_operacion == "entrada"):
            saldo_inicial = hist_list_mes[0].cantidad_final - hist_list_mes[0].cantidad
        elif (hist_list_mes[0].tipo_operacion == "salida"):
            saldo_inicial = hist_list_mes[0].cantidad_final + hist_list_mes[0].cantidad
        elif (hist_list_mes[0].tipo_operacion == "inv_inicial"):
            saldo_inicial = hist_list_mes[0].cantidad_final
        for hist in hist_list_mes:
            if (hist.tipo_operacion == "entrada"):
                entradas += hist.cantidad
            elif (hist.tipo_operacion == "salida"):
                salidas += hist.cantidad
        saldo_final = saldo_inicial + entradas - salidas
    else:
        date = str(year) + "-" + str(mes) + "-1"
        hist_list_after = hist_list.filter(fecha_operacion__lt=date)
        # hist_list_after = hist_list_after.order_by("-id")
        if (hist_list_after):
            print(id_prod)
            print(mes)
            print(hist_list_after.values())

    result = {
        "saldo_inicial": saldo_inicial,
        "salidas": salidas,
        "entradas": entradas,
        "saldo_final": saldo_final,
    }
    return result


def loadDataExcel(datos):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    movs_data = resumen_mov_local(datos)
    mov_list = movs_data.get("mov_list")
    emp = datos.get("emp")
    # Here we will adding the code to add data
    worksheet = workbook.add_worksheet("Resumen de movimientos")
    # formatos
    title = workbook.add_format({
        'bold': True,
        'font_size': 14,
        'align': 'center',
        'valign': 'vcenter'
    })
    top_title = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'align': 'left',
        'valign': 'vleft'
    })
    header = workbook.add_format({
        'bg_color': '#F7F7F7',
        'color': 'black',
        'align': 'center',
        'valign': 'top',
        'border': 1
    })

    cell_format = workbook.add_format({
        'align': 'center',
        'color': 'black',
    })

    ruc = "RUC: " + str(emp.ruc)
    empresa = "Denominación: " + emp.nombre
    titulo = "Resumen de saldos y movimientos del mes de " + movs_data.get("mes")
    worksheet.merge_range('A1:D1', ruc, top_title)
    worksheet.merge_range('E1:G1', empresa, top_title)
    worksheet.merge_range('B3:G3', titulo, title)
    # encabezados
    worksheet.write(4, 0, "#", header)
    worksheet.write(4, 1, "Código", header)
    worksheet.write(4, 2, "Nombre", header)
    worksheet.write(4, 3, "Saldo inicial", header)
    worksheet.write(4, 4, "Entradas", header)
    worksheet.write(4, 5, "Salidas", header)
    worksheet.write(4, 6, "Saldo final", header)
    # datos
    idx = 1
    row = 5
    for mov in mov_list:
        worksheet.write_number(row, 0, idx)
        worksheet.write(row, 1, mov.get("codigo"), cell_format)
        worksheet.write(row, 2, mov.get("nombre"), cell_format)
        worksheet.write(row, 3, mov.get("saldo_inicial"), cell_format)
        worksheet.write(row, 4, mov.get("entradas"), cell_format)
        worksheet.write(row, 5, mov.get("salidas"), cell_format)
        worksheet.write(row, 6, mov.get("saldo_final"), cell_format)
        row += 1
        idx += 1

    # resizing columns
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 15)

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


def export_excel(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    datos = {}
    datos["emp"] = emp
    datos["mes"] = request.session.get("mes")
    datos["year"] = request.session.get("empresa").get("anno_inicio")

    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report'

    xlsx_data = loadDataExcel(datos)

    response.write(xlsx_data)
    return response


def loadDataPDF(datos):
    movs_data = resumen_mov_local(datos)
    mov_list = movs_data.get("mov_list")
    mes = movs_data.get("mes")
    emp = datos.get("emp")

    data_pdf = {
        "headings": [("Codigo", "Nombre", "Saldo inicial", "Entradas", "Salidas", "Saldo final")],
        "data": [],
        "title": "Resumen de saldos y movimientos del mes de " + mes,
        "ruc": "<b>RUC: </b>",
        "empresa": "<b>Denominación: </b>",
    }
    for mov in mov_list:
        aux = [
            mov.get("codigo"),
            mov.get("nombre"),
            mov.get("saldo_inicial"),
            mov.get("entradas"),
            mov.get("salidas"),
            mov.get("saldo_final"),
        ]
        data_pdf["data"].append(aux)
    return data_pdf


def export_pdf(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    datos = {}
    datos["emp"] = emp
    datos["mes"] = request.session.get("mes")
    datos["year"] = request.session.get("empresa").get("anno_inicio")

    pdf_data = loadDataPDF(datos)
    pdf_data["ruc"] += str(emp.ruc)
    pdf_data["empresa"] += emp.nombre

    response = HttpResponse(content_type='application/pdf')
    filename = pdf_data.get("title")
    response['Content-Disposition'] = 'attachement; filename=' + filename
    buffer = io.BytesIO()
    pdf = PdfPrint(buffer, 'A4')
    pdf = pdf.generar_pdf(pdf_data)
    response.write(pdf)
    return response
