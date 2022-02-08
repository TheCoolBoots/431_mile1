from cfg_generator import CFG_Node

def modify(node:CFG_Node):
    node.mappings[1] = "HELLO"

node = CFG_Node([], [], [], None)
print(node.mappings)
modify(node)
print(node.mappings)