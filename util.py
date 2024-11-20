from globall import TokenType as tp,MAXCHILDREN
import globall
#from scan import reservedWords as rw
from globall import TreeNode,ExpKind,StmtKind,DecKind,NodeKind
import os
import json
from symtab import BucketList, LineList
fileoutput = open(os.path.join(os.getcwd(),'Archivo_Tokens.txt'),'r+')
#fileoutput.truncate()
fileoutputError = open(os.path.join(os.getcwd(),'Archivo_Errores.txt'),'r+')
#fileoutputError.truncate()
fileoutput2 = open(os.path.join(os.getcwd(),'Archivo_Tokens2.txt'),'r+')
#fileoutput2.truncate()
def printToken(token,tokenString):
 
    if (token in [tp.MAIN , tp.IF , tp.THEN , tp.ELSE
    , tp.END , tp.DO , tp.WHILE , tp.REPEAT
    , tp.UNTIL , tp.CIN , tp.COUT , tp.REAL
    , tp.INT , tp.BOOLEAN]) :
        print ( "RESERVED-WORD \t{0}".format(tokenString)+"\t{}\t  {}".format(globall.lineno,globall.colpos) )
        write ( "RESERVED-WORD\t{0}".format(tokenString),"\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.PLUS == token ):

        print( "PLUS\t+\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "PLUS\t+","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.MINUS == token ):
        print( "MINUS\t-\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "MINUS\t-","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.TIMES == token ):
        print( "TIMES\t*\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "TIMES\t*","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.OVER == token ):
        print( "OVER\t/\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "OVER\t/","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.RES == token ):
        print( "RES\t%\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "RES\t%","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.LESST == token ):
        print( "LESST\t<\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "LESST\t<","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.LESSET == token ):
        print( "LESSET\t<=\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "LESSET\t<=","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.GREATERT == token ):
        print( "GREATERT\t>\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "GREATERT\t>","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.GREATERET == token ):
        print( "GREATERET\t>=\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "GREATERET\t>=","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.EQ == token ):
        print( "EQ\t=\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "EQ\t=","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.DIFF == token ):
        print( "DIFF\t<>\t {}\t  {}".format(globall.lineno,globall.colpos) )       
        write( "DIFF\t<>","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif( token == tp.ASSIGN):
        print ( "ASSIGN\t:=\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write("ASSIGN\t:=","\t{}\t{}".format(globall.lineno,globall.colpos))
    elif ( tp.LPAREN == token ):
        print( "LPAREN\t(\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "LPAREN\t(","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.RPAREN == token ):
        print( "RPAREN\t)\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "RPAREN\t)","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.LBPAREN == token ):
        print( "LBPAREN\t{"+"\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "LBPAREN\t{","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.RBPAREN == token ):
        print( "RBPAREN\t"+"}"+"\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "RBPAREN\t"+"}","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.PLUSP == token ):
        print( "PLUSP\t++\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "PLUSP\t++","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.LESSL == token ):
        print( "LESSL\t--\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "LESSL\t--","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.COMMA == token ):
        print( "COMMA\t,\t {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "COMMA\t,","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.SEMMICOL == token ):
        print( "SEMMICOL\t;\t  {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "SEMMICOL\t;","\t{}\t{}".format(globall.lineno,globall.colpos) )
    elif ( tp.ID == token ):
        print( "ID\t {}\t  {}\t  {}".format(tokenString,globall.lineno,globall.colpos) )
        write( "ID\t{}".format(tokenString),"\t{}\t{}".format(globall.lineno,globall.colpos) )

    elif ( tp.ENTERO == token ):
        print( "ENTERO\t{0}".format(tokenString)+"\t  {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "ENTERO\t{0}".format(tokenString),"\t{}\t{}".format(globall.lineno,globall.colpos) )

    elif ( tp.NUMREAL == token ):
        print( "NUMREAL\t {0}".format(tokenString)+"\t  {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "NUMREAL\t{0}".format(tokenString),"\t{}\t{}".format(globall.lineno,globall.colpos))

    elif ( tp.ENDFILE == token ):
        print( "EOF" )
        #write( "EOF\t EOF","\t  {}\t  {}".format(globall.lineno,globall.colpos))
    elif ( tp.ERROR == token ):
        print( "Err  {}\t  {}\t  {}".format(tokenString,globall.lineno,globall.colpos) )
        writeErrores("Lexical Error:  {}  \t at line: {}\t and column: {}".format(tokenString,globall.lineno,globall.colpos))
    elif (tp.STRING == token):
        print( "STRING\t {0}".format(tokenString)+"\t  {}\t  {}".format(globall.lineno,globall.colpos) )
        write( "STRING\t{0}".format(tokenString),"\t{}\t{}".format(globall.lineno,globall.colpos))

    else:
        print("UNKNOWN TOKEN\t{}".format(tokenString))
        write("UNKNOWN TOKEN\t{}".format(tokenString))
        

def write(text,txt):
    try:
       
        # Procesamiento para escribir en el fichero
        fileoutput.write(text+"\n")
        fileoutput2.write(text+txt+"\n")
    except:
        pass
    finally:
        pass

def writeErrores(text):
    try:
       
        # Procesamiento para escribir en el fichero
        fileoutputError.write(text+"\n")
    except:
        pass
    finally:
        pass  

def newStmtNode(kind:StmtKind)->TreeNode:
 
    t = TreeNode(globall.lineno,NodeKind.STMTK,kind)
    return t
def newExpNode(kind:ExpKind)->TreeNode:
    
    t = TreeNode(globall.lineno,NodeKind.EXPK,kind)
    return t

indentno = 0
def increaseIn():
    global indentno
    indentno += 2
def decreaseIn():
    global indentno
    indentno -= 2
def printSpaces():
    global indentno
    i:int
    for i in range(0,indentno):
        print(f" ",end="")

def printTree( tree:TreeNode ):
    i:int
    increaseIn()
    while tree != None:
        printSpaces()
        if tree.getNodeKind().value == NodeKind.STMTK.value:
            if tree.getKind() == StmtKind.IFK.value:
                print("If: ") 
            elif tree.getKind() == StmtKind.ELSEK.value:
                print("Else: ")    
            elif tree.getKind() == StmtKind.UNTILK.value:
                print("Do until: ")
            elif tree.getKind() == StmtKind.WHILEK.value:
                print("While: ")
            elif tree.getKind() == StmtKind.ASSIGNS.value:
                print(f"Assign to: {tree.getAttr()}")
            elif tree.getKind() == StmtKind.CINK.value:
                print(f"Read: {tree.getAttr()}")
            elif tree.getKind() == StmtKind.COUTK.value:
                print(f"Write: ")
            elif tree.getKind() == StmtKind.DECK.value:
                print(f"Dec :")
            elif tree.getKind() == StmtKind.MAINK.value:
                print(f"Main :")
            elif tree.getKind() == StmtKind.TYPEDEF.value:
                print(f"Type : { globall.diccionario[tree.getAttr()]}")    
            else:
                print(f"Unknown Stmt Node ... {tree.getKind()}")
        elif tree.getNodeKind().value == NodeKind.EXPK.value:
            if tree.getKind() == ExpKind.OPK.value:
                print(f"Op: {globall.diccionario[tree.getAttr()]}")
            elif tree.getKind() == ExpKind.CONSTIK.value:
                print(f"Const Int: {tree.getAttr()}")
            elif tree.getKind() == ExpKind.CONSTFK.value:
                print(f"Const Float: {tree.getAttr()}")
            elif tree.getKind() == ExpKind.IDK.value:
                print(f"Id: {tree.getAttr()} ")
            elif tree.getKind() == ExpKind.STRINGK.value:
                print(f"String: {tree.getAttr()} ")
            else:
                print(f"Unknown ExpNode kind....")
        else:
            print("Unknown node kind...")
        for i in range(0,3):
            
            printTree(tree.getChild(i))
        tree = tree.getSibling()
    decreaseIn()

def printTreeSemantic( tree:TreeNode ):
    i:int
    increaseIn()
    while tree != None:
        printSpaces()
        if tree.getNodeKind().value == NodeKind.STMTK.value:
            if tree.getKind() == StmtKind.IFK.value:
                print("If: ") 
            elif tree.getKind() == StmtKind.ELSEK.value:
                print("Else: ")    
            elif tree.getKind() == StmtKind.UNTILK.value:
                print("Do until: ")
            elif tree.getKind() == StmtKind.WHILEK.value:
                print("While: ")
            elif tree.getKind() == StmtKind.ASSIGNS.value:
                print(f"Assign to: {tree.getAttr()} {tree.valueCalc}")
            elif tree.getKind() == StmtKind.CINK.value:
                print(f"Read: {tree.getAttr()}")
            elif tree.getKind() == StmtKind.COUTK.value:
                print(f"Write: ")
            elif tree.getKind() == StmtKind.DECK.value:
                print(f"Dec :")
            elif tree.getKind() == StmtKind.MAINK.value:
                print(f"Main :")
            elif tree.getKind() == StmtKind.TYPEDEF.value:
                print(f"Type : { globall.diccionario[tree.getAttr()]}")    
            else:
                print(f"Unknown Stmt Node ... {tree.getKind()}")
        elif tree.getNodeKind().value == NodeKind.EXPK.value:
            if tree.getKind() == ExpKind.OPK.value:
                print(f"Op: {globall.diccionario[tree.getAttr()]} - {tree.valueCalc}" )
            elif tree.getKind() == ExpKind.CONSTIK.value:
                print(f"Const Int: {tree.getAttr()} {tree.valueCalc}")
            elif tree.getKind() == ExpKind.CONSTFK.value:
                print(f"Const Float: {tree.getAttr()} {tree.valueCalc}")
            elif tree.getKind() == ExpKind.IDK.value:
                print(f"Id: {tree.getAttr()} ")
            elif tree.getKind() == ExpKind.STRINGK.value:
                print(f"String: {tree.getAttr()} ")
            else:
                print(f"Unknown ExpNode kind....")
        else:
            print("Unknown node kind...")
        for i in range(0,3):
            
            printTreeSemantic(tree.getChild(i))
        tree = tree.getSibling()
    decreaseIn()


def serialice(root:TreeNode)->dict:
    if root is None:
        return None
    return {
        "valor":root.getAttr(),
        "nodeKind":root.getNodeKind().value,
        "kind":root.getKind(),
        "type":root.getType(),
        "valCalc":root.valueCalc,
        "firstChild": serialice(root.getChild(0)),
        "secondChild":serialice(root.getChild(1)),
        "thirdChild": serialice(root.getChild(2)),
        "sibling"   : serialice(root.getSibling()), 
    }
