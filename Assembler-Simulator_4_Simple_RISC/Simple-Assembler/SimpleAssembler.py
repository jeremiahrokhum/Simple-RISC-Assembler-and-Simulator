import sys
counter  = 0
Lines=0
v_count=0
l_count=0
output=[]
errorList=[]
variable={}
labels={}

def errorLister(errType, cnt):
    global errorList
    if(errType=="UndefinedVar"):
        errorList.append(f"Undefined variable in line {cnt}")

    elif(errType=="Typo"):
        errorList.append(f"typo in line {cnt}")

    elif(errType=="HltDefinedInBetween"):
        errorList.append(f"Hlt statement provided in between in line {cnt}")

    elif(errType=="HltNotDeclared"):
        errorList.append(f"Hlt statement not at the end {cnt}")

    elif(errType=="ImmediateVal"):
        errorList.append(f"Immediate value out of range in line {cnt}")

    elif(errType=="IllegalFlag"):
        errorList.append(f"Illegal flag used in line {cnt}")

    elif(errType=="VariableAtBetween"):
        errorList.append(f"Variable defined on start in line {cnt}")

    elif(errType=="LabelAsVariable"):
        errorList.append(f"Used label as variable in line {cnt}")

    elif(errType=="VariableAsLable"):
        errorList.append(f"Used variable as label in line {cnt}")

    elif(errType=="HltMissed"):
        errorList.append(f"Hlt statement missing in line {cnt}")

    elif(errType == "MemoryExceed256"):
        errorList.append(f"Error: The assembler can only write 256 lines")
    else:
        errorList.append(f"General syntax error in line {cnt}")


def regtobinary(reg):
    if reg =="R0":
        return "000"
    elif reg =="R1":
        return "001"
    elif reg =="R2":
        return "010"
    elif reg =="R3":
        return "011"
    elif reg =="R4":
        return "100"
    elif reg =="R5":
        return "101"
    elif reg =="R6":
        return "110"
    elif reg =="FLAGS":
        return "111"
    else:
        #errorhandling
        print("Invalid name")


def decimalToBinary(n):
    return bin(n).replace("0b", "")


def Immcheck(n):
    if(n<=255 & n>=0):
        return 1
    else:
        return 0
    
def immmaking(n):
    if(Immcheck(n) == 1):
        r = decimalToBinary(n)
        if(len(r)!=8):
            result = "0"*(8 - len(r)) + r
        return(result)
    else:
        #error handling 
        print("error for not having 8 bit number")

def memaddress_making(var):
    counter=variable[var]+Lines
    if(Immcheck(counter) == 1):
        r = decimalToBinary(counter)
        if(len(r)!=8):
            result = "0"*(8-len(r)) + r
        return(result)
    else:
        #error handling
        print("Error")

def memaddress_making_label(label):
    counter=labels[label]
    if(Immcheck(counter) == 1):
        r = decimalToBinary(counter)
        if(len(r)!=8):
            result = "0"*(8-len(r)) + r
        return(result)
    else:
        #error handling
        print("Error")


def var(variable):
    #do something with variable
    global counter, output
    counter = counter + 1

def add(reg1,reg2,reg3):
    
    global counter, output 
    counter = counter + 1
    
    r1=regtobinary(reg1)
    r2=regtobinary(reg2)
    r3=regtobinary(reg3)
    if r1=="111" or r2=="111" or r3=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name" or r2=="Invalid name" or r3=="Invalid name":
        errorLister("Typo",counter)
    else:
        term="1000000"+r1+r2+r3
        output.append(term)
    # return reg3

def sub(reg1,reg2,reg3):
    global counter, output
    counter = counter + 1
    # print(10001,end = '')
    # print("00",end = '')
    r1=regtobinary(reg1)
    r2=regtobinary(reg2)
    r3=regtobinary(reg3)
    if r1=="111" or r2=="111" or r3=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name" or r2=="Invalid name" or r3=="Invalid name":
        errorLister("Typo",counter)
    else:
        term="10001"+"00"+r1+r2+r3
        output.append(term)
    
def movimm(reg,imm):
    global counter, output 
    counter = counter + 1
    # print(10010,end ='')
    # print(regtobinary(reg),end = '')
    im=immmaking(imm)
    r1= regtobinary(reg)
    if r1=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name":
        errorLister("Typo",counter)
    else:
    # print(immmaking(imm),end = '\n')
        term="10010"+r1+im
        output.append(term)
  
def movreg(reg1,reg2):
    global counter, output 
    counter = counter + 1
    # reg2=reg1
    # print(10011,end = '')
    # print("00000",end = '')
    # print(regtobinary(reg1),end = '')
    # print(regtobinary(reg2),end = '\n')
    r1 = regtobinary(reg1)
    r2 = regtobinary(reg2)
    if r1=="111" or r2=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name" or r2=="Invalid name":
        errorLister("Typo",counter)
    else:
        term = "10011"+"00000"+r1+r2
        output.append(term)

def ld(reg1,var):
    global counter, output
    counter = counter + 1
    # print(10100,end = '')
    r1 = regtobinary(reg1)
    mem = memaddress_making(var)
    # print(regtobinary(reg1),end = '')
    # print(memaddress_making(counter),end = '\n')
    if r1=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name":
        errorLister("Typo",counter)
    elif mem=="Error":
        errorLister("UndefinedVar")
    # reg1=mem_address
    else:
        term = "10100" + r1 + mem                    #term
        output.append(term)
def st(reg1,var):
    global counter, output
    counter = counter + 1
    # print(10101,end = '')
    r1 = regtobinary(reg1)
    mem = memaddress_making(var)
    # print(regtobinary(reg1),end = '')
    # print(memaddress_making(counter),end = '\n')
    if r1=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name":
        errorLister("Typo",counter)
    elif mem=="Error":
        errorLister("UndefinedVar")
    else:
        term =  "10101" + r1 + mem                    #term
        output.append(term)
    
    # mem_address=reg1
def mul(reg1,reg2,reg3):
    global counter, output
    counter = counter + 1
    # reg3= reg1*reg2
    # if len(reg1)+len(reg2)>len(reg3):
    #     flag=1
    # flag=0
    # print(10110,end='')
    # print("00",end='')
    # print(regtobinary(reg1),end='')
    # print(regtobinary(reg2),end='')
    # print(regtobinary(reg3),end='\n')
    r1=regtobinary(reg1)
    r2=regtobinary(reg2)
    r3=regtobinary(reg3)
    if r1=="111" or r2=="111" or r3=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name" or r2=="Invalid name" or r3=="Invalid name":
        errorLister("Typo",counter)
    else:
        term="10110" +"00"+r1+r2+r3                  #term
        output.append(term)

def div(reg3,reg4):
    global counter, output
    counter = counter + 1
    # print(10111,end = '')
    # print("00000",end = '')
    # print(regtobinary(reg3),end='')
    # print(regtobinary(reg4),end = '\n')
    r3=regtobinary(reg3)
    r4=regtobinary(reg4)
    if r3=="111" or r4=="111":
        errorLister("IllegalFlag",counter)
    elif r3=="Invalid name" or r4=="Invalid name":
        errorLister("Typo",counter)
    # reg0=reg3//reg4
    # reg1=reg3%reg4
    #return quotient and remainder or only one thing
    else:
        term = "10111" +  "00000" + r3 + r4                #term
        output.append(term)

def rs(reg1,imm):
    global counter, output
    counter = counter + 1
    # print(11000,end = '')
    # print(regtobinary(reg1),end = '')
    # print(immmaking(imm),end = '\n')
    # if len(str(imm))==8:
    #     reg1=str(imm)+str(reg1)
    r1 = regtobinary(reg1)
    im = immmaking(imm)
    if r1=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name":
        errorLister("Typo",counter)
    else:
        term = "11000" + r1 + im                 #term
        output.append(term)

def ls(reg1,imm):
    global counter, output
    counter = counter + 1
    # print(11001,end = '')
    # print(regtobinary(reg1),end = '')
    # print(immmaking(imm),end = '\n')#imm ke liye thoda aur karo
    # if len(str(imm))==8:xor
    #     reg1=+str(reg1)+str(imm)
    r1 = regtobinary(reg1)
    im = immmaking(imm)
    if r1=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name":
        errorLister("Typo",counter)
    else:
        term = "11001" + r1 + im                     #term
        output.append(term)

def xor(reg1,reg2,reg3):
    global counter, output
    counter = counter + 1
    # print(11010,end = '')
    # print("00",end = '')
    # print(regtobinary(reg1),end = '')
    # print(regtobinary(reg2),end = '')
    # print(regtobinary(reg3),end = '\n')
    r1=regtobinary(reg1)
    r2=regtobinary(reg2)
    r3=regtobinary(reg3)
    if r1=="111" or r2=="111" or r3=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name" or r2=="Invalid name" or r3=="Invalid name":
        errorLister("Typo",counter)
    else:
        term="11010"+"00"+r1+r2+r3                  #term
        output.append(term)
    # # reg3=reg1^reg2
  
def bitwise_and(reg1,reg2,reg3):
    global counter,output
    r1=regtobinary(reg1)
    r2=regtobinary(reg2)
    r3=regtobinary(reg3)
    if r1=="111" or r2=="111" or r3=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name" or r2=="Invalid name" or r3=="Invalid name":
        errorLister("Typo",counter)
    else:
        term="11100" + "00" +r1+r2+r3                  #term
        output.append(term)

def bitwise_or(reg1,reg2,reg3):
    global counter,output
    r1=regtobinary(reg1)
    r2=regtobinary(reg2)
    r3=regtobinary(reg3)
    if r1=="111" or r2=="111" or r3=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name" or r2=="Invalid name" or r3=="Invalid name":
        errorLister("Typo",counter)
    else:
        term="11011" + "00" +r1+r2+r3                  #term
        output.append(term)

def invert(reg1,reg2):
    global counter, output
    # reg2=~reg1
    # print(11101,end='')
    # print("00000",end='')
    # print(regtobinary(reg1),end='')
    # print(regtobinary(reg2),end='\n')
    r1=regtobinary(reg1)
    r2=regtobinary(reg2)
    if r1=="111" or r2=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name" or r2=="Invalid name":
        errorLister("Typo",counter)
    else:
        term = "11101"+"00000"+r1+r2
        output.append(term)

def cmp(reg1,reg2):
    global counter, output
    #???
    # return 0
    # print(11110,end='')
    # print("00000",end='')
    # print(regtobinary(reg1),end='')
    # print(regtobinary(reg2),end='\n')
    r1=regtobinary(reg1)
    r2=regtobinary(reg2)
    if r1=="111" or r2=="111":
        errorLister("IllegalFlag",counter)
    elif r1=="Invalid name" or r2=="Invalid name":
        errorLister("Typo",counter)
    else:
        term = "11110"+"00000"+r1+r2
        output.append(term)

def jgt(label):
    global counter, output
    a =labels[label]
    mem =memaddress_making_label(label)
    if(mem == "Error"):
        errorLister("",counter)
    else:
        term = "01101" + "000" + mem
        output.append(term)

def jmp(label):
    global counter, output
    a =labels[label]
    mem =memaddress_making_label(label)
    if(mem == "Error"):
        errorLister("",counter)
    else:
        term = "11111" + "000" + mem
        output.append(term)
def jlt(label):
    global counter, output
    a=labels[label]
    mem=memaddress_making_label(label)
    if mem=="Error":
        errorLister("",counter)            #fill in
    else:
        term = "01100" + "000" + mem
        output.append(term)

def je(label):
    global counter, output
    a = labels[label]
    mem = memaddress_making_label(label)
    if(mem == "Error"):
        errorLister("",counter)
    else:
        term = "01111" + "000" + mem
        output.append(term)

def hlt():
    global counter,output
    term = "01010" + "00000000000"
    output.append(term)
    
c=0
isv=True
hlt_c=0
lines=[]

for line in sys.stdin:
    c+=1
    a=line.split()
    if (a[0]=="/n"):
        a="this@@@$empty"
        lines.append(a)
    elif(a[0]=="var"):
        Lines+=1
        if isv==True:
            if(a[1] in variable):
                errorLister("ble",c)
            elif(a[1] in labels):
                errorLister("LabelAsVariable",c)
                lines.append("alreadyused___")
            else:
                variable[a[1]]=c
        else:
            errorLister("VariableAtBetween",c)
            lines.append("alreadyused___")
    elif(a[0][-1]==":"):
        Lines+=1
        isv=False
        if(a[0] in labels):
            errorLister("ble",c)
            lines.append("alreadyused___")
        elif(a[0] in variable):
            errorLister("VariableAsLable",c)
            lines.append("alreadyused___")
        else:
            labels[a[0]]=Lines
            lines.append(a[1::])
    elif (a[0]=="hlt"):
        hlt_c+=1
        lines.append(a)
    
    else:
        isv==False
        Lines+=1
        lines.append(a)

    
if (hlt_c<1):
    errorLister("HltMissed",len(lines))
for j in range(len(lines)):
    try:
        input=lines[j]
        i=j+len(variable)
        if (input[0]=="this@@@$empty"):
            continue
        elif (input[0]=="alreadyused___"):
            continue
        elif(input[0]=="add"):
            add(input[1],input[2],input[3])
        elif(input[0]=="sub"):
            sub(input[1],input[2],input[3])
        elif(input[0]=="mov"):
            if input[2][0]=="$":
                imm=input[2][1::]
                movimm(input[1],imm)
            else:
                movreg(input[1],input[2])

        elif(input[0]=="ld"):
            ld(input[1],input[2])
        elif(input[0]=="st"):
            st(input[1],input[2])
        elif(input[0]=="mul"):
            mul(input[1],input[2],input[3])
        elif(input[0]=="div"):
            div(input[1],input[2])
        elif(input[0]=="rs"):
            rs(input[1],input[2][1::])
        elif(input[0]=="ls"):
            ls(input[1],input[2][1::])
        elif(input[0]=="xor"):
            ls(input[1],input[2],input[3])
        elif(input[0]=="or"):
            bitwise_or(input[1],input[2],input[3])
        elif(input[0]=="and"):
            bitwise_and(input[1],input[2],input[3])
        elif(input[0]=="not"):
            invert(input[1],input[2])
        elif(input[0]=="cmp"):
            cmp(input[1],input[2])
        elif(input[0]=="jmp"):
            jmp(input[1])
        elif(input[0]=="jlt"):
            jlt(input[1])
        elif(input[0]=="jgt"):
            jgt(input[1])
        elif(input[0]=="je"):
            je(input[1])
        elif(input[0]=="hlt"):
            hlt()
        else:
            errorLister("Typo",i)

    except:
        errorLister("",i)
if(len(errorList) != 0):
    for i in errorList:
        print(i)
else:
    for i in range(min(265,len(output))):
        print(output[i])
#Functions left to be made:- 
#Jump if less than RAGHAV DONE
#Jump if greater than JEREMIAH DOING
#Jump if equal     JEREMIAH DOING
#Halt DONE
#unconditional jump   DONE
#bitwise or DONE 
