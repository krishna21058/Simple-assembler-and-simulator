import sys
import matplotlib.pyplot as pyt

global pc_list
pc_list=[]
input = sys.stdin.read().split("\n")
for i in input:
    i.rstrip()

reg = {"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0, "111": 0}
var = {}
flags = {"lt": 0, "gt": 0, "e": 0, "done": 0, "mem": "00000000"}
opcode = [
    ["10000", "10001", "10110", "11010", "11011", "11100", "00000", "00001"],
    ["10010", "11000", "11001", "00010"], 
    ["10011", "10111", "11101", "11110"],
    ["10100", "10101"], 
    ["11111", "01100", "01101", "01111"], 
    ["01010"]
]

def decimalToBinary(n, limit: int):
    b = bin(n).replace('0b', '')
    while len(b) < limit:
        b = '0'+b
    return b

def float_bin2dec(num: str):
    exp = num[:3]
    man = 0.0
    exp = int(exp, 2)-3
    for i in range(5):
        if num[3+i] == "1":
            man += 2**(-int(i+1))
    return (1+man)*2**exp

def float_dec2bin(number):
    num, dec = str(number).split(".")
    num = int(num)
    dec = int (dec)
    res = bin(num).lstrip("0b") + "."
    n = "0."+str(dec)
    p, q = n.split(".")
    i = 0
    while(n != "1.0" and i != 5):
        n = str(n)
        p, q = n.split(".")
        n = "0."+q
        n = float(n)
        n *= 2
        n = str(n)
        p, q = n.split(".")
        res += str(p)
        i += 1
    p, q = res.split(".")
    exp = len(p)+2
    res = p[0]+"."+p[1:]+q
    man = (res.split("."))[1]
    man = man[:5]
    exp = bin(exp).lstrip("0b")
    while(len(exp) < 3):
        exp = "0"+exp
    while(len(man) < 5):
        man += "0"
    final = exp+man
    return final

def print_reg(flag: int):
    gwee = 0
    if flag == 0:
        for i in reg.values():
            if gwee == 7:
                print(decimalToBinary(i, 16))
            else:
                print(decimalToBinary(i, 16), end = " ")
                gwee += 1
    else:
        for i in reg.values():
            if gwee == 7:
                print("0000000000000000")
            else:
                print(decimalToBinary(i, 16), end = " ")
                gwee += 1

def dkdk(command: str, pc: str, flag: int = 0):
    print(pc, end = " ")
    pc_list.append(pc)
    code = command[:5]
    if code in opcode[0]:
        typeA(command)
        print_reg(flag)  
    elif code in opcode[1]:
        typeB(command)
        print_reg(flag)
    elif code in opcode[2]:
        typeC(command)
        print_reg(flag)
    elif code in opcode[3]:
        typeD(command)
        print_reg(flag)
    elif code in opcode[4]:
        print_reg(flag)
        typeE(command, pc)
    else:
        flags["done"] = 1
        reg["111"] = 0
        print_reg(flag)

def typeA(command: str):
    code = command[:5]
    r1, r2, r3 = command[7: 10], command[10: 13], command[13: 16]
    if code == "10000":
        reg[r1] = reg[r2]+reg[r3]
    elif code == "10001":
        reg[r1] = reg[r2]-reg[r3]
    elif code == "10110":
        reg[r1] = reg[r2]*reg[r3]
    elif code == "11010":
        reg[r1] = reg[r2]^reg[r3]
    elif code == "11011":
        reg[r1] = reg[r2]|reg[r3]
    elif code == "00000":
        #addf
        reg[r3] = float_dec2bin(float_bin2dec(reg[r1])+float_bin2dec(reg[r2]))
    elif code == "00001":
        #subf
        v1 = float_bin2dec(reg[r1])
        v2 = float_bin2dec(reg[r2])
        if v1 < v2:
            reg[r3] = "0000000000000000"
            reg["111"] = 1
        else:
            reg[r3] = float_dec2bin(float_bin2dec(reg[r1])-float_bin2dec(reg[r2]))
    else:
        reg[r1] = reg[r2]&reg[r3]
        
def typeB(command: str):
    code = command[:5]
    r1, imm = command[5: 8], command[8: 16]
    imm = int(imm, 2)
    if code == "10010":
        reg[r1] = imm
    elif code == "11000":
        for i in range(imm):
            reg[r1] /= 2
    elif code == "11001":
        for i in range(imm):
            reg[r1] *= 2
    else:
        #movf
        reg[r1] = command[8: 16]

def typeC(command: str):
    code = command[:5]
    r1, r2 = command[10: 13], command[13: 16]
    if code == "10011":
        reg[r2] = reg[r1]
    elif code == "10111":
        reg["000"] = reg[r1]/reg[r2]
        reg["001"] = reg[r1]%reg[r2]
    elif code == "11101":
        reg[r2] = ~reg[r1]
    else:
        reg["111"] = 1
        if reg[r1] > reg[r2]:
            flags["gt"] = 1
            flags["lt"] = 0
            flags["e"] = 0
            reg["111"] = 2
        elif reg[r1] < reg[r2]:
            flags["gt"] = 0
            flags["lt"] = 1
            flags["e"] = 0
            reg["111"] = 4
        else:
            flags["gt"] = 0
            flags["lt"] = 0
            flags["e"] = 1
            reg["111"] = 1

def typeD(command: str):
    code = command[:5]
    r1, mem = command[5: 8], command[8: 16]
    if code == "10100":
        try:
            reg[r1] = var[mem]
        except:
            reg[r1] = 0
    else:
        var.update({mem: reg[r1]})

def typeE(command: str, pc: str):
    code = command[:5]
    mem = command[8: 16]
    if code == "11111":
        pc = mem
        dkdk(input[int(pc, 2)], mem)
        flags["mem"] = mem
    elif code == "01100":
        if flags["lt"]:
            pc = mem
            dkdk(input[int(pc, 2)], mem)
            flags["mem"] = mem
    elif code == "01101":
        if flags["gt"]:
            pc = mem
            dkdk(input[int(pc, 2)], mem)
            flags["mem"] = mem
    else:
        if flags["e"]:
            pc = mem
            dkdk(input[int(pc, 2)], mem)
            flags["mem"] = mem

def main(pc: str):
    if input[-1] == "" or input[-1] == "\n" or input[-1] == " ":
        input.pop()
    while pc != decimalToBinary(len(input), 8):
        if reg["111"] != 0:
            line = input[int(pc, 2)]
            flags["mem"] = pc
            pre_mem = flags["mem"]
            dkdk(line, pc, reg["111"])
            if pre_mem != flags["mem"]:
                pc = flags["mem"]
            pc = decimalToBinary(int(pc, 2)+1, 8)
            reg["111"] = 0
            if flags["done"] == 1:
                break
        else:
            line = input[int(pc, 2)]
            flags["mem"] = pc
            pre_mem = flags["mem"]
            dkdk(line, pc)
            if pre_mem != flags["mem"]:
                pc = flags["mem"]
            pc = decimalToBinary(int(pc, 2)+1, 8)
            if flags["done"] == 1:
                break
    if len(var) > 0:
        for i in sorted(var):
            input.append(decimalToBinary(var[i], 16))
    for i in range(256-len(input)):
        input.append("0000000000000000")
    for i in input:
        print(i)
	
main("00000000")
# cycle_list = [i for i in range(0, len(pc_list))]
# pyt.title("PC v/s Time Scatter Graph")
# pyt.xlabel("Time")
# pyt.ylabel("Cycle")
# pyt.scatter(cycle_list, pc_list)
# pyt.show()
