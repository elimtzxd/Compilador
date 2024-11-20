import sys
import os 
import globall
from globall import TokenType as tp
from globall import lineno
from enum import Enum
from util import *
bufsize = 0
MaxTokenLen = 40
TokenString = list()
linea = str()
MAXBUFFER = 1024
namefile = sys.argv[1]
source = open(namefile,'r')
#########################################
fileoutput = open(os.path.join(os.getcwd(),'Archivo_Tokens.txt'),'w')
fileoutputError = open(os.path.join(os.getcwd(),'Archivo_Errores.txt'),'w')
fileoutput2 = open(os.path.join(os.getcwd(),'Archivo_Tokens2.txt'),'w')
###################################################
consume:bool  = True
c:str
reservedWords ={
    'MAIN':tp.MAIN,
    'IF':tp.IF,
    'THEN':tp.THEN,
    'ELSE':tp.ELSE,
    'END':tp.END,
    'DO':tp.DO,
    'WHILE':tp.WHILE,
    'REPEAT':tp.REPEAT,
    'UNTIL':tp.UNTIL,
    'CIN':tp.CIN,
    'COUT':tp.COUT,
    'REAL':tp.REAL,
    'INT':tp.INT,
    'BOOLEAN':tp.BOOLEAN


} 

class States(Enum):
    INICIO = 0
    EMENOS = 1
    EMMENOS = 2
    EMAS = 3
    EMMAS = 4
    EENTEROS = 5
    EPREAL = 6
    EREAL = 7
    EID = 8
    EASIGNA = 9
    EPCOMM = 10
    ECOMMSIMPLE = 11
    EPCOMMMULTI = 12
    ECOMMMULTI = 13
    EMAYOR = 14
    EMAYORIGUAL = 15
    EMENOR = 16
    EMENORIGUAL = 17
    EDIFERENTE = 18
    HECHO = 19
    ESTRING = 20
    
def getNextChar():
    
    global bufsize
    global source
    global linea
    if( not(globall.colpos < bufsize) ):
        linea = source.readline()
        
        if  linea:
            globall.lineno+=1
            
            bufsize = len(linea)
            globall.colpos = 0
            char = linea[globall.colpos]
            globall.colpos+=1
            return char
        else:
            
            return "EOF"    
    else:
        char = linea[globall.colpos]
        
        globall.colpos+=1
        return char
    
        
def ungetChar():
    globall.colpos-=1

def isReservedWord(tokenString:str)->tp:
    for key in reservedWords.keys():
        if(key.lower() == tokenString):
            
            return reservedWords[key]

    return tp.ID    

def getToken()->tp:
    global consume,c
    tokenStringIndex = 0
    currentToken:tp
    state:States = States.INICIO
    
    while state != States.HECHO:
        
        if consume == True: 
            c = getNextChar()
       
        if state == States.INICIO:
            consume = True
            while c in ['\n' , '\t' , ' '] :
                c = getNextChar()
                
            if type(c) is tp:
                c = "EOF"
               
            TokenString.append(c)
            
            if   c == "EOF":
                state = States.HECHO
                currentToken = tp.ENDFILE
            elif c.isdigit():
                state = States.EENTEROS
            elif c.isalnum() or c == "_":
                state = States.EID
               
            elif c == ":":
                state = States.EASIGNA
            elif c == "+":
                state = States.EMAS
            elif c == "-":
                state = States.EMENOS
            elif c == "/":
                
                state = States.EPCOMM
            elif c == ">":
                state = States.EMAYOR
            elif c == "<":
                state = States.EMENOR
            elif c == "*":
                currentToken = tp.TIMES
                state = States.HECHO
            elif c == "%":
                currentToken = tp.REMAINDER
                state = States.HECHO
            elif c == "(":
                currentToken = tp.LPAREN
                state = States.HECHO
            elif c == ")":
                currentToken = tp.RPAREN
                state = States.HECHO
            elif c == "{":
                currentToken = tp.LBPAREN
                state = States.HECHO
            elif c == "}":
                currentToken = tp.RBPAREN
                state = States.HECHO
            elif c == ",":
                currentToken = tp.COMMA
                state = States.HECHO
            elif c == ";":
                currentToken = tp.SEMMICOL
                state = States.HECHO
            elif c == "=":
                currentToken = tp.EQ
                state = States.HECHO
            elif c == "\"":
                state = States.ESTRING
            else:
                
                currentToken = tp.ERROR
                state = States.HECHO 
        elif state == States.EENTEROS:
           
            if c == ".":
                state = States.EPREAL
                TokenString.append(c)
                consume = True
            elif not c.isdigit():
                currentToken = tp.ENTERO
                state = States.HECHO
                consume = False
                
            else:
                TokenString.append(c)
        elif state == States.EID:
            
            if c.isdigit() or c == "_" or c.isalnum() and c != "EOF": 
               TokenString.append(c)
            else : 
               currentToken  = tp.ID
               currentToken = isReservedWord("".join(TokenString))
               state = States.HECHO 
               consume = False
        elif state == States.EPREAL:
            if c.isdigit() :
                state = States.EREAL
                TokenString.append(c)
            else : 
                state = States.HECHO
                currentToken = tp.ERROR
                consume = False
        elif state == States.EREAL:
            if c.isdigit():
                TokenString.append(c)
            else : 
                consume = False
                currentToken = tp.NUMREAL
                state = States.HECHO
        elif state == States.EMAYOR:
            if c == '=':
                currentToken = tp.GREATERET #Mayor Igual
                state = States.HECHO
            else : 
                consume = False
                currentToken = tp.GREATERT
                state = States.HECHO

        elif state == States.EMENOR:
            if c == '=':
                currentToken = tp.LESSET #Menor Igual
                state = States.HECHO
            elif c == '>':
                currentToken = tp.DIFF #### Diferente <>
                state = States.HECHO
            else :
                currentToken = tp.LESST
                state = States.HECHO
                consume = False
            ###########################################################################
        elif state == States.EASIGNA:
            if c == "=":
                currentToken = tp.ASSIGN
                state = States.HECHO
                TokenString.append(c)
            else:
                currentToken = tp.ERROR
                state = States.HECHO
                consume = False
        elif state == States.EMAS:
            if c == "+":
                currentToken = tp.PLUSP
                state = States.HECHO
                TokenString.append(c)
            else:
                currentToken = tp.PLUS
                state = States.HECHO
                consume = False        
        elif state == States.EMENOS:
                if c == "-":
                    currentToken = tp.LESSL
                    state = States.HECHO
                    TokenString.append(c)
                else : 
                    currentToken = tp.MINUS
                    state = States.HECHO
                    consume = False 
        elif state == States.EPCOMM:
            if c == "/":
                TokenString.clear()      
                c = getNextChar()
                while c !='\n':
                    c = getNextChar()
                #    
                state = States.INICIO
                consume = True
            elif c == "*":
                TokenString.clear()      
                state = States.EPCOMMMULTI
                consume =True
            else : 
                currentToken = tp.OVER
                state = States.HECHO
                consume = False
        elif state == States.EPCOMMMULTI:
            if c == "*":
                state = States.ECOMMMULTI
            elif c == "EOF":
                state = States.HECHO
                currentToken = tp.ERROR
            else:
                pass 
        elif state == States.ECOMMMULTI:
            if c == "/":
                state = States.INICIO
            elif c == "*":
                pass
            elif c == "EOF":
                currentToken = tp.ERROR
                state = States.HECHO
            else:
                state = States.EPCOMMMULTI  
        elif state == States.ESTRING:
            if c.isdigit() or c == "_" or c == ":" or c == " "  or c == "\\" or c.isalnum() and c != "EOF" : 
                TokenString.append(c)
            else:
                if(c == "\""):
                    TokenString.append(c)
                    currentToken = tp.STRING 
                    state = States.HECHO 
                    consume = True
                else:
                    currentToken = tp.ERROR
                    state = States.HECHO
                    consume = True
    printToken(currentToken,"".join(TokenString))
    TokenString.clear()
    return currentToken

while getToken() != tp.ENDFILE:
    pass
fileoutput.close()
fileoutputError.close()
fileoutput2.close()