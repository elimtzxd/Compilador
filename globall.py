from ctypes import Union
from enum import Enum
import os

with open(os.path.join(os.getcwd(),'Archivo_Tokens.txt'), "a") as archivo:
        pass  # No se realiza ninguna operación, simplemente se crea el archivo
with open(os.path.join(os.getcwd(),'Archivo_Errores.txt'), "a") as archivo:
        pass  # No se realiza ninguna operación, simplemente se crea el archivo
with open(os.path.join(os.getcwd(),'Archivo_Tokens2.txt'), "a") as archivo:
        pass  # No se realiza ninguna operación, simplemente se crea el archivo
with open(os.path.join(os.getcwd(),'Archivo_TabSym.txt'), "a") as archivo:
        pass  # No se realiza ninguna operación, simplemente se crea el archivo
with open(os.path.join(os.getcwd(),'Archivo_ErrorSem.txt'), "a") as archivo:
        pass  # No se realiza ninguna operación, simplemente se crea el archivo
MAXCHILDREN = 3
MAXRESERVEDWORDS = 14
diccionario = {
     3 : 'id',
     38: 'integer',
     37: 'real',
     6: '+',
     7: '-',
     8: '*',
     9: '/',
     40: '%',
     11: '<',
     12: '<=',
     13: '>',
     14: '>=',
     15: '=',
     16: '<>',
     17: ':=',
     18: '(',
     19: ')',
     20: '++',
     21: '--',
     22: ',',
     23: ';',
     24: '{',
     25: '}',
     34:'until',
     41:'string'
}
class TokenType(Enum):
    ENDFILE = 1
    ERROR = 2

    ID = 3
    ENTERO = 4
    NUMREAL = 5

    PLUS = 6
    MINUS = 7
    TIMES = 8
    OVER = 9
    RES = 10
    LESST = 11
    LESSET = 12
    GREATERT = 13
    GREATERET = 14
    EQ = 15
    DIFF = 16
    ASSIGN = 17
    LPAREN = 18
    RPAREN = 19
    PLUSP = 20
    LESSL = 21
    COMMA = 22
    SEMMICOL = 23
    LBPAREN = 24
    RBPAREN = 25
    

    MAIN = 26
    IF = 27
    THEN = 28
    ELSE = 29
    END = 30
    DO = 31
    WHILE = 32
    REPEAT = 33
    UNTIL = 34
    CIN = 35
    COUT = 36
    REAL = 37
    INT = 38
    BOOLEAN = 39

    REMAINDER = 40#%
    STRING = 41
lineno = 0
colpos = 0

#############################################################################
####################                     ####################################
#################### Analisis Sintactico ####################################
####################                     ####################################
#############################################################################
class NodeKind(Enum):
    STMTK = 1
    EXPK = 2
    DECK = 3

class StmtKind(Enum):
    IFK = 1
    WHILEK = 2
    DOK = 3
    UNTILK = 4
    CINK = 5
    COUTK = 6
    ASSIGNS = 7
    MAINK = 8
    DECK = 9
    TYPEDEF = 10
    ELSEK = 11

class ExpKind(Enum):
    OPK = 1
    CONSTIK = 2
    CONSTFK = 3
    IDK = 4
    STRINGK = 5

class DecKind(Enum):
    INTK = 1
    REALK = 2
    VOIDK = 3
    BOOLEANK = 4

class TreeNode:
    def __init__(self,lineno,nodekind,kind):
        self.child:list = [None]*MAXCHILDREN
        self.sibling:TreeNode = None
        self.lineno:int = lineno
        self.nodekind:NodeKind = nodekind
        self.kind:Union[StmtKind, ExpKind] = kind
        self.attr:Union[TokenType,int,float,str] = ""
        self.type:DecKind = -1
        self.valueCalc = None
    def __str__(self):
        return f'Node: {self.nodekind.name}, {self.lineno}, {self.attr}'
    def getChild(self,pos)->list:
        return self.child[pos]
    
    def setChild(self,child,pos)->None:
         self.child.insert(pos,child)
    def getSibling(self):
         return self.sibling
    def setSibling(self,sibling)->None:
         self.sibling = sibling
    def getType(self)->DecKind:
         return self.type
    def setType(self,type:DecKind)->None:
         self.type = type
    def getAttr(self):
         return self.attr
    def setAttr(self,attr)->None:
         self.attr = attr
    def getNodeKind(self)->NodeKind:
         return self.nodekind
    def getKind(self):
         return self.kind
   
    def toString(self)->str:
        return ''+str(self.lineno)+' '+str(self.nodekind)+' '+str(self.kind)+' '+str(self.attr)



    


