import os
from globall import TreeNode
from tabulate import tabulate
SIZE = 211
SHIFT = 4
TabSym = open(os.path.join(os.getcwd(),'Archivo_TabSym.txt'),'a')

@staticmethod
def hash(key)->int:
    global SHIFT
    global SIZE
    temp = 0
    i = 0
    while (i < len(key)):
        temp = ((temp << SHIFT) + ord(key[i])) % SIZE
        i+=1

    return temp

class LineList:
    def __init__(self, lineno) -> None:
        self.lineno:int = lineno
        self.next:LineList = [None]
    def __str__(self) -> str:
        conc = []
        t = self
        while t is not None:
            conc.append(str(t.lineno) + ", ")
            t = t.getNext()
        return "".join(conc)
    def getLineno(self)->int:
        return self.lineno
    def setLineno(self,lineno):
        self.lineno = lineno

    def getNext(self)->None:
        return self.next
    def setNext(self,next):
        self.next = next
    
class BucketList:
    def __init__(self,tipo,name,meloc) -> None:
        self.name:str = name
        self.tipo:int = tipo
        self.valor:int|float = None
        self.lines:LineList = [None]
        self.meloc:int = meloc
        self.next:BucketList = [None]
    def getTipo(self)->int:
        return self.tipo
    def setValor(self,valor)->None:
        self.valor = valor
    def setName(self,name):
        self.name = name
    def getName(self):
        return self.name
    
    def setLines(self,lines:LineList):
        self.lines = lines
    def getLines(self)->LineList:
        return self.lines
    
    def setMeloc(self,meloc:int):
        self.meloc = meloc
    def getMeloc(self)->int:
        return self.meloc
    
    def setNext(self,next):
        self.next = next
    def getNext(self):
        return self.next

hashTable:BucketList = [None]*SIZE

def st_insert(name:str,tipo:int,valor:int|float|str, lineno:int, loc:int):
    
    h:int = hash(name)
    #h:int=100
    l:BucketList = hashTable[h]
    while ((l != None) and not(name == l.name)):
        l = l.getNext()
    if(l == None):
        l = BucketList(tipo,name,loc)
        #l.setName(name)
        l.lines = LineList(lineno)
        #l.lines.setLineno(lineno)
        #l.setMeloc(loc)
        l.lines.setNext(None)
        l.setNext(hashTable[h])
        hashTable[h] = l
        
    else:
        t:LineList = l.getLines()
        while (t.next != None):
            t = t.getNext()
        t.next = LineList(lineno)
        #t.next.setLineno(lineno)
        t.next.setNext(None)

def st_lookup(name:str)->int:
    h:int = hash(name)
    l:BucketList = hashTable[h]
    while((l != None) and not(name==l.getName())):
        l = l.getNext()
    if(l == None):
        return -1
    else:
        return l.getMeloc()

def printSymtab()->None:
    
    i = 0
    data = []
    #TabSym.write("Variable_Name\tType\tValue\tLocation\tLine_Numbers\n")
    for i in range(SIZE):
        if hashTable[i] is not None:
            l:BucketList = hashTable[i]
            while l is not None:
                t:LineList = l.getLines()
                data.append([str(l.getName()),str(l.getTipo()),l.valor,l.getMeloc(),l.getLines()])
                #TabSym.write(str(l.getName())+"\t\t\t\t")
                # Falta el Type
                #TabSym.write(str(l.getTipo())+"\t")
                # Falta el Value
                #TabSym.write(f"{l.valor}"+"\t")

                #TabSym.write(str(l.getMeloc())+"\t")
                #TabSym.write(str(l))
                """while t is not None:
                    TabSym.write(str(t.getLineno())+"-")
                    t = t.getNext()
                """
                
                l = l.getNext()
    TabSym.write(tabulate(data, headers=["Variable", "Tipo", "Valor", "L.Memoria","# de Linea"]))

def serialiceTabSym()->dict:
    file = open(os.path.join(os.getcwd(),'Diccionario_XD.txt'),'w')
    i = 0
    table:list = []
    for i in range(SIZE):
        if hashTable[i] is not None:
            l:BucketList = hashTable[i]   
            texto:dict ={
                "indice":i,
                "tab":serialiceBucket(l)
            }
            table.append(texto)
            file.write(str(texto))   
    tableF:dict ={
        "table":table
    }
    file.close()
    
    return tableF
#####
def serialiceLine(numLineas:LineList)->dict:
    tem:str=""
    if(numLineas is not None):
        while numLineas is not None:
            tem = tem + str(numLineas.getLineno())+", "
            numLineas = numLineas.getNext()
        return tem
    else:
        return None


def serialiceBucket(ren:BucketList):
    if(ren is not None):
        return {
            "name": ren.getName(),
            "valor":ren.valor,
            "type":ren.getTipo(),
            "lines":serialiceLine(ren.getLines()),
            "meloc":ren.getMeloc(),
            "next":serialiceBucket(ren.getNext())
        }
    else:
        return None
#####

####  PRUEBAS  ####
""" 
j=0
st_insert("hola",10,0)
for r in hashTable:
    print(str(r)+" -> "+str(j))
    
    j+=1 
lin:LineList = hashTable[100].getLines()
print(str(hashTable[100].getName()))
print(str(lin.getLineno())) """