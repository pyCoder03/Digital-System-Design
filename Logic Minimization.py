def Transpose(l):
    l2=list(zip(*l))
    l1=[]
    for i in l2:
        l1.append(list(i))
    return l1
def binary(n):
    s=""
    while n>=2:
        s+=str((n%2))
        n//=2
    s+=str(n)
    while len(s)<num:
        s+='0'
    return s[::-1]
def adjacency(s1,s2):               #To check the adjacency of two implicants
    num=0
    n=len(s1)
    for i in range(n):                      
        if s1[i]!=s2[i]:
            index=i
            num+=1
    adj=True if (num==1 and (s1[index]!="_" and s2[index]!="_")) else False
    return adj,index
def Minimize(minterms,dontcares):
    tot=minterms[::]
    tot.extend(dontcares)
    implicants=[]
    mincover=[]
    l1=[]
    l2=[]
    l3=[]
    for i in tot:
        l1.append(binary(i))
        l2.append([i])
    n=len(l1)
    ch=1
    while ch:
        ch=0
        for i in range(n-1):
            if l1[i].count('1')>l1[i+1].count('1'):
                l1[i],l1[i+1]=l1[i+1],l1[i]
                l2[i],l2[i+1]=l2[i+1],l2[i]
                ch=1
    while True:
        m1=[]
        m2=[]
        n=len(l1)
        l3=[False]*n            
        i=0
        j=0
        while i<n:
            while j<n :
                #print(1)
                if l1[j].count('1')==l1[i].count('1'):          #Constructing the Prime Implicant Table
                    j+=1
                    if j<n:
                        if l1[j].count('1')!=l1[i].count('1'):
                            if l1[j].count('1')==l1[i].count('1')+1:
                                num1=j
                            else:
                                num1=j
                                i=num1
                    else:
                        i=j
                        break
                elif l1[j].count('1')==l1[i].count('1')+1:
                    adj,ind=adjacency(l1[i],l1[j])
                    if adj:
                        l3[i]=True
                        l3[j]=True
                        p=l1[i][:ind:]+"_"+l1[i][ind+1::]
                        if p not in m1:
                            m1.append(p)
                            m=l2[i][::]
                            m.extend(l2[j])
                            m2.append(m)
                    if j+1<n:
                        j+=1
                    else:
                        j=num1
                        i+=1
                else:
                    j=num1
                    i+=1
        print(l1)
        print(l2)
        print(l3)
        num1=0
        for i in range(n):
            if not(l3[i]):
                implicants.append(l1[i])
                mincover.append(l2[i])
                num1+=1
        if num1==n:
            break
        l1=m1[::]
        l2=m2[::]
    print(implicants)
    print(mincover)
    ok=False
    implicants.reverse()
    mincover.reverse()
    final=set(minterms)                             #Constructing the Cover Table
    lst=minterms[::]
    minimized=[]
    num1=1
    while num1:
        num1=0
        ch=len(implicants)
        n=len(lst)
        l1=[]
        for i in range(ch):                  
            l0=[]
            for j in range(n):
                print("LST[j]: ",lst[j])
                print("Mincover[i]: ",mincover[i])
                print(lst[j] in mincover[i])
                l0.append(lst[j] in mincover[i])
            l1.append(l0)
        l2=Transpose(l1)
        print("L1: ",l1)
        print("L2: ",l2)
        j=0
        while j<len(lst):
            if l2[j].count(True)==1:               #Picking the Essential Prime Implicants
                i=l2[j].index(True)
                a=0
                while a<len(lst):
                    if lst[a] in mincover[i]:
                        print("a = ",a)
                        print("i = ",i)
                        del lst[a]
                        del l2[a]
                        print(lst)
                        print(l2)
                    else:
                        a+=1
                l1=Transpose(l2)
                minimized.append(implicants[i])
                del implicants[i]
                del mincover[i]
                if l1!=[]:
                    del l1[i]
                l2=Transpose(l1)
                print(lst)
                print(minimized)
                print(implicants)
                print(mincover)
                print(l1)
                j=0
                num1=1
            else:
                j+=1
        final=set(lst)
        l2=Transpose(l1)
        for i in range(len(mincover)):
            mincover[i]=list(set(mincover[i])&final)
        print("Minimized: ",minimized)
        if final!=set():
            ch=len(implicants)
            i=ch-1
            while i>0:
                j=i-1
                while j>=0:
                    print(set(mincover[i]))
                    print(set(mincover[j]))
                    if set(mincover[i])&set(mincover[j])==set(mincover[i]):    #Removing dominated rows
                        del implicants[i]
                        del mincover[i]
                        del l1[i]
                        num1=1
                        i-=1
                        j=i-1
                        continue
                    j-=1
                if j==-1:
                    i-=1
            ch=1
            l2=Transpose(l1)
            while ch:
                ch=0
                for i in range(len(lst)-1):
                    if l2[i].count(True)>l2[i+1].count(True):
                        l2[i],l2[i+1]=l2[i+1],l2[i]
                        lst[i],lst[i+1]=lst[i+1],lst[i]
                        ch=1
            final=set(lst)
            ch=len(lst)
            i=ch-1
            while i>0:
                j=i-1
                while j>=0:
                    if set(l2[i])&set(l2[j])==set(l2[i]):                   #Removing dominating columns
                        del l2[i]
                        del lst[i]        
                        num1=1
                        i-=1
                        j=i-1
                        continue
                    j-=1
                if j==-1:
                    i-=1
    if final==set():
        print("Poda")
    while final!=set():
        print("Hi")
        minimized.append(implicants[0])
        final=final-set(mincover[0])
        del implicants[0]
        del mincover[0]
    return minimized
var="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
print("LOGIC MINIMIZATION OF BOOLEAN FUNCTION (Uses Quine McCluskey Method)\n")
num=int(input("Enter no. of variables in the Boolean function (don't exceed 26.. xD): "))
lim=pow(2,num)
print("Enter list of minterms to be covered (Enter",lim,"to terminate):")
minterms=[]
dontcares=[]
while True:
    a=int(input())
    if a>=lim:
        break
    minterms.append(a)
print("\nEnter list of don't cares (Enter",lim,"to terminate):")
while True:
    a=int(input())
    if a>=lim:
        break
    dontcares.append(a)
minimal=Minimize(minterms,dontcares)
function=""
num_terms=len(minimal)
if minimal=="_"*num_terms:
    s="1"
else:
    for i in range(num_terms):
        term=minimal[i]
        for j in range(len(term)):
            if term[j]=="_":
                continue
            else:
                function+=var[j]
                if term[j]=="0":
                    function+="'"
        if i<num_terms-1:
            function+=" + "
print("Minimized Boolean Function:",function)
                

    
    
    
