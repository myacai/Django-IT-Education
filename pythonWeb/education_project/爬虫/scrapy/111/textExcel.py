import openpyxl


def write(path, value,sheetTitle, i=0):
    wb = openpyxl.Workbook()
    sheet = wb.active
    sheet.title = sheetTitle
    for j in range(0, len(value)):
        print('i %d j %d'% (i,j))
        sheet.cell(row=i + 1, column=j + 1, value=str(value[i][j]))

    wb.save(path)
    print("写入数据成功！")


