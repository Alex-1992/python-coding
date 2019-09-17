import openpyxl

world_list = {}
block_list = ['new', 'for', 'to', 'with', '*', '+', '-', 'of', 'was', 'come', 'you', 'the', ' ', '', 'is', 'now', 'and']
# 打开excel文件,获取工作簿对象
wb = openpyxl.load_workbook('Space-Shooter分析.xlsx')
ws = wb.active
colD = ws['D']
# 遍历D列
for cell in colD[1:52]:
    # print(cell.value)
    str = cell.value.replace('!', ' ').replace('.', ' ').replace(',', ' ').lower()
    str_arr = str.split(' ')
    for s in str_arr:
        if s not in world_list:
            if s not in block_list:
                # kw = {s:1}
                world_list[s] = 1
        else:
            world_list[s] += 1
# print(world_list)
for w in world_list:
    if (world_list[w] > 2):
        print(w, '出现次数:', world_list[w])
