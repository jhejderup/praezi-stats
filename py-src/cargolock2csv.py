#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" Generate a dependency graph from a Cargo.lock file
   Run: python3 cargolock2csv.py <path-to-Cargo.lock>
   Deps: pip3 install toml
   Return: pkg_nodes.csv, pkg_edges.csv
"""
import sys

import toml

assert len(sys.argv) == 2

def read_contents(file_path):
  with open(file_path, 'r') as f:
    return f.read()


def create_name_version_mappings(lockfile_dict):
    __pkg_name_version_mappings = {}
    for pkg in lockfile_dict['package']:
        if pkg['name'] in __pkg_name_version_mappings: 
            continue ##don't include resolved versions
        else:
            __pkg_name_version_mappings[pkg['name']] = pkg['version']
    return __pkg_name_version_mappings



lockfile_string = read_contents(sys.argv[1])
lockfile_dict = toml.loads(lockfile_string)

__mappings_name_ver = create_name_version_mappings(lockfile_dict)

with open("pkg_edges.csv", "w") as edge_file:
        edge_file.write("source_name,source_version,target_name,target_version\n")
        for pkg in lockfile_dict['package']:
            source_name = pkg['name']
            source_version = pkg['version']
            source = "{},{}".format(source_name, source_version)

            if 'dependencies' in pkg:
                for dep in pkg['dependencies']:
                    if " " in dep:
                        dep_arr = dep.split(" ")
                        target = "{},{}".format(dep_arr[0], dep_arr[1])
                    else:
                        target_version = __mappings_name_ver[dep]
                        target = "{},{}".format(dep, target_version)
                
                    edge_file.write("{},{}\n".format(source, target))

with open("pkg_nodes.csv", "w") as node_file:
    node_file.write("package_name,package_version\n")
    for pkg in lockfile_dict['package']:
        name = pkg['name']
        version = pkg['version']
        node = "{},{}\n".format(name, version)
        node_file.write(node)











