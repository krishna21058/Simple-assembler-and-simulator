file = open("stdin.txt", "r")
commands = []
for line in file.readlines():
    if line[-1] == "\n":
        commands.append(line[:-1].split(" "))
    else:
        commands.append(line.split(" "))

orginal_list = commands.copy()
noCommands = len(commands)

labels = {}
noVars = 0
vars = {}

# removing "" from commands
commands = [i for i in commands if i != [""]]
noCommands = len(commands)

varFlag = False
varRaiseError = False
for i in range(noCommands):
    if commands[i][0] == "var":
        if varFlag == False:
            vars[commands[i][1]] = 0
        else:
            varRaiseError = i
    elif commands[i][0][-1] == ":":
        labels[commands[i][0][:-1]] = i
        commands[i] = commands[i][1:]
    else : 
        varFlag = True

# removing vars from commands
commands = [i for i in commands if i[0] != "var"]
noCommands = len(commands)

hltMissingRaiseError = ["hlt"] not in commands
hltRaiseError = commands[-1] != ["hlt"]

error = False

zee = 0
for i in vars:
    vars[i] = noCommands+zee
    zee += 1

def decimalToBinary(n):
    b = bin(n).replace('0b','')
    while len(b) < 8:
        b='0'+b
    return b

type = [
    {
        "add": "10000",
        "sub": "10001",
        "mul": "10110",
        "xor": "11010",
        "or": "11011",
        "and": "11100" 
    }, {
        "mov": "10010",
        "rs": "11000",
        "ls": "11001"
    }, {
        "mov": "10011",
        "div": "10111",
        "not": "11101",
        "cmp": "11110"
    }, {
        "ld": "10100",
        "st": "10101"
    }, {
        "jmp": "11111",
        "jlt": "01100",
        "jgt": "01101",
        "je": "01111"
    }, {
        "hlt": "01010"
    }
]

# Atype = ["add", "sub", "mul", "xor", "or", "and"]
# Btype = ["rs", "ls"] #mov is not included
# Ctype = ["div", "not", "cmp"] #mov is not included
# Dtype = ["ld", "st"]
# Etype = ["jmp", "jlt", "jgt", "je"]
# Ftype = ["hlt"]

regMem = {
    "R0": "000",
    "R1": "001",
    "R2": "010",
    "R3": "011",
    "R4": "100",
    "R5": "101",
    "R6": "110"
}

# def regMemory(reg: str):
#     if reg == "R0":
#         return "000"
#     elif reg == "R1":
#         return "001"
#     elif reg == "R2":
#         return "010"
#     elif reg == "R3":
#         return "011"
#     elif reg == "R4":
#         return "100"
#     elif reg == "R5":
#         return "101"
#     elif reg == "R6":
#         return "110"
#     else :
#         return "111"

def typeA(command: list):
    if len(command) != 4:
        return ["111", "General syntax error"]
    out = []
    out.append(type[0][command[0]])
    out.append("00")
    if command[1] not in regMem:
        return ["111", "Wrong registor name"]
    else:
        out.append(regMem[command[1]])
    if command[2] not in regMem:
        return ["111", "Wrong registor name"]
    else:
        out.append(regMem[command[2]])
    if command[3] not in regMem:
        return ["111", "Wrong registor name"]
    else:
        out.append(regMem[command[3]])
    return out

def typeB(command: list):
    if len(command) != 3:
        return ["111", "General syntax error"]
    out = []
    out.append(type[1][command[0]])
    if command[1] not in regMem:
        return ["111", "Wrong registor name"]
    else:
        out.append(regMem[command[1]])
    num = int(command[2][1:])
    if num < -128 or num > 127:
        return ["111", "Illegal immediate value"]
    out.append(decimalToBinary(num))
    return out

def typeC(command: list):
    if len(command) != 3:
        return ["111", "General syntax error"]
    out = []
    out.append(type[2][command[0]])
    out.append("00000")
    if command[1] not in regMem:
        return ["111", "Wrong registor name"]
    else:
        out.append(regMem[command[1]])
    if command[2] not in regMem:
        return ["111", "Wrong registor name"]
    else:
        out.append(regMem[command[2]])
    return out

def typeD(command: list):
    if len(command) != 3:
        return ["111", "General syntax error"]
    out = []
    out.append(type[3][command[0]])
    if command[1] not in regMem:
        return ["111", "Wrong registor name"]
    else:
        out.append(regMem[command[1]])
    if command[2] in vars:
        out.append(decimalToBinary(vars[command[2]]))
        return out
    else:
        return ["111", "Use of undefined variable"]

def typeE(command: list):
    if len(command) != 2:
        return ["111", "General syntax error"]
    out = []
    out.append(type[4][command[0]])
    out.append("000")
    if command[1] in labels:
        out.append(decimalToBinary(labels[command[1]]))
        return out
    else:
        return ["111", "Use of undefined label"]

def typeF(command: list):
    if len(command) != 1:
        return ["111", "General syntax error"]
    else:
        return ["01010","00000000000"]

output = []
pc = 0
for i in commands:
    if varRaiseError != False:
        error = True
        print(f"Error @Line{varRaiseError+1}: Variables must be defined at the very beginning")
        break
    if hltMissingRaiseError:
        error = True
        print(f"Error : Missing hlt instruction")
        break
    if hltRaiseError:
        error = True
        print(f"Error : Hlt not being used as the last instruction")
        break
    if i[0] in type[0]:
        out = typeA(i)
        if out[0] == "111":
            output.clear()
            output.append(f"Error @Line{pc+1}: "+out[1])
            break
        else:
            output.append("".join(out))
    elif i[0] == "mov":
        if i[2][0] == "$":
            out = typeB(i)
            if out[0] == "111":
                output.clear()
                output.append(f"Error @Line{pc+1}: "+out[1])
                break
            else:
                output.append("".join(out))
        elif i[2] in regMem:
            out = typeC(i)
            if out[0] == "111":
                output.clear()
                output.append(f"Error @Line{pc+1}: "+out[1])
                break
            else:
                output.append("".join(out))
        else:
            output.clear()
            output.append(f"Error @Line{pc+1}: Wrong Syntax")
            break
    elif i[0] in type[1]:
        out = typeB(i)
        if out[0] == "111":
            output.clear()
            output.append(f"Error @Line{pc+1}: "+out[1])
            break
        else:
            output.append("".join(out))
    elif i[0] in type[2]:
        out = typeC(i)
        if out[0] == "111":
            output.clear()
            output.append(f"Error @Line{pc+1}: "+out[1])
            break
        else:
            output.append("".join(out))
    elif i[0] in type[3]:
        out = typeD(i)
        if out[0] == "111":
            output.clear()
            output.append(f"Error @Line{pc+1}: "+out[1])
            break
        else:
            output.append("".join(out))
    elif i[0] in type[4]:
        out = typeE(i)
        if out[0] == "111":
            output.clear()
            output.append(f"Error @Line{pc+1}: "+out[1])
            break
        else:
            output.append("".join(out))
    elif i[0] in type[5]:
        out = typeF(i)
        if out[0] == "111":
            output.clear()
            output.append(f"Error @Line{pc+1}: "+out[1])
            break
        else:
            output.append("".join(out))
    pc += 1

if error == False:
    out = open("compiled.bin", "wb")
    for i in output:
        out.write(str.encode(i+"\n"))
    out.close()
