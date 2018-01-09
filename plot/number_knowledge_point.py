# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-28 Thursday
# @email: i@yanshengjia.com
# number all knowledge points, 0-based

from codecs import open
import xlrd

def read_knowledge_tree():
    workbook = xlrd.open_workbook('../data/knowledge/knowledge_tree.xlsx')
    worksheet = workbook.sheet_by_index(0)
    offset = 0  # change this depending on how many header rows are present
    rows = []
    knowledge_point_list = []
    for i, row in enumerate(range(worksheet.nrows)):
        if i <= offset:  # skip headers
            continue
        r = []
        for j, col in enumerate(range(worksheet.ncols)):
            r.append(worksheet.cell_value(i, j))
        rows.append(r)
    print('Got %d rows from .xlsx' % (len(rows) - offset))
    return rows

def find_between(s, first, last):
    start = s.index(first) + len(first)
    end = s.index(last, start)
    return s[start:end]

def main():
    kp_id_number_path = '../data/knowledge/kp_id_number.txt'
    knowledge_points = []
    knowledge_tree = read_knowledge_tree()
    for row in knowledge_tree:
            for i in row:
                if i == '':
                    continue
                current_kp_id = find_between(i, '[', ']')
                knowledge_points.append(current_kp_id)
    knowledge_points = list(set(knowledge_points))

    with open(kp_id_number_path, mode='a', encoding='utf8') as file:
        counter = 0
        for kp in knowledge_points:
            line = kp + '\t' + str(counter) + '\n'
            file.write(line)
            counter += 1
        print("Found %d knowledge points" % counter)

if __name__ == "__main__":
    main()

