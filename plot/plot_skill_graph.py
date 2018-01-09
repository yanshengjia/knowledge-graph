# !/usr/bin/python
# -*- coding:utf-8 -*-  
# @author: Shengjia Yan
# @date: 2017-12-14 Thursday
# @email: i@yanshengjia.com
# run under python 3

import os
from codecs import open
import pydot
import networkx as nx
from networkx.drawing.nx_agraph import write_dot
from networkx.drawing.nx_pydot import to_pydot
import matplotlib.pyplot as plt


class PlotSkillGraph:
    def __init__(self, parent=None):
        self.parent = parent
        self.skill_rel_path = '../data/knowledge/skill_rel.txt'
        self.pgm = nx.MultiDiGraph()
        self.threshold = 0.95
        self.edge_counter = 0

    def cluster(self):
        print

    def build_skill_graph(self):
        with open(self.skill_rel_path, mode='r', encoding='UTF8') as skill_file:
            for line in skill_file.readlines():
                line = line.strip()
                node_from, node_to, probability = line.split()
                node_from = int(node_from)
                node_to = int(node_to)
                probability = float(probability)
                # if probability > self.threshold:
                self.pgm.add_node(node_from, label=str(node_from))
                self.pgm.add_node(node_to, label=str(node_to))
                self.pgm.add_edge(node_from, node_to, probability=probability, label=str(probability))
                self.edge_counter += 1
            # self.graph_name = '../output/graph_' + str(self.threshold) + '_' + str(self.edge_counter)
            self.graph_name = '../output/graph'
    
    def draw_skill_graph(self):
        g_str = to_pydot(self.pgm).to_string()
        self.pgm = pydot.graph_from_dot_data(g_str)
        self.pgm[0].write_png(self.graph_name + '.png')
    
    def save_dot(self):
        write_dot(self.pgm, self.graph_name + '.dot')
        # os.system('dot -Tsvg ' + self.graph_name + '.dot' + ' -o ' + self.graph_name + '.svg')
    
    def save_gexf(self):
        nx.write_gexf(self.pgm, self.graph_name + '.gexf')

def main():
    plotter = PlotSkillGraph()
    plotter.build_skill_graph()
    plotter.draw_skill_graph()
    # plotter.save_graph_dot()
    # plotter.save_gexf()

if __name__ == "__main__":
    main()
