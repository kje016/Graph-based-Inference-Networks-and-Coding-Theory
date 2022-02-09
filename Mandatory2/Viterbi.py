# cd Desktop/INF244/Exercises/MA2
from sage.all import *


class Node:
    def __init__(self, path, errors):
        self.path = path
        self.errors = errors
        self.values = (path, errors)


def iterate_register(mat, input_bit, crnt_state):
    eval = mat[0].substitute(x0=input_bit, x1=crnt_state[0], x2=crnt_state[1])
    next_state = [input_bit] + crnt_state[:len(crnt_state)-1]
    return list(eval), ''.join([str(elem) for elem in next_state])


def state_diagram_fun(input_mat, state_len):
    sd = {}             # sd == state_diagram
    ss = []             # ss == state_space
    breakpoint()
    for i in range(2**state_len):
        state = "{0:b}".format(i)
        state = "0" * (state_len-len(state)) + state
        for bit in [0, 1]:
            output, next_state = iterate_register(input_mat, bit, [int(x) for x in state])
            sd.update({(state, bit): (next_state, output)})
            ss.append(next_state)
    ss = list(set(ss))
    return sd, ss


def state_to_state(state_space, state_diagram):
    output = {}
    for state1 in state_space:
        for bit in [0, 1]:
            state2 = state_diagram.get((state1, bit))
            output.update({(state1, state2[0]): (bit, state2[1])})
    return output


def decendant_set_fun(input_diagram, state_len):
    states = {}
    for i in range(2**state_len):
        state = "{0:b}".format(i)
        state = "0" * (state_len-len(state)) + state
        up_state, _ = input_diagram.get( (state, 0) )
        down_state, _ = input_diagram.get( (state, 1) )
        states.update({state: (up_state, down_state)})
    return states


def predecessor_set_fun(state_diagram):
    output = {}
    for key, value in state_diagram.items():
        new_val = output.get(value[0], [])
        output.update({value[0]: new_val+[key[0]]})
    return output


def Sd_fun(depth, predecessor_set):
    root = '00'
    s0 = list(predecessor_set.get(root))
    output = {0: s0}
    for i in range(1, depth+1):
        key = i
        value = ()
        for preds in output.get(i-1):
            value += predecessor_set.get(preds)
        value = sorted(set(value))
        output.update({key: sorted(set(value))})
    return output


def Pd_fun_s(ancestor_set):
    output = {}
    for key, value in ancestor_set.items():
        output.update({key+2: value})
    for i in range(2):
        output.update({i: ['00']})
    return output





"""     Running the Viterbi Algorithm       """


def prune(dict_paths):
    return min(dict_paths.values(), key=lambda item: item.errors)


def vit(r, S_d, P_s, P_ds, state_state):
    cwords = {}
    for n in range(len(r)):
        for next_state in S_d.get(n):
            shortest_path = {}
            for vi, valid_predecessor in enumerate(set(P_s.get(next_state)).intersection(P_ds.get(n+1))):
                key_updater = cwords.get((valid_predecessor, n - 1), Node('', 0))
                output = state_state.get((valid_predecessor, next_state))[1]
                weight = len([a+b for a, b in zip(r[n], output) if a+b >0])
                shortest_path.update({(next_state, vi): Node(key_updater.path+next_state, key_updater.errors+weight)})
            shortest_path = prune(shortest_path)
            cwords.update({(next_state, n) : Node(shortest_path.path, shortest_path.errors)})

        for next_state in S_d.get(n):
            cwords.pop((next_state, n-1), None)
    cwords = prune(cwords)
    return cwords


def path_to_inputs(vit_node, state_len, state_state):
    path = '00' +vit_node.path
    path = [path[i:i+len(state_len)] for i in range(0, len(path), len(state_len))]
    output = []
    for i, elem in enumerate(path):
        if i+1 >= len(path):
            break
        output.append(state_state.get((elem, path[i+1]))[0])
    return output


def main_viterbi(matrix, r, state_len):
    r = [r[i:i + matrix.ncols()] for i in range(0, len(r), matrix.ncols())]
    state_diagram, state_space = state_diagram_fun(matrix, len(state_len))
    state_space.sort()
    decendant_set = decendant_set_fun(state_diagram, matrix.ncols())

    P_s = predecessor_set_fun(state_diagram)
    S_d = Sd_fun(len(r)+1, decendant_set)
    P_ds = Pd_fun_s(S_d)

    state_state = state_to_state(state_space, state_diagram)
    decoded = vit(r=r, S_d=S_d, P_s=P_s, P_ds=P_ds, state_state=state_state)
    codeword = path_to_inputs(decoded, state_len, state_state)
    return codeword
