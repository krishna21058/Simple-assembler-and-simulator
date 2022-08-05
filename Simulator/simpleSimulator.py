import sys

input = sys.stdin.read().split("\n")[:-1]

reg = {"000": 0, "001": 0, "010": 0, "011": 0, "100": 0, "101": 0, "110": 0, "111": 0}
var = {}
flags = {"lt": 0, "gt": 0, "e": 0, "done": 0, "mem": "00000000"}
opcode = [
    ["10000", "10001", "10110", "11010", "11011", "11100"],
    ["10010", "11000", "11001"], 
    ["10011", "10111", "11101", "11110"],
    ["10100", "10101"], 
    ["11111", "01100", "01101", "01111"], 
    ["01010"]
]

def decimalToBinary(n):
    b = bin(n).replace('0b', '')
    while len(b) < 8:
        b = '0'+b
    return b

def dkdk(command: str, pc: str):
    print(pc, end = " ")
    code = command[:5]
    if code in opcode[0]:
        typeA(command)
        for j in reg.values():
            print(decimalToBinary(j), end = " ")
        print()
    elif code in opcode[1]:
        typeB(command)
        for j in reg.values():
            print(decimalToBinary(j), end = " ")
        print()
    elif code in opcode[2]:
        typeC(command)
        for j in reg.values():
            print(decimalToBinary(j), end = " ")
        print()
    elif code in opcode[3]:
        typeD(command)
        for j in reg.values():
            print(decimalToBinary(j), end = " ")
        print()
    elif code in opcode[4]:
        for j in reg.values():
            print(decimalToBinary(j), end = " ")
        print()
        typeE(command, pc)
    else:
        flags["done"] = 1
        for j in reg.values():
            print(decimalToBinary(j), end = " ")
        print()

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
        if reg[r1] > reg[r2]:
            flags["gt"] = 1
            flags["lt"] = 0
            flags["e"] = 0
        elif reg[r1] < reg[r2]:
            flags["gt"] = 0
            flags["lt"] = 1
            flags["e"] = 0
        else:
            flags["gt"] = 0
            flags["lt"] = 0
            flags["e"] = 1

def typeD(command: str):
    code = command[:5]
    r1, mem = command[5: 8], command[8: 16]
    if code == "10100":
        reg[r1] = var[mem]
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
    while pc != decimalToBinary(len(input)):
        line = input[int(pc, 2)]
        flags["mem"] = pc
        pre_mem = flags["mem"]
        dkdk(line, pc)
        if pre_mem != flags["mem"]:
            pc = flags["mem"]
        pc = decimalToBinary(int(pc, 2)+1)
        if flags["done"] == 1:
            break
    for line in input:
        print(line)
    if len(input) < 256:
        for i in range(256-len(input)):
            print("0000000000000000")

main("00000000")