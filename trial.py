file = open("trial.txt", "r")
commands = []
for line in file.readlines():
    if line[-1] == "\n":
        commands.append(line[:-1].split(" "))
    else:
        commands.append(line.split(" "))

noCommands = len(commands)

Atype = ["add", "sub", "mul", "xor", "or", "and"]
Btype = ["rs", "ls"] #mov is not included
Ctype = ["div", "not", "cmp"] #mov is not included
Dtype = ["ld", "st"]
Etype = ["jmp", "jlt", "jgt", "je"]
Ftype = ["hlt"]

def regMemory(reg: str):
    if reg == "R0":
        return "000"
    elif reg == "R1":
        return "001"
    elif reg == "R2":
        return "010"
    elif reg == "R3":
        return "011"
    elif reg == "R4":
        return "100"
    elif reg == "R5":
        return "101"
    elif reg == "R6":
        return "110"
    else :
        return "111"

def typeA(command: list):
    if len(command) != 4:
        return ["111", "Wrong number of operands"]
    out = []
    if command[0] == "add":
        out.append("10000")
    elif command[0] == "sub":
        out.append("10001")
    elif command[0] == "mul":
        out.append("10110")
    elif command[0] == "xor":
        out.append("11010")
    elif command[0] == "or":
        out.append("11011")
    elif command[0] == "and":
        out.append("11100")
    out.append("00")
    if regMemory(command[1]) != "111":
        out.append(regMemory(command[1]))
    else:
        return ["111", "Wrong registor name"]
    if regMemory(command[2]) != "111":
        out.append(regMemory(command[2]))
    else:
        return ["111", "Wrong registor name"]
    if regMemory(command[3]) != "111":
        out.append(regMemory(command[3]))
    else:
        return ["111", "Wrong registor name"]
    return out

def typeB(command: list):
    pass

def typeC(command: list):
    pass

def typeD(command: list):
    pass

def typeE(command: list):
    pass

def typeF(command: list):
    pass

print(commands)
# out = open("compiled.bin", "wb")
output = []
pc = 0
for i in commands:
    if i[0] in Atype:
        out = typeA(i)
        if out[0] == "111":
            output.clear()
            output.append(f"Error @Line{pc+1}: "+out[1])
            break
        else:
            output.append(" ".join(out))
    elif commands[i][0] in Dtype:
        output[i] = typeD(commands[i])



    pc += 1;

for i in output:
    print(i)
