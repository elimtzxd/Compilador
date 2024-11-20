from nltk.tree import Tree
from globall import TokenType
from globall import TreeNode
import globall
from globall import StmtKind,ExpKind,DecKind,NodeKind
import sys
from globall import diccionario
import os
from util import newExpNode,newStmtNode,printTree,printTreeSemantic,indentno
from parseH import *
from analyze import buildSymtab,checkNode,typeCheck,postEval,printSymtab
from symtab import serialiceTabSym
from cgen import codeGen
#### Global Variables #####
token = -1
source = open('Archivo_Tokens2.txt','r')
tokenString = ''
root:TreeNode = None
colpos = 0
fileSintax = open(os.path.join(os.getcwd(),'Errores_Sintaxis.txt'),'w')

### Functions ###
def sintaxError(msg:str):
    #global lineno
    fileSintax.write("Syntax error at line: {0} message: {1}\n".format(globall.lineno,msg))
    recoverySintax()

def match(expected:TokenType):
    global token
    global tokenString
    if( token == expected):
        token = getTokenSintax()
    else:
        sintaxError("Unexpected token -> " + tokenString + " expected " + diccionario[expected])
         
def list_dec()->TreeNode:
    global token
    t = statement()
    p  = t
    while( token != TokenType.ENDFILE.value  and token != TokenType.END.value
          and token != TokenType.UNTIL.value and token != TokenType.ELSE.value
          and token != TokenType.RBPAREN.value):
        
        q = statement()
        if q != None:
            if t == None:
                t = p = q
            else:
                p.setSibling(q)
                p = q
     
    return t

def dec_var()->TreeNode:
    global token 
    global tokenString
    t = newStmtNode(StmtKind.DECK.value)
    e = newStmtNode(StmtKind.TYPEDEF.value)
        
    if( token == TokenType.INT.value ):
        e.setType(DecKind.INTK.value)
        e.setAttr(TokenType.INT.value)
        match(TokenType.INT.value)
    elif ( token == TokenType.BOOLEAN.value ):
        e.setType(DecKind.BOOLEANK.value)
        e.setAttr(TokenType.BOOLEAN.value)
        match(TokenType.BOOLEAN.value)
    elif( token == TokenType.REAL.value ):
        e.setType(DecKind.REALK.value)
        e.setAttr(TokenType.REAL.value)
        match(TokenType.REAL.value)
    else:
        sintaxError('Date Type Unknown')
        recoverySintax()
        return t
    t.setChild(e,0)
    id = newExpNode(ExpKind.IDK.value)
    if token == TokenType.ID.value:
        id.setAttr(tokenString)
        id.setType(e.getType())
        t.setChild(id,1)
        match(TokenType.ID.value)     
        while token == TokenType.COMMA.value:
            match(TokenType.COMMA.value)
            idAux = newExpNode(ExpKind.IDK.value)
            idAux.setAttr(tokenString)
            idAux.setType(e.getType())
         
            id.setSibling(idAux)
            id = idAux
            match(TokenType.ID.value) 
    if( token == TokenType.SEMMICOL.value ):
        match(TokenType.SEMMICOL.value)
    else:
        sintaxError('unexpected token ' + tokenString + ' Token expected '+
                    (',' if token == TokenType.ID.value else ';'))
        recoverySintax()
    return t

def statement()->TreeNode|None:
    global token 
    t = None
    if ( token == TokenType.MAIN.value ):
        t = main_stmt()
    elif( token == TokenType.IF.value ):
        t = if_stmt()
    elif( token == TokenType.DO.value):
        t = rep_stmt()
    elif( token == TokenType.WHILE.value ):
        t = it_stmt()
    elif( token == TokenType.CIN.value ):
        t = cin_stmt()
    elif( token == TokenType.COUT.value):
        t = cout_stmt()
    elif( token == TokenType.ID.value or token == TokenType.LESSL.value or token == TokenType.PLUSP.value ): 
        t = assign_stmt()
    elif( token == TokenType.INT.value or token == TokenType.BOOLEAN.value or token == TokenType.REAL.value ):
        t = dec_var()
    else:
        sintaxError(f'Unexpected Token -> {tokenString}')
       
    return t

def main_stmt()->TreeNode:
    
    t = newStmtNode(StmtKind.MAINK.value)
    match(TokenType.MAIN.value)
    match(TokenType.LBPAREN.value)
    t.setChild(list_dec(),0)
    match(TokenType.RBPAREN.value)
   
    return t

def assign_stmt()->TreeNode:
    global token
    global tokenString
    t = newStmtNode(StmtKind.ASSIGNS.value)
    if token == TokenType.LESSL.value or token == TokenType.PLUSP.value:
         t.setChild(assign_pre(),0)
         t.setAttr(tokenString)
         match(token)
    else:
        variable = tokenString
        t.setAttr(tokenString)
        match(TokenType.ID.value)
        if( token == TokenType.ASSIGN.value ):
            match(TokenType.ASSIGN.value)
            t.setChild(exp(),0)    
        elif( token == TokenType.LESSL.value or token == TokenType.PLUSP.value ):
            t.setChild(assign_post(variable),0)
            match(token)
        else:
            sintaxError(f"Unexpected Token {tokenString} ... ")
    match(TokenType.SEMMICOL.value)
    return t

def assign_pre()->TreeNode:
    global token
    global tokenString
    t = newExpNode(ExpKind.OPK.value)
    t.setAttr(TokenType.PLUS.value) if token == TokenType.PLUSP.value else t.setAttr(TokenType.MINUS.value)
    match(token)
    id = newExpNode(ExpKind.IDK.value)
    id.setAttr(tokenString)
    add = newExpNode(ExpKind.CONSTIK.value)
    add.setAttr(1)
    add.valueCalc = 1
    
    t.setChild(id,0)
    t.setChild(add,1)
    return t

def assign_post(variable:str)->TreeNode:
    global token
    global tokenString
    t = newExpNode(ExpKind.OPK.value)
    t.setAttr(TokenType.PLUS.value) if token == TokenType.PLUSP.value else t.setAttr(TokenType.MINUS.value)
    id = newExpNode(ExpKind.IDK.value)
    id.setAttr(variable)
    add = newExpNode(ExpKind.CONSTIK.value)
    add.setAttr(1)
    add.valueCalc = 1
   
    t.setChild(id,0)
    t.setChild(add,1)
    return t


def if_stmt()->TreeNode:
    global token 
    t = newStmtNode(StmtKind.IFK.value)
    match(TokenType.IF.value)
    t.setChild(exp(),0)
    t.setChild(list_dec(),1)
    if ( token == TokenType.ELSE.value ):
        match(TokenType.ELSE.value)
        e = newStmtNode(StmtKind.ELSEK.value)
        e.setChild(list_dec(),0)
        t.setChild(e,2)
    match(TokenType.END.value)
    return t

def it_stmt()->TreeNode:
    global token
    t = newStmtNode(StmtKind.WHILEK.value)
    match(TokenType.WHILE.value)
    t.setChild(exp(),0)
    if token == TokenType.SEMMICOL.value:
        match(TokenType.SEMMICOL.value)
        return t
    match(TokenType.LBPAREN.value)
    t.setChild(list_dec(),1)
    match(TokenType.RBPAREN.value)
    return t

def rep_stmt()->TreeNode:
    global token
    global tokenString
    t = newStmtNode(StmtKind.UNTILK.value)
    match(TokenType.DO.value)
    t.setChild(list_dec(),0)
    match(TokenType.UNTIL.value)
    t.setChild(exp(),1)
    match(TokenType.SEMMICOL.value)
    return t


def cin_stmt()->TreeNode:
    global token
    global tokenString
    t = newStmtNode(StmtKind.CINK.value)
    match(TokenType.CIN.value)
    if( token == TokenType.ID.value ):
        t.setAttr(tokenString)
    match(TokenType.ID.value)
    match(TokenType.SEMMICOL.value)
    return t

def cout_stmt()->TreeNode:
    global token 
    t = newStmtNode(StmtKind.COUTK.value) 
    match(TokenType.COUT.value)
    t.setChild(exp(),0)
    match(TokenType.SEMMICOL.value)
    return t

def exp()->TreeNode:
    global token
    t = simp_exp()
    if( ( token == TokenType.LESSET.value ) or ( token == TokenType.LESST.value )  or
        ( token == TokenType.GREATERT.value ) or ( token == TokenType.GREATERET.value ) 
        or ( token == TokenType.EQ.value ) or (token == TokenType.DIFF.value)):
        p = newExpNode(ExpKind.OPK.value)
        p.setChild( t , 0 )
        p.setAttr( token )
        t = p
        match(token)
        t.setChild(simp_exp(),1)
    return t        

def simp_exp()->TreeNode:
    global token 
    t = term()
    while( ( token == TokenType.PLUS.value) or ( token == TokenType.MINUS.value ) 
          or ( token == TokenType.PLUSP.value ) or ( token == TokenType.LESSL.value ) ):
        p = newExpNode(ExpKind.OPK.value)
        p.setChild(t,0)
        p.setAttr(token)
        t = p 
        match(token)
        p.setChild(term(),1)
    return t

def term()->TreeNode:
    global token
    t = factor()
    while( (token == TokenType.TIMES.value) or (token==TokenType.OVER.value)or(token == TokenType.REMAINDER.value)):
        p = newExpNode(ExpKind.OPK.value)
        p.setChild(t,0)
        p.setAttr(token)
        t = p        
        match(token)
        p.setChild(factor(),1)
    return t

def factor()->TreeNode:
    global token 
    t = None
    global tokenString
    if ( token == TokenType.ENTERO.value ):
        t = newExpNode(ExpKind.CONSTIK.value)
        t.setAttr(int(tokenString))
        t.valueCalc = int(tokenString)
        match(TokenType.ENTERO.value)
    elif ( token == TokenType.NUMREAL.value ):
        t = newExpNode(ExpKind.CONSTFK.value)
        t.setAttr(float(tokenString))
        t.valueCalc = float(tokenString)
        match(TokenType.NUMREAL.value)
    elif ( token == TokenType.ID.value ):

        t = newExpNode(ExpKind.IDK.value)
        t.setAttr(str(tokenString))
        match(TokenType.ID.value)
    elif(token == TokenType.STRING.value):
        t = newExpNode(ExpKind.STRINGK.value)
        t.setAttr(str(tokenString))
        match(TokenType.STRING.value)
    elif ( token == TokenType.LPAREN.value ):
        
         match(TokenType.LPAREN.value)
         t = exp()
         match(TokenType.RPAREN.value)
    else:
        sintaxError('Unexpected token -> '+tokenString)
        
    return t        
def parse()->TreeNode:
    global token
    global root
    global tokenString
    root = None
    token = getTokenSintax()
    root = list_dec()
    if( token != TokenType.ENDFILE.value ):
        sintaxError(f'Code ends before file {token}\n')
    return root

def getTokenSintax():
    global source
    linea = source.readline()
    global tokenString
    #global lineno
    global colpos
    if  linea:
        elementos = linea.split('\t')
        elementos = [elemento.replace("\n", "") for elemento in elementos]
        lts = []
        aux = elementos[0]
        if len(elementos)>=2:
            tokenString = elementos[1]
            globall.lineno = elementos[2]
            colpos = elementos[3]
        if(elementos[0] == 'RESERVED-WORD'):
           aux = TokenType[elementos[1].upper()].value 
        else:
            aux = TokenType[aux.upper()].value 
        return aux   
    else:
        return TokenType.ENDFILE.value    
def recoverySintax():
    global token
    while(not(token == TokenType.ENDFILE.value or 
              token == TokenType.IF.value or 
              token == TokenType.CIN.value or
              token == TokenType.COUT.value or
              token == TokenType.DO.value or
              token == TokenType.END.value or
              token == TokenType.MAIN.value or
              token == TokenType.THEN.value or
              token == TokenType.ELSE.value or
              token == TokenType.WHILE.value or
              token == TokenType.UNTIL.value or
              token == TokenType.REAL.value or
              token == TokenType.INT.value or
              token == TokenType.BOOLEAN.value or
              token == TokenType.REPEAT.value or
              token == TokenType.RBPAREN.value or
              token == TokenType.SEMMICOL.value) or
              token == TokenType.THEN.value):
        token = getTokenSintax()
    if( token == TokenType.SEMMICOL.value ):
        token = getTokenSintax()
r = parse()
print("###################")
printTree(r)
from util import serialice


fileSintax.close()
buildSymtab(r)
typeCheck(r)
indentno = 0
#calcExp(r)
printTreeSemantic(r)
with open('arbol.json', 'w') as archivo:
    arbol_diccionario = serialice(r)
    json.dump(arbol_diccionario, archivo)
with open('tabHash.json', 'w') as archivo:
    tabHash = serialiceTabSym()
    json.dump(tabHash, archivo)
printSymtab()
filesEmpty = True
with open("Archivo_Errores.txt") as file:

    file.seek(0, os.SEEK_END) # go to end of file
    if file.tell(): # if current position is truish (i.e != 0)
        file.seek(0) # rewind the file for later use 
        filesEmpty = False
    
    else:
        print ("file is empty")
        
with open("Archivo_ErrorSem.txt") as file:
    file.seek(0, os.SEEK_END) # go to end of file
    if file.tell(): # if current position is truish (i.e != 0)
        file.seek(0) # rewind the file for later use 
        filesEmpty = False
    else:
        print ("file is empty")
        

with open("Errores_Sintaxis.txt") as file:
    file.seek(0, os.SEEK_END) # go to end of file
    if file.tell(): # if current position is truish (i.e != 0)
        file.seek(0) # rewind the file for later use 
        filesEmpty = False
    else:
        print ("file is empty")
       
if filesEmpty:
    codeGen(r,"intermediateCode.tm")