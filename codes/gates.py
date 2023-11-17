def and_gate(a, b):
    if a == 'Z' or b == 'Z':
        return 'Z'
    elif a == 'U' or b == 'U':
        return 'U'
    else:
        return a and b
        
def nand_gate(a, b):
    if a == 'Z' or b == 'Z':
        return 'Z'
    elif a == 'U' or b == 'U':
        return 'U'
    else:
        return int(not(a and b))
    
def or_gate(a, b):
    if a == 'Z' or b == 'Z':
        return 'Z'
    elif a == 'U' or b == 'U':
        return 'U'
    else:
        return a or b

def nor_gate(a, b):
    if a == 'Z' or b == 'Z':
        return 'Z'
    elif a == 'U' or b == 'U':
        return 'U'
    else:
        return int(not(a or b))

def xor_gate(a, b):
    if a == 'Z' or b == 'Z':
        return 'Z'
    elif a == 'U' or b == 'U':
        return 'U'
    else:
        return int((a and not b) or (not a and b))

def xnor_gate(a, b):
    if a == 'Z' or b == 'Z':
        return 'Z'
    elif a == 'U' or b == 'U':
        return 'U'
    else:
        return int((a and b) or (not a and not b))

def not_gate(a):
    if a == 'Z':
        return 'Z'
    elif a == 'U':
        return 'U'
    else:
        return int(not(a))

def buf_gate(a):
    if a == 'Z':
        return 'Z'
    elif a == 'U':
        return 'U'
    else:
        return a

def fanout_gate(a, num_outputs=2):
    outputs = []

    if a == 'Z':
        return ['Z'] * num_outputs
    elif a == 'U':
        return ['U'] * num_outputs
    else:
        return [a] * num_outputs
