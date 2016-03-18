from XlsxWriter import xlsxwriter
import io
from django.http import HttpResponseRedirect, HttpResponse


# funcion para crear excel
def export(request):
    workbook = xlsxwriter.Workbook('exports/hello.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'Hello world')

    workbook.close()
    return workbook


def WriteToExcel():
    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output,{'in_memory': True})

    # Here we will adding the code to add data
    worksheet = workbook.add_worksheet("Summary")

    worksheet.write(0, 0, 'Hello, world!')

    workbook.close()
    xlsx_data = output.getvalue()
    # xlsx_data contains the Excel file
    return xlsx_data


def export_excel(request):
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment; filename=Report.xlsx'
    xlsx_data = WriteToExcel()
    response.write(xlsx_data)
    return response

