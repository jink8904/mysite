# _*_ coding: utf-8
from django.shortcuts import render_to_response
from django.template import RequestContext
from control_inventario import models
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from control_inventario.app.export.pdf import PdfPrint
from XlsxWriter import xlsxwriter
from reportlab.lib import colors
import io


def list_proveedor(proveedor_list):
    for proveedor in proveedor_list:
        proveedor["tipo_id"] = models.TipoId.objects.get(id=proveedor.get("tipo_id_id"))
    return proveedor_list


def getMonth(mes):
    meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Ocyubre",
             "Noviembre", "Diciembre"]
    return meses[mes - 1]


@login_required(login_url='/ingresar')
def reporte_proveedor(request, tipo):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    args = {}
    args["tipo"] = tipo

    proveedor_list = emp.proveedor_set.values()
    proveedor_list = list_proveedor(proveedor_list)

    args["form"] = True
    args["proveedor_list"] = proveedor_list
    datos = request.POST
    det_compra_list = []
    if (datos):
        args["form"] = False
        id = datos.get("identificador")
        request.session["reporte_proveedor"] = {"proveedor_id": id}
        proveedor = emp.proveedor_set.get(id=id)
        args["proveedor"] = {  "nombre": proveedor.nombre, "id": proveedor.identificador}
        report_title = "Reporte de compras "

        if (tipo == "diario"):
            fecha = datos.get("fecha")
            date = fecha.split("-")
            dia = int(date[2])
            mes = getMonth(int(date[1]))
            report_title += "del dia " + str(dia) + " de " + mes.lower() + " del año " + date[0]
            request.session["reporte_proveedor"]["tipo"] = "diario"
            request.session["reporte_proveedor"]["fecha"] = fecha

            compra_list = emp.compra_set.filter(fecha=fecha)
            compra_list = compra_list.filter(proveedor_id=id)
        elif (tipo == "mensual"):
            mes = int(datos.get("mes"))
            year = request.session['empresa']["anno_inicio"]
            report_title += "de " + getMonth(mes).lower() + " del " + str(year)

            request.session["reporte_proveedor"]["tipo"] = "mensual"
            request.session["reporte_proveedor"]["mes"] = mes
            request.session["reporte_proveedor"]["year"] = year

            compra_list = emp.compra_set.filter(fecha__month=mes)
            compra_list = compra_list.filter(fecha__year=year)
            compra_list = compra_list.filter(proveedor_id=id)
        elif (tipo == "anual"):
            year = datos.get("year")
            request.session["reporte_proveedor"]["tipo"] = "anual"
            request.session["reporte_proveedor"]["year"] = year
            report_title += "del año " + year
            compra_list = emp.compra_set.filter(fecha__year=year)
            compra_list = compra_list.filter(proveedor_id=id)

        for compra in compra_list.values():
            comp_id = compra.get("tipo_comprobante_id")
            compra["comprobante"] = models.TipoComprobante.objects.get(id=comp_id).denominacion
            det_list = get_detalle_compra(compra)
            det_compra_list += det_list
    if det_compra_list.__len__() == 0:
        args["empty"] = True
    else:
        args["det_compra_list"] = det_compra_list
        args["total"] = get_total(det_compra_list)
        args["report_title"] = report_title

    return render_to_response('reportes_proveedor/main.html', args, context_instance=RequestContext(request))


def reporte_proveedor_local(datos):
    emp = datos.get("emp")
    args = {}
    args["tipo"] = datos.get("tipo")

    id = datos.get("proveedor_id")
    proveedor = emp.proveedor_set.get(id=id)
    args["proveedor"] = {"nombre": proveedor.nombre, "id": proveedor.identificador}

    det_compra_list = []
    if (datos):
        tipo = datos.get("tipo")
        proveedor = emp.proveedor_set.get(id=id)
        args["proveedor"] = {"nombre": proveedor.nombre, "id": proveedor.identificador}
        report_title = "Reporte de compras "
        if (tipo == "diario"):
            fecha = datos.get("fecha")
            date = fecha.split("-")
            dia = int(date[2])
            mes = getMonth(int(date[1]))
            report_title += "del dia " + str(dia) + " de " + mes.lower() + " del año " + date[0]

            compra_list = emp.compra_set.filter(fecha=fecha)
            compra_list = compra_list.filter(proveedor_id=id)
        elif (tipo == "mensual"):
            mes = datos.get("mes")
            year = datos.get("year")
            report_title += "de " + getMonth(mes).lower() + " del " + str(year)

            compra_list = emp.compra_set.filter(fecha__month=mes)
            compra_list = compra_list.filter(fecha__year=year)
            compra_list = compra_list.filter(proveedor_id=id)
        elif (tipo == "anual"):
            year = datos.get("year")
            report_title += "del año " + year
            compra_list = emp.compra_set.filter(fecha__year=year)
            compra_list = compra_list.filter(proveedor_id=id)

        for compra in compra_list.values():
            comp_id = compra.get("tipo_comprobante_id")
            compra["comprobante"] = models.TipoComprobante.objects.get(id=comp_id).denominacion
            det_list = get_detalle_compra(compra)
            det_compra_list += det_list

    args["det_compra_list"] = det_compra_list
    args["total"] = get_total(det_compra_list)
    args["report_title"] = report_title
    return args


def get_detalle_compra(compra):
    id = compra.get("id")
    det_list = models.DetalleCompra.objects.filter(compra_id=id).values()
    for det in det_list:
        det["serie"] = compra.get("serie")
        det["numero"] = compra.get("numero")
        det["fecha"] = compra.get("fecha")
        det["tipo"] = compra.get("comprobante")

        prod = models.Producto.objects.get(id=det.get("producto_id"))
        det["codigo"] = prod.codigo
        det["producto"] = prod.nombre

    return det_list


def get_total(detalle_list):
    total = {
        "cantidad": 0,
        "valor_unitario": 0,
        "valor_venta": 0,
        "igv": 0,
        "importe": 0,
    }
    for det in detalle_list:
        total["cantidad"] += det.get("cantidad")
        total["valor_unitario"] += det.get("valor_unitario")
        total["valor_venta"] += det.get("valor_venta")
        total["igv"] += det.get("igv")
        total["importe"] += det.get("importe")
    return total


def loadDataExcel(emp, datos):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    datos["emp"] = emp
    args = reporte_proveedor_local(datos)
    detalles_list = args.get("det_compra_list")
    total = args.get("total")
    # Here we will adding the code to add data
    worksheet = workbook.add_worksheet("Reporte de proveedor")
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
        'valign': 'center',
        'border': 1
    })

    cell_format = workbook.add_format({
        'align': 'center',
        'color': 'black',
    })

    cell_total_format = workbook.add_format({
        'align': 'right',
        'color': 'black',
    })

    cell_date_format = workbook.add_format({
        'align': 'center',
        'color': 'black',
        'num_format': 'yyyy-mm-dd',
    })

    ruc = "RUC: " + str(emp.ruc)
    empresa = "Denominación: " + emp.nombre
    report_title = args.get("report_title")
    report_subtitle = "Detalles de compra al proveedor:"
    proveedor = args.get("proveedor")
    client_dni = "R.U.C / D.N.I: " + str(proveedor.get("id"))
    client_name = "Nombre o razón social: " + proveedor.get("nombre")

    worksheet.merge_range('B1:F1', ruc, top_title)
    worksheet.merge_range('G1:L1', empresa, top_title)
    worksheet.merge_range('A2:L2', "", "")
    worksheet.merge_range('A3:L3', report_title, title)
    worksheet.merge_range('B4:L4', report_subtitle, top_title)
    worksheet.merge_range('B5:F5', client_dni, top_title)
    worksheet.merge_range('G5:L5', client_name, top_title)
    # encabezados
    worksheet.write(5, 0, "#", header)
    worksheet.write(5, 1, "Fecha", header)
    worksheet.write(5, 2, "Tipo", header)
    worksheet.write(5, 3, "Serie", header)
    worksheet.write(5, 4, "Número", header)
    worksheet.write(5, 5, "Código", header)
    worksheet.write(5, 6, "Descripción", header)
    worksheet.write(5, 7, "Cantidad", header)
    worksheet.write(5, 8, "Valor unitario", header)
    worksheet.write(5, 9, "Valor compra", header)
    worksheet.write(5, 10, "IGV", header)
    worksheet.write(5, 11, "Precio compra", header)
    # datos
    idx = 1
    row = 6
    for det in detalles_list:
        worksheet.write_number(row, 0, idx)
        worksheet.write_datetime(row, 1, det.get("fecha"), cell_date_format)
        worksheet.write(row, 2, det.get("tipo"), cell_format)
        worksheet.write(row, 3, det.get("serie"), cell_format)
        worksheet.write(row, 4, det.get("numero"), cell_format)
        worksheet.write(row, 5, det.get("codigo"), cell_format)
        worksheet.write(row, 6, det.get("descripcion"), cell_format)
        worksheet.write(row, 7, det.get("cantidad"), cell_format)
        worksheet.write(row, 8, det.get("valor_unitario"), cell_format)
        worksheet.write(row, 9, det.get("valor_venta"), cell_format)
        worksheet.write(row, 10, det.get("igv"), cell_format)
        worksheet.write(row, 11, det.get("importe"), cell_format)
        row += 1
        idx += 1
    worksheet.merge_range('B' + str(row + 1) + ':G' + str(row + 1), "Total  ", cell_total_format)
    worksheet.write(row, 7, total.get("cantidad"), cell_format)
    worksheet.write(row, 8, total.get("valor_unitario"), cell_format)
    worksheet.write(row, 9, total.get("valor_venta"), cell_format)
    worksheet.write(row, 10, total.get("igv"), cell_format)
    worksheet.write(row, 11, total.get("importe"), cell_format)

    # resizing columns
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 30)
    worksheet.set_column('D:D', 15)
    worksheet.set_column('E:E', 15)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 30)
    worksheet.set_column('H:H', 15)
    worksheet.set_column('I:I', 15)
    worksheet.set_column('J:J', 15)
    worksheet.set_column('L:L', 15)

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


def export_excel(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    datos = request.session["reporte_proveedor"]
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report'

    xlsx_data = loadDataExcel(emp, datos)

    response.write(xlsx_data)
    return response


def loadDataPDF(datos):
    args = reporte_proveedor_local(datos)
    title = args["report_title"]
    detalles_list = args.get("det_compra_list")
    total = args["total"]
    total = ["Total", "", "", "", "", "",total.get("cantidad"), total.get("valor_unitario"),
             total.get("valor_venta"), total.get("igv"), total.get("importe"),]

    data_pdf = {
        "headings": [("Fecha", "Tipo", "Serie", "Número", "Código", "Descripción", "Cantidad",
                      "Valor unitario", "Valor compra", "IGV", "Precio compra")],
        "data": [],
        "title": title,
        "ruc": "<b>RUC: </b>",
        "empresa": "<b>Denominación: </b>",
    }
    for det in detalles_list:
        aux = [
            det.get("fecha"),
            det.get("tipo"),
            det.get("serie"),
            det.get("numero"),
            det.get("codigo"),
            det.get("descripcion"),
            det.get("cantidad"),
            det.get("valor_unitario"),
            det.get("valor_venta"),
            det.get("igv"),
            det.get("importe"),
        ]
        data_pdf["data"].append(aux)
    data_pdf["data"].append(total)

    data_pdf["table_style"] = [
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
        ('BOX', (0, 0), (-1, -1), 0.75, colors.black),
        ('VALIGN', (0, 0), (-1, 0), 'MIDDLE'),
        ('BACKGROUND', (0, 0), (-1, 0), colors.whitesmoke),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('SIZE', (0, 0), (-1, -1), 7),
        ('SPAN', (0, -1), (5, -1)),
        ('ALIGN',(0, -1), (5, -1),'RIGHT'),
    ]

    id = args.get("proveedor").get("id")
    nombre = args.get("proveedor").get("nombre")
    datos_proveedor = "<b>R.U.C / D.N.I:</b> " + str(id)
    datos_proveedor += "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"
    datos_proveedor += "<b>Proveedor:</b> " + nombre
    data_pdf["more_text"] = ["<b>Detalles de compra al proveedor:</b>", datos_proveedor]

    return data_pdf


def export_pdf(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    datos = request.session["reporte_proveedor"]
    datos["emp"] = emp

    data = loadDataPDF(datos)
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
