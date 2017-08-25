import uuid
import itertools
import json
raw = [('a','b1'),
       ('a','b2'),
       ('b1','c1'),
       ('b1','c2'),
       # ('c2','f1'),
       # ('f1','g1'),
       # ('g1','h1'),
       ('c1','d1'),
       ('d1','e1'),
       ('d1','e2'),
       ('a1','b3'),
       ('b3','c3'),
       ('b3','c4'),
       ('c3','d2'),
       ('c3','d3'),
        ('c3','d4'),
        ('c3','d5'),
        ('d4','e3')
       ]

relations = {x[1]:x[0] for x in raw}
def member_info(name):
    id = uuid.uuid4().hex
    return {'id':id,'name':name}

def select_leaf():
    leafs = relations.keys()
    nodes = relations.values()
    leaf_list = list(set(leafs)-set(nodes))
    return leaf_list

node_list = [x[0] for x in raw]
leaf_list = [x[1] for x in raw]
conflicts = [x for x in list(set(leaf_list)) if leaf_list.count(x)>1]
assert not conflicts

families_list = list(set(node_list+leaf_list))
families = {name:member_info(name) for name in families_list}




while True:
    leaf = select_leaf()
    if not len(leaf):
        break
    while len(leaf):
        child_name = leaf.pop(0)
        parent_name = relations[child_name]
        child = families.pop(child_name)
        if 'child' not in families[parent_name]:
            families[parent_name]['child']=[]
        families[parent_name]['child'].append(child)
        del relations[child_name]

data = families['a']
level = 0

def set_level_by_recursion(current_member,level):
    current_member['level'] = level
    level = level+1
    current_member = current_member.get('child',[])
    for c in current_member:
        set_level_by_recursion(c,level)



def set_level_without_recursion(data):
    copy_data = data.copy()
    parent = [copy_data]
    level = 0
    while True:
        child_list = []
        for p in parent:
            p['level'] = level
            if 'child' in p:
                child_list.extend(p['child'])
        level = level + 1
        for cl in child_list:
            cl['level'] = level
        parent = child_list
        if not parent:
            break
    return copy_data

def get_relations(data):
    relations = {}
    queue = [data]
    while len(queue):
        node = queue.pop(0)
        parent_name = node['name']
        child_list = node.get('child',[])
        queue.extend(child_list)
        for c in child_list:
            relations[c['name']] = parent_name
    return relations



data = {"name": "ROOT",
 "child": [
        {"name": "Hemiptera",
         "child": [
             {"name": "Miridae",
              "child": [
                  {"name": "Kanakamiris", "child":[]},
                  {"name": "Neophloeobia",
                   "child": [
                       {"name": "incisa", "child":[] }
                   ]}
              ]}
         ]},
        {"name": "Lepidoptera",
         "child": [
             {"name": "Nymphalidae",
              "child": [
                  {"name": "Ephinephile",
                   "child": [
                       {"name": "rawnsleyi", "child":[] }
                   ]}
              ]}
         ]}
    ]}

def json_format(node,padding="--"):
    parent_list = []
    traversed = {}
    while node:
        if node['name'] not in traversed.keys():
            print padding * (len(parent_list)) + node['name']
            traversed[node['name']] = None
        child_list = node.get('child',[])
        if child_list:
            child = child_list.pop(0)
            if child['name'] not in traversed:
                print padding * (len(parent_list)+1) + child['name']
                traversed[child['name']] = node['name']
            parent_list.append(node)
            node = child

        else:
            if parent_list and child['name'] not in traversed.keys():
                print padding*(len(parent_list)+1)+child['name']
                traversed[child['name']] = node['name']
            if parent_list:
                node = parent_list.pop(-1)
            else:
                node = None
json_format(data)