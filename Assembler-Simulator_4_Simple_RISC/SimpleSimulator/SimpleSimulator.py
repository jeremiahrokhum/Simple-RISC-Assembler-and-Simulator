from sys import stdin

def decimalToBinary(n):
    bnr = bin(int(n)).replace('0b', '')
    x = bnr[::-1]
    while len(x) < 8:
        x += '0'
    bnr = x[::-1]
    return bnr

# def  decimalToBinary2(n):
#     return '{0:016b}'.format👎

def binaryToDecimal(binary):
    binary=int(binary)
    decimal=0
    i = 0
    while(binary != 0):
        dec = binary % 10
        decimal+=dec * pow(2, i)
        binary = binary//10
        i += 1
    return decimal 
    
def decimalToBinary2(n):
    bnr = bin(int(n)).replace('0b', '')
    x = bnr[::-1]
    while len(x) < 16:
        x += '0'
    bnr = x[::-1]
    return bnr

mem_adds=["0000000000000000"]*256
pC=0
reg_val={'000':0, '001':0, '010':0, '011':0, '100':0, '101':0, '110':0, "111":"0000000000000000"}
inputs=[]


for i in stdin:
    inputs.append(i.strip())

for i in range(len(inputs)):
    mem_adds[i]=inputs[i]


def mem_dump():
    for i in mem_adds:
        print(i)

V=0
L=0
G=0
E=0

def flag_reset():
    reg_val["111"]="0000000000000000"

def execute(sen):
    global V ,L,G,E
    global pC
    op=sen[0:5]
    if op=="10000":         #  Add
        reg_val[sen[13:16]]=reg_val[sen[10:13]]+reg_val[sen[7:10]]
        if reg_val[sen[10:13]]+reg_val[sen[7:10]]>255:
            V=1
        else:
            flag_reset()
    if op=="10001":         #   Sub
        reg_val[sen[13:16]]=reg_val[sen[7:10]]-reg_val[sen[10:13]]
        if reg_val[sen[7:10]]-reg_val[sen[10:13]]<0:
            V=1
        else:
            flag_reset()
    if op=="10110":         #   Multiply
        reg_val[sen[13:16]]=reg_val[sen[7:10]]*reg_val[sen[10:13]]
        if reg_val[sen[7:10]]*reg_val[sen[10:13]]>255:
            V=1
        else:
            flag_reset()
    if op=="10111":         #   Divide    
        reg_val["000"]=int(reg_val[sen[10:13]]//reg_val[sen[13:16]])
        reg_val["001"]=int(reg_val[sen[10:13]]%reg_val[sen[13:16]])
        flag_reset()
    if op=="10011":         #   Mov reg
        reg_val[sen[13:16]]=reg_val[sen[10:13]]
        flag_reset()
    if op=="10010":         #   Mov imm
        reg_val[sen[5:8]]=binaryToDecimal(sen[8:16])
        flag_reset()
    if op=="10100":         #   Load
        reg_val[sen[5:8]]=binaryToDecimal(mem_adds[binaryToDecimal(sen[8:16])])
        flag_reset()
    if op=="10101":         #   Store
        mem_adds[binaryToDecimal(sen[8:16])-1]=decimalToBinary2(reg_val[sen[5:8]])
        flag_reset()
    if op=="11000":         #   Right Shift
        reg_val[sen[5:8]]>>binaryToDecimal(sen[8:16])
        flag_reset()
    if op=="11001":         #   Left Shift
        reg_val[sen[5:8]]<<binaryToDecimal(sen[8:16])
        flag_reset()
    if op=="11010":         #   Exclusiive Or
        reg_val[sen[13:16]]=reg_val[sen[7:10]]^reg_val[sen[10:13]]
        flag_reset()
    if op=="11011":         #   Bitwise Or
        reg_val[sen[13:16]]=reg_val[sen[7:10]]|reg_val[sen[10:13]]
        flag_reset()
    if op=="11100":         #   Bitwise And
        reg_val[sen[13:16]]=reg_val[sen[7:10]]&reg_val[sen[10:12]]
        flag_reset()
    if op=="11110":         #   Compare And Flag
        if reg_val[sen[10:13]]==reg_val[sen[13:16]]:
            E=1
        elif reg_val[sen[10:13]]>reg_val[sen[13:16]]:
            G=1
        elif reg_val[sen[10:13]]<reg_val[sen[13:16]]:
            L=1
    if op=="11111":         #   Unconditional Jump
        pC=int(binaryToDecimal(sen[8:16]))
        return
    if op=="01100":         #   Jump If  less than
        if L==1:
            pC=int(binaryToDecimal(sen[8:16]))
            return
    if op=="01101":         #   Jump If greater than
        if G==1:
            pC=int(binaryToDecimal(sen[8:16]))
            return
    if op=="01111":         #   Jump If  equal to
        if E==1:
            pC=int(binaryToDecimal(sen[8:16]))
            return
    if op=="01010":
        pass
    pC+=1

# Executing

while (pC<256):
    execute(mem_adds[pC])
    print(decimalToBinary(pC-1),end=" ")
    for x in reg_val :
        if x!="111":
            print(decimalToBinary2(str(reg_val[x])) ,end=" ")
            # print(type(reg_val[x]), end=" ")
    print(f"000000000000{V}{L}{G}{E}")
    if (mem_adds[pC-1][0:5]=="01010"):
        break
mem_dump()
