# _*_ coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from control_inventario import models
from django.contrib.auth.decorators import login_required

from control_inventario.app.export.pdf import PdfPrint
from reportlab.lib import colors
from XlsxWriter import xlsxwriter
import io


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
        elif int(periodo) == 4:
            rango["ini"] = 10
            rango["fin"] = 13
            meses = ["Octubre", "Noviembre", "Diciembre"]
        args["meses"] = meses

        mov_list = {}
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
                mov_list[id_prod][mes] = get_hist_prod_mes(id_prod, i, emp, year)
                if mov_list[id_prod][mes]["saldo_inicial"] == 0:
                    if mes > 0:
                        mov_list[id_prod][mes]["saldo_inicial"] = mov_list[id_prod][mes - 1]["saldo_final"]
                        mov_list[id_prod][mes]["saldo_final"] = mov_list[id_prod][mes - 1]["saldo_final"]
                mes += 1

        args['movimientos'] = mov_list
        request.session["movimientos"] = {
            "mov_list": mov_list,
            "meses": meses,
            "year": year
        }

    args['form'] = form
    return render_to_response('resumen_movimientos_prod/main.html', args, context_instance=RequestContext(request))


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


def loadDataExcel(emp, data):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    meses = data.get("meses")
    mov_list = data.get("mov_list")
    year = data.get("year")
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
        'border': 2
    })

    cell_format = workbook.add_format({
        'align': 'center',
        'color': 'black',
        'border': 1
    })

    cell_format_left = workbook.add_format({
        'align': 'left',
        'color': 'black',
        'border': 1
    })

    ruc = "RUC: " + str(emp.ruc)
    empresa = "Denominacion: " + emp.nombre
    titulo = "Resumen de saldos y movimientos desde el mes de " + meses[0] + " hasta " + meses[2] + " del año " + year
    # merges
    worksheet.merge_range('A1:G1', ruc, top_title)
    worksheet.merge_range('H1:O1', empresa, top_title)
    worksheet.merge_range('A3:O3', titulo, title)
    worksheet.merge_range('A5:A6', "#", header)
    worksheet.merge_range('B5:B6', "Codigo", header)
    worksheet.merge_range('C5:C6', "Nombre", header)
    worksheet.merge_range('D5:G5', meses[0], header)
    worksheet.merge_range('H5:K5', meses[1], header)
    worksheet.merge_range('L5:O5', meses[2], header)


    # encabezados
    worksheet.write(5, 3, "Sal. Ini.", header)
    worksheet.write(5, 4, "Entrada", header)
    worksheet.write(5, 5, "Salida", header)
    worksheet.write(5, 6, "Saldo", header)
    worksheet.write(5, 7, "Sal. Ini.", header)
    worksheet.write(5, 8, "Entrada", header)
    worksheet.write(5, 9, "Salida", header)
    worksheet.write(5, 10, "Saldo", header)
    worksheet.write(5, 11, "Sal. Ini.", header)
    worksheet.write(5, 12, "Entrada", header)
    worksheet.write(5, 13, "Salida", header)
    worksheet.write(5, 14, "Saldo", header)
    # datos
    idx = 1
    row = 6
    for key in mov_list:
        fila = mov_list[key]
        worksheet.write_number(row, 0, idx, cell_format)
        worksheet.write(row, 1, fila.get("codigo"), cell_format_left)
        worksheet.write(row, 2, fila.get("nombre"), cell_format_left)
        worksheet.write(row, 3, fila.get("0").get("saldo_inicial"), cell_format)
        worksheet.write(row, 4, fila.get("0").get("entradas"), cell_format)
        worksheet.write(row, 5, fila.get("0").get("salidas"), cell_format)
        worksheet.write(row, 6, fila.get("0").get("saldo_final"), cell_format)
        worksheet.write(row, 7, fila.get("1").get("saldo_inicial"), cell_format)
        worksheet.write(row, 8, fila.get("1").get("entradas"), cell_format)
        worksheet.write(row, 9, fila.get("1").get("salidas"), cell_format)
        worksheet.write(row, 10, fila.get("1").get("saldo_final"), cell_format)
        worksheet.write(row, 11, fila.get("2").get("saldo_inicial"), cell_format)
        worksheet.write(row, 12, fila.get("2").get("entradas"), cell_format)
        worksheet.write(row, 13, fila.get("2").get("salidas"), cell_format)
        worksheet.write(row, 14, fila.get("2").get("saldo_final"), cell_format)
        row += 1
        idx += 1

    # resizing columns
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


def export_excel(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    data = request.session["movimientos"]
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report'

    xlsx_data = loadDataExcel(emp, data)

    response.write(xlsx_data)
    return response


def loadDataPDF(emp, datos):
    producto_list = emp.producto_set.values()

    meses = datos.get("meses")
    mov_list = datos.get("mov_list")
    year = datos.get("year")
    titulo = "Resumen de saldos y movimientos desde el mes de " + meses[0] + " hasta " + meses[2] + " del año " + year

    data_pdf = {
        "headings": [("Codigo", "Nombre", meses[0],"","","", meses[1],"","","", meses[2],"","",""),
                     ("", "", "Sal. Ini.","Entradas","Salidas","Saldo", "Sal. Ini.","Entradas","Salidas","Saldo", "Sal. Ini.","Entradas","Salidas","Saldo")],
        "data": [],
        "title": titulo,
        "ruc": "<b>RUC: </b>",
        "empresa": "<b>Denominacion: </b>",
    }

    table_style = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.black),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 1), colors.whitesmoke),
        ('ALIGN',(0,0),(-1,0),'CENTER'),
        ('FONTSIZE', (0, 0), (-1, -1), 7),
        ('SPAN', (0, 0), (0, 1)),
        ('SPAN', (1, 0), (1, 1)),
        ('SPAN', (2, 0), (5, 0)),
        ('SPAN', (6, 0), (9, 0)),
        ('SPAN', (10, 0), (13, 0)),
    ]
    data_pdf["table_style"] = table_style

    for prod in mov_list:
        fila = mov_list[prod]
        aux = [
            fila.get("codigo"),
            fila.get("nombre"),
            fila.get("0").get("saldo_inicial"),
            fila.get("0").get("entradas"),
            fila.get("0").get("salidas"),
            fila.get("0").get("saldo_final"),
            fila.get("1").get("saldo_inicial"),
            fila.get("1").get("entradas"),
            fila.get("1").get("salidas"),
            fila.get("1").get("saldo_final"),
            fila.get("2").get("saldo_inicial"),
            fila.get("2").get("entradas"),
            fila.get("2").get("salidas"),
            fila.get("2").get("saldo_final"),
        ]
        data_pdf["data"].append(aux)
    return data_pdf


def export_pdf(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)

    datos = request.session["movimientos"]

    data = loadDataPDF(emp, datos)
    data["ruc"] += str(emp.ruc)
    data["empresa"] += emp.nombre

    response = HttpResponse(content_type='application/pdf')
    filename = data.get("title")
    response['Content-Disposition'] = 'attachement; filename=' + filename
    buffer = io.BytesIO()
    pdf = PdfPrint(buffer, 'A4')
    pdf = pdf.generar_pdf(data)
    response.write(pdf)
    return response
