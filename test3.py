from graphviz import Digraph,Source
import re

# $代表空ε


def graph_nfaprint():  # 画NFA的图像
    g = Digraph('G', filename='NFA.gv', format='png',)

    for i in range(len(Move_NFA)):
        g.edge(Move_NFA[i][0], Move_NFA[i][2], label=Move_NFA[i][1])
    for i in range(len(Begin)):
        g.node(Begin[i], color='red')  # 开始节点红色
        g.node('q0',bgcolor='white',fillcolor='white',penwidht='0',style='filled')
        g.edge('q0',Begin[i], label='Start')
    for j in range(len(End)):
        g.node(End[j], shape='doublecircle')  # 结束节点双层

    g.view()


def graph_dfaprint(StateList, Begin0, End0):  # 画DFA图像
    g = Digraph('G', filename='DFA.gv', format='png')
    Begin1 = []
    End1 = []
    for i in range(len(Begin0)):
        Begin1.append(" ".join(sorted(Begin0[i])))
    for j in range(len(End0)):
        End1.append(" ".join(sorted(End0[j])))  # 从小到大排序

    for i in range(len(StateList)):
        Dict = FindNewState(StateList[i])
        for j in Str0:
            if StateList[i] != [] and Dict[j] != []:
                g.edge(" ".join(sorted(StateList[i])), " ".join(sorted(Dict[j])), label=j)
    for k in range(len(Begin1)):
        g.node(Begin1[k],color='red', shape='circle')
        g.node('q0', bgcolor='white', fillcolor='white', penwidht='0', style='filled')
        g.edge('q0', Begin1[k], label='Start')
    for i in range(len(StateList)):
        g.node(" ".join(sorted(StateList[i])), shape='circle')
    for j in range(len(End1)):
        g.node(End1[j], shape='doublecircle')
    g.view()


def Findclosure(AA):   # 输入一个状态,找这个状态的所有等价状态
    A = _closure[AA]   # 查询输入状态的空闭包
    A0 = []
    for ch in A:
        A0 = A0 + _closure[ch]
    A0 = list(set(A0))
    while set(A) != set(A0):   # 循环直到闭包集合不再变化,得到最终的结果
        A = A0
        A0 = []
        for ch in A:
            A0 = A0 + _closure[ch]
        A0 = list(set(A0))

    return A0


def FindNewState(AB):  # 找DFA状态的单步集合
    res = dict()
    for ch in Str0:
        RES = []
        for i in range(len(AB)):
            for j in range(len(Move_NFA)):
                if Move_NFA[j][0] == AB[i] and Move_NFA[j][1] == ch:
                    RES.append(Move_NFA[j][2])
        result = []
        for k in RES:
            result = result+Findclosure(k)
        res[ch] = list(set(result))
    return res


# -----------------------
with open('data2.txt', 'r') as r:
    NFA = [line.rstrip('\n') for line in r.readlines()]
Move_NFA = NFA[2::]
for i in range(len(Move_NFA)):
    Move_NFA[i] = Move_NFA[i].split()  # 以空格为分隔符分开
State = []
Str = []
for i in range(len(Move_NFA)):
    State.append(Move_NFA[i][0])
    State.append(Move_NFA[i][2])
    Str.append(Move_NFA[i][1])

State0 = list(set(State))    # 去重
State0.sort(key=State.index)  # 排序
Str0 = list(set(Str))
Str0.sort(key=Str.index)
if '$' in Str0:
    Str0.remove('$')    # 字符列表去掉ε
# print(State0)
_closure = dict()    # 建立一个空字典,表示由每个状态经由条件ε可以到达的 所有状态的集合
End = NFA[1].split()
Begin = NFA[0].split()

if __name__ == '__main__':
    graph_nfaprint()
    for i in range(len(State0)):
        res = [State0[i]]
        for j in range(len(Move_NFA)):
            if Move_NFA[j][0] == State0[i] and Move_NFA[j][1] == '$':  # 查找空闭包
                res.extend(Move_NFA[j][2])
        _closure[State0[i]]=list(set(res))
    SS = Findclosure(State0[0])     # A为初始状态等价集合
    number = 0
    length = 1
    StateList = []
    StateList .append(SS)
    while number < length:
        SS2 = FindNewState(StateList[number])
        number = number+1
        for i in Str0:
            temp = 1
            for p in range(length):
                if set(SS2[i]) == set(StateList[p]):
                    temp = 0
                    break
            if temp == 1:
                StateList .append(SS2[i])
                length = length+1


    Begin0 = []
    End0 = []  # 存放DFA开始状态和结束状态
    for i in range(len(Begin)):
        Begin0.append(Findclosure(Begin[i]))
    for j in range(len(End)):
        for k in range(len(StateList)):
            if End[j] in StateList[k]:
                if StateList[k] not in End0:
                    End0.append(StateList[k])

    while [] in StateList:
        StateList.remove([])   # 删除空状态,防止y 0 $的情况
    print('DFA状态表为:', StateList )
    print('DFA开始状态:', Begin0)
    print('DFA终止状态:', End0)
    graph_dfaprint(StateList, Begin0, End0)  # 画出DFA





