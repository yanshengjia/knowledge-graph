# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-28 Thursday
# @email: i@yanshengjia.com

import json
import pickle
import xlrd
from codecs import open
import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class Tracker:
    def __init__(self, parent=None):
        self.parent = parent
        self.student_skill_path = '../data/knowledge/student_skill.txt'  # './17_Seq2Nov_stu_skill.txt'
        self.knowledge_tree_path = '../data/knowledge/knowledge_tree.xlsx'   # './Book-All-102-2017-12-11.xlsx'
        self.knowledge_point_hash_path = '../data/knowledge/kp_id_hash.txt'  # './kp_rel_102.txt'
        self.skill_dict_path = '../data/knowledge/skill.dict'
        self.kp_number_path = '../data/knowledge/kp_id_number.txt'
        self.new_student_skill_path = '../data/knowledge/new_student_skill.txt'
        self.hierarchy_path = '../data/knowledge/hierarchy.txt'
    
    def read_knowledge_tree(self):
        workbook = xlrd.open_workbook(self.knowledge_tree_path)
        worksheet = workbook.sheet_by_index(0)
        offset = 0  # change this depending on how many header rows are present
        rows = []
        for i, row in enumerate(range(worksheet.nrows)):
            if i <= offset:  # skip headers
                continue
            r = []
            for j, col in enumerate(range(worksheet.ncols)):
                r.append(worksheet.cell_value(i, j))
            rows.append(r)
        print('Got %d rows from .xlsx' % (len(rows) - offset))
        self.knowledge_tree = rows

    def read_skill_dict(self):
        with open(self.skill_dict_path, mode='rb', encoding='utf8') as skill_dict:
            self.kp_number_hash = pickle.load(skill_dict)
    
    def read_kp_id_hash(self):
        with open(self.knowledge_point_hash_path, mode='r', encoding='utf8') as kp_id_hash_file:
            self.kp_id_hash = {}
            for line in kp_id_hash_file.readlines():
                hash, kp_id = line.strip().split('\t')
                self.kp_id_hash[hash] = kp_id

    def read_kp_number(self):
        with open(self.kp_number_path, mode='r', encoding='utf8') as kp_number_file:
            self.kp_id_number = {}
            for line in kp_number_file.readlines():
                kp_id, number = line.strip().split('\t')
                self.kp_id_number[kp_id] = number

    def get_hash(self, kp_number):
        for hash, kp_num in self.kp_number_hash.items():
            if kp_num == kp_number:
                hash = hash[1:-1]
                return hash

    def find_between(self, s, first, last):
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]

    def locate_kp(self, kp_id):
        for row in self.knowledge_tree:
            row_size = len(row)
            for i in range(row_size - 1, -1, -1):
                current_kp = row[i]
                if current_kp == '':
                    continue
                current_kp_id = self.find_between(current_kp, '[', ']')
                if kp_id == current_kp_id:
                    higher_kp = row[i-1]
                    higher_kp_id = self.find_between(higher_kp, '[', ']')
                    index = i + 1   # kp level
                    return higher_kp, higher_kp_id
        return 'null', 'null'

    def build_kp_relation(self):
        self.hierarchy = {}     # {‘kp_number’: higher_kp_number}
        for hash, kp_num in self.kp_number_hash.items():
            hash = hash[1:-1]
            kp_id = self.kp_id_hash[hash]
            higher_kp, higher_kp_id = self.locate_kp(kp_id)
            if higher_kp == 'null' and higher_kp_id == 'null':
                self.hierarchy[kp_num] = 'null'
            else:
                higher_kp_number = self.kp_id_number[higher_kp_id]
                self.hierarchy[kp_num] = higher_kp_number
        with open(self.hierarchy_path, mode='w', encoding='utf8') as hierarchy_file:
            json.dump(self.hierarchy, hierarchy_file)

    def track(self):
        with open(self.student_skill_path, mode='r', encoding='utf8') as student_skill:
            with open(self.new_student_skill_path, mode='a', encoding='utf8') as new_student_skill:
                new_student_skill.seek(0)
                new_student_skill.truncate()
                counter = 0
                for line in student_skill.readlines():
                    counter += 1
                    line = line.strip()
                    print('line ' + str(counter) + ': ' + line)
                    student_id, knowledge_point, result = line.split()
                    knowledge_point_list = knowledge_point.split(';')
                    higher_kp_list = []
                    for kp_number in knowledge_point_list:
                        print('--------------------------')
                        print('kp_number: ' + kp_number)
                        higher_kp_number = self.hierarchy[int(kp_number)]
                        if higher_kp_number == 'null':
                            print('knowledge point does not exist!')
                            continue
                        higher_kp_list.append(higher_kp_number)
                        print('higher_kp_number: ' + higher_kp_number)
                    higher_kp_list = list(set(higher_kp_list))    # merge the same higher knowledge points
                    higher_kp_str = ';'.join(higher_kp_list)
                    newline = student_id + ' ' + higher_kp_str + ' ' + result
                    print('newline ' + str(counter) + ': ' + newline)
                    print()
                    new_student_skill.write(newline + '\n')

def main():
    tracker = Tracker()
    tracker.read_knowledge_tree()
    tracker.read_skill_dict()
    tracker.read_kp_id_hash()
    tracker.read_kp_number()
    tracker.build_kp_relation()
    tracker.track()

if __name__ == "__main__":
    main()    




