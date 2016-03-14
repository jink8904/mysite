from XlsxWriter import xlsxwriter

# funcion para crear excel
def export(request):
    workbook = xlsxwriter.Workbook('exports/hello.xlsx')
    worksheet = workbook.add_worksheet()

    worksheet.write('A1', 'Hello world')

    workbook.close()
