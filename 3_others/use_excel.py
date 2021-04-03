import xlwt, xlrd

def write_excel():
    # 创建workbook和sheet对象
    workbook = xlwt.Workbook()  # 注意Workbook的开头W要大写
    sheet1 = workbook.add_sheet('startup information', cell_overwrite_ok=True)
    sheet2 = workbook.add_sheet('cpu', cell_overwrite_ok=True)
    sheet3 = workbook.add_sheet('memory', cell_overwrite_ok=True)
    sheet4 = workbook.add_sheet('disk read rate', cell_overwrite_ok=True)
    sheet5 = workbook.add_sheet('disk write rate', cell_overwrite_ok=True)
    sheet6 = workbook.add_sheet('connections num', cell_overwrite_ok=True)
    sheet7 = workbook.add_sheet('files num', cell_overwrite_ok=True)
    sheet8 = workbook.add_sheet('threads num', cell_overwrite_ok=True)
    # 向sheet页中写入数据
    sheet1.write(0, 0, 'proc_exe')
    sheet1.write(0, 1, 'proc_param')
    sheet1.write(0, 2, 'proc_name')
    sheet1.write(0, 3, 'proc_user')
    sheet1.write(0, 4, 'start time times')
    sheet1.write(0, 5, 'start time set')
    sheet1.write(0, 6, 'start time distribution')
    sheet1.write(0, 7, 'start time Probability entropy ')

    sheet2.write(0, 0, 'proc_exe')
    sheet2.write(0, 1, 'proc_param')
    sheet2.write(0, 2, 'range')
    sheet2.write(0, 3, 'average')
    sheet2.write(0, 4, 'standard deviation')
    sheet2.write(0, 5, 'Information entropy')

    sheet3.write(0, 0, 'proc_exe')
    sheet3.write(0, 1, 'proc_param')
    sheet3.write(0, 2, 'range')
    sheet3.write(0, 3, 'average')
    sheet3.write(0, 4, 'standard deviation')
    sheet3.write(0, 5, 'Information entropy')

    sheet4.write(0, 0, 'proc_exe')
    sheet4.write(0, 1, 'proc_param')
    sheet4.write(0, 2, 'range')
    sheet4.write(0, 3, 'average')
    sheet4.write(0, 4, 'standard deviation')
    sheet4.write(0, 5, 'Information entropy')

    sheet5.write(0, 0, 'proc_exe')
    sheet5.write(0, 1, 'proc_param')
    sheet5.write(0, 2, 'range')
    sheet5.write(0, 3, 'average')
    sheet5.write(0, 4, 'standard deviation')
    sheet5.write(0, 5, 'Information entropy')

    sheet6.write(0, 0, 'proc_exe')
    sheet6.write(0, 1, 'proc_param')
    sheet6.write(0, 2, 'range')
    sheet6.write(0, 3, 'average')
    sheet6.write(0, 4, 'standard deviation')
    sheet6.write(0, 5, 'Information entropy')

    sheet7.write(0, 0, 'proc_exe')
    sheet7.write(0, 1, 'proc_param')
    sheet7.write(0, 2, 'range')
    sheet7.write(0, 3, 'average')
    sheet7.write(0, 4, 'standard deviation')
    sheet7.write(0, 5, 'Information entropy')

    sheet8.write(0, 0, 'proc_exe')
    sheet8.write(0, 1, 'proc_param')
    sheet8.write(0, 2, 'range')
    sheet8.write(0, 3, 'average')
    sheet8.write(0, 4, 'standard deviation')
    sheet8.write(0, 5, 'Information entropy')

    """
    #-----------使用样式-----------------------------------
    #初始化样式
    style = xlwt.XFStyle() 
    #为样式创建字体
    font = xlwt.Font()
    font.name = 'Times New Roman'
    font.bold = True
    #设置样式的字体
    style.font = font
    #使用样式
    sheet.write(0,1,'some bold Times text',style)
    """
    # 保存该excel文件,有同名文件时直接覆盖
    workbook.save('test2.xls')
    print('创建excel文件完成！')

if __name__ == '__main__':
    write_excel()