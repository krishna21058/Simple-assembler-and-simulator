from hashlib import new
import math
mem=input("Space in memory :: ")
adr=input("Type of memory addressed :: ")
length=int(input("lenght of instruction :: "))
reg=int(input("length of register :: "))

# mem=input()
# adr=input()
# length=int(input())
# reg=int(input())

mems=mem.split()
adrs=adr.split()


# time={"K":2**10,"M":2**20,"G":2**30}
# meml={"B":2**3,"b":1}

time={"K":10,"M":20,"G":30}
meml={"B":3,"b":0,"w":6} #2**x
adrl={"bit":0,"nibble":2,"byte":3,"word":64}

minbit=math.ceil((math.log2(int(mems[0])))+time[mems[1][0]]+meml[mems[1][1]]-(adrl[adrs[0]]))
# print(math.log2(int(mems[0])),"+",time[mems[1][0]],"+",meml[mems[1][1]],"-",adrl[adrs[0]])
# print(minbit)

opcode=length-minbit-reg
filler=length-opcode-2*reg
instructionno=2**opcode
regno=2**reg

print("\n----------------------------------------------------------------")
print("Minimum bits are needed to represent an address in this architecture :: ",opcode)
print("Bits for opcode  :: ",opcode)
print("Number of Filler bits :: ",filler)
print("Maximum numbers of instructions this ISA can support :: ",instructionno)
print("Maximum number of registers this ISA can support :: ",regno)
# print(minbit,regno,"|",filler,instructionno)

print("\n-----------------------System enhancement-----------------------")
# cpubit=int(input("cpu bit :: "))
# changeto=input("change to :: ")

cpubit=int(input())
changeto=input()
adrl["word"]=math.log2(cpubit)
newadrtypel=changeto.split()

pin=adrl[adrs[0]]-adrl[newadrtypel[0]]

cpubit=int(input("Cpu bit :: "))
pins=int(input("pins :: "))
typeme=input(" Type of memory addressable :: ")


# cpubit=int(input())
# pins=int(input())
# typeme=input()
typemes=typeme.split()
adrl["word"]=math.ceil(math.log2(cpubit))
memorysize=(2**pins)*(2**(adrl[typemes[0]]))/8


print("\n\t\t\tType 1")
print("Mddress pins are saved or required :: ",end= " ")
print(int(pin))
print("\n\t\t\tType 2")
print("Main memory in Bytes :: ",(memorysize),"B")
print("Main memory in Bytes :: 2**(",math.log2(memorysize),") B")
print("\n----------------------------------------------------------------")



