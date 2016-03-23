from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from control_inventario import models
from control_inventario.app.export.pdf import PdfPrint
from django.contrib.auth.decorators import login_required
from XlsxWriter import xlsxwriter
import io


def productos_list_updated(emp):
    producto_list = emp.producto_set.values()
    producto_list = producto_list.order_by("inventario")
    for prod in producto_list:
        stock_disp = emp.inventario_set.get(producto_id=prod.get("id")).cantidad
        categoria = emp.categoria_set.get(id=prod.get("categoria_id")).denominacion
        tipo = models.TipoProducto.objects.get(id=prod.get("tipo_id")).denominacion
        unidad = models.UnidadProducto.objects.get(id=prod.get("unidad_id")).denominacion
        prod["stock_disp"] = stock_disp
        prod["categoria"] = categoria
        prod["tipo"] = tipo
        prod["unidad"] = unidad
    return producto_list


@login_required(login_url='/ingresar')
def stock_disponible(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    producto_list = productos_list_updated(emp)
    args = {}
    args["producto_list"] = producto_list
    return render_to_response('stock_disponible/main.html', args, context_instance=RequestContext(request))


def loadDataExcel(emp):
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output, {'in_memory': True})
    producto_list = productos_list_updated(emp)
    # Here we will adding the code to add data
    worksheet = workbook.add_worksheet("Stock disponible")
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
    empresa = "Denominacion: " + emp.nombre
    worksheet.merge_range('A1:D1', ruc, top_title)
    worksheet.merge_range('E1:G1', empresa, top_title)
    worksheet.merge_range('B3:G3', "Reporte de stock disponible", title)
    # encabezados
    worksheet.write(4, 0, "#", header)
    worksheet.write(4, 1, "Codigo", header)
    worksheet.write(4, 2, "Nombre", header)
    worksheet.write(4, 3, "Categoria", header)
    worksheet.write(4, 4, "Tipo", header)
    worksheet.write(4, 5, "Unidad", header)
    worksheet.write(4, 6, "Stock disponible", header)
    # datos
    idx = 1
    row = 5
    for prod in producto_list:
        worksheet.write_number(row, 0, idx)
        worksheet.write(row, 1, prod.get("codigo"), cell_format)
        worksheet.write(row, 2, prod.get("nombre"), cell_format)
        worksheet.write(row, 3, prod.get("categoria"), cell_format)
        worksheet.write(row, 4, prod.get("tipo"), cell_format)
        worksheet.write(row, 5, prod.get("unidad"), cell_format)
        worksheet.write(row, 6, prod.get("stock_disp"), cell_format)
        row += 1
        idx += 1

    # resizing columns
    worksheet.set_column('B:B', 15)
    worksheet.set_column('C:C', 15)
    worksheet.set_column('D:D', 25)
    worksheet.set_column('E:E', 40)
    worksheet.set_column('F:F', 15)
    worksheet.set_column('G:G', 15)

    workbook.close()
    xlsx_data = output.getvalue()
    return xlsx_data


def export_excel(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report'

    xlsx_data = loadDataExcel(emp)

    response.write(xlsx_data)
    return response


def loadDataPDF(emp):
    producto_list = productos_list_updated(emp)
    data_pdf = {
        "headings": [("Codigo", "Nombre", "Categoria", "Tipo", "Unidad", "Stock disponible")],
        "data": [],
        "title": "Reporte de stock disponible",
        "ruc": "<b>RUC: </b>",
        "empresa": "<b>Denominacion: </b>",
    }
    for prod in producto_list:
        aux = [
            prod.get("codigo"),
            prod.get("nombre"),
            prod.get("categoria"),
            prod.get("tipo"),
            prod.get("unidad"),
            prod.get("stock_disp"),
        ]
        data_pdf["data"].append(aux)
    return data_pdf


def export_pdf(request):
    id_empresa = request.session['empresa']["id"]
    emp = models.Empresa.objects.get(id=id_empresa)
    data = loadDataPDF(emp)
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
