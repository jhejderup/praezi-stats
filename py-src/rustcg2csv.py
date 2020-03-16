#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Generate a dependency graph from a rust call graph
   Run: python3 rustcg2csv.py <path-to-callgaph.json>
   Return: pkg_nodes_calldata.csv, pkg_edges_calldata.csv
"""

import json
import sys
from pathlib import Path
assert len(sys.argv) == 2

with open(sys.argv[1]) as cg_file:
    data = json.load(cg_file)
    nodes = set()
    _mapping_id_node = {}
    ##
    ### Process nodes
    ##
    with open("pkg_nodes_call_data.csv", "w") as node_file: 
        node_file.write("package_name,package_version\n")
        for cg_node in data['nodes']:
             nodes.add(cg_node['package'])
             _mapping_id_node[cg_node['id']] = cg_node['package']
        for node in nodes:
            if node != 'NULL':
                pkg_id = node.split(" ")
                try:
                    node_file.write("{},{}\n".format(pkg_id[0],pkg_id[1]))
                except Exception:
                    print(pkg_id)
    ##
    ### Process edges
    ##
    with open("pkg_edges_call_data.csv", "w") as edge_file:
        edge_file.write("source_name,source_version,target_name,target_version\n")
        pkg_edges = set()
        for edge in data['edges']:
            source_id = edge[0]
            target_id = edge[1]

            source_name = _mapping_id_node[source_id]
            target_name = _mapping_id_node[target_id]
            

            ## we only want package-bound edges
            if source_name != target_name and source_name != 'NULL' and target_name != 'NULL':
                source = source_name.split(" ")
                target = target_name.split(" ")
                pkg_edges.add("{},{},{},{}\n".format(source[0], source[1],target[0],target[1]))
          
        for edge in pkg_edges:
            edge_file.write(edge)

