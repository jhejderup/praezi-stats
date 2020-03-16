#!/usr/bin/python3
# -*- coding: utf-8 -*-
""" 
   Run: python3 cratesio-temporal-changes <path-to-crates.io-index> <path-to-dylib>
   Return csv-file with resolved edges
"""

import sys
import json
from pathlib import Path

from ctypes import cdll, c_bool, c_void_p, cast, c_char_p, c_int32

assert len(sys.argv) == 3

RUST = cdll.LoadLibrary(sys.argv[2])

### is_match function
RUST.is_match.argtypes = (c_void_p,c_void_p)
RUST.is_match.restype = c_bool

### cmp function
RUST.cmp.argtypes = (c_void_p,c_void_p)
RUST.cmp.restype = c_int32

### Helper function
def cmp_to_key(mycmp):
    'Convert a cmp= function into a key= function'
    class K(object):
        def __init__(self, obj, *args):
            self.obj = obj
        def __lt__(self, other):
            return mycmp(self.obj, other.obj) < 0
        def __gt__(self, other):
            return mycmp(self.obj, other.obj) > 0
        def __eq__(self, other):
            return mycmp(self.obj, other.obj) == 0
        def __le__(self, other):
            return mycmp(self.obj, other.obj) <= 0  
        def __ge__(self, other):
            return mycmp(self.obj, other.obj) >= 0
        def __ne__(self, other):
            return mycmp(self.obj, other.obj) != 0
    return K

### Examples

# ver_list = "3.0.0|1.0.0|1.0.1|1.1.0|2.0.0|2.0.1|2.1.0|2.10.0|2.11.0|2.12.0|2.13.0|2.14.0|2.15.0|2.16.0|2.17.0|2.17.1|2.2.0|2.2.1|2.3.0|2.3.1|2.4.0|2.5.0|2.5.1|2.6.0|2.6.1|2.7.0|2.8.0|2.9.0".split('|')
# print(sorted(ver_list, key=cmp_to_key(RUST.cmp)))

# VER = "0.1.0"
# REQ = "^0.1.0"
# print('Does {} match {}? {}'.format(VER, REQ, RUST.is_match(REQ.encode('ascii'), VER.encode('ascii'))))


version_registry= {}
package_versions = list()

###
### Create version table
###
for path in Path(sys.argv[1]).glob('**/*'):
    if path.is_file() and "config.json" not in path.name and "crates.io-index/.git/" not in str(path):
        with path.open() as idx_fh:
            for raw_entry in idx_fh.readlines():
                entry = json.loads(raw_entry)
                package_versions.append(entry)
                if entry['name'] not in version_registry:
                    version_registry[entry['name']] = list()
                version_registry[entry['name']].append(entry['vers'])


with open("resolved_graph.csv", "w") as graph_file:
    graph_file.write("source_name,source_version,target_name,target_version\n")
    for rev in package_versions:
        if 'deps' in rev:
            for dep in rev['deps']:
                if dep['name'] in  version_registry and 'kind' in dep and (dep['kind'] == 'normal' or dep['kind'] ==  'builds'):
                    valid_vers = [ver for ver in version_registry[dep['name']] if RUST.is_match(dep['req'].encode('ascii'), ver.encode('ascii'))]
                    if len(valid_vers) > 0:
                        row =  "{},{},{},{}\n".format(rev['name'],rev['vers'],dep['name'],valid_vers)
                        graph_file.write(row)
