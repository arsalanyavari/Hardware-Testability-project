from functools import reduce

def and_gate(input_list = []):
    if 0 in input_list:
        return 0
    elif 'Z' in input_list:
        return 'Z'
    elif 'U' in input_list:
        return 'U'
    else:
        return 1
        # return int(all(i for i in input_list))
        
def nand_gate(input_list = []):
    tmp = and_gate(input_list)
    if tmp != 1 and tmp != 0:
        return tmp
    else:
        return int(not(tmp))

    # if 'Z' in input_list:
    #     return 'Z'
    # elif 'U' in input_list:
    #     return 'U'
    # else:
    #     return int(not(all(i for i in input_list)))
    
def or_gate(input_list = []):
    if 1 in input_list:
        return 1
    elif 'Z' in input_list:
        return 'Z'
    elif 'U' in input_list:
        return 'U'
    else:
        return 0
        # return int(any(i for i in input_list))

def nor_gate(input_list = []):
    tmp = or_gate(input_list)
    if tmp != 1 and tmp != 0:
        return tmp
    else:
        return int(not(tmp))
    # if 'Z' in input_list:
    #     return 'Z'
    # elif 'U' in input_list:
    #     return 'U'
    # else:
    #     return int(not(any(i for i in input_list)))

def xor_gate(input_list = []):
    if 'Z' in input_list:
        return 'Z'
    elif 'U' in input_list:
        return 'U'
    else:
        return int(reduce(lambda x, y: x ^ y, input_list))

def xnor_gate(input_list = []):
    if 'Z' in input_list:
        return 'Z'
    elif 'U' in input_list:
        return 'U'
    else:
        return int(not(reduce(lambda x, y: x ^ y, input_list)))

def not_gate(input_):
    if input_ == 'Z':
        return 'Z'
    elif input_ == 'U':
        return 'U'
    else:
        return int(not(input_))

def buffer_gate(input_):
    if input_ == 'Z':
        return 'Z'
    elif input_ == 'U':
        return 'U'
    else:
        return input_

def fanout_gate(a, num_outputs=2):
    if a == 'Z':
        return ['Z'] * num_outputs
    elif a == 'U':
        return ['U'] * num_outputs
    else:
        return [a] * num_outputs
