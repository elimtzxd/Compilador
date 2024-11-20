from code_ import *
from globall import NodeKind,StmtKind,TreeNode, ExpKind, TokenType
from symtab import st_lookup
tmpOffset = 0

def genStmt(tree:TreeNode):
    global ac,ac1,pc,mp,gp,TraceCode
    p1, p2, p3 = None, None, None
    savedLoc1, savedLoc2, currentLoc = 0, 0, 0
    loc = 0
    if tree.kind == StmtKind.IFK.value:
        if TraceCode:
            emitComment("-> if")
        p1 = tree.child[0]
        p2 = tree.child[1]
        p3:TreeNode = tree.child[2]
        
        cGen(p1)
        savedLoc1 = emitSkip(1)
        emitComment("if: jump to else belongs here")
        
        cGen(p2)
        savedLoc2 = emitSkip(1)
        emitComment("if: jump to end belongs here")
        currentLoc = emitSkip(0)
        emitBackup(savedLoc1)
        emitRM_Abs("JEQ", ac, currentLoc, "if: jmp to else")
        emitRestore()
        if p3 != None:
            print(f"kind {p3.kind} kindNode {p3.getNodeKind()}")
            p3 = p3.child[0]
        cGen(p3)
        currentLoc = emitSkip(0)
        emitBackup(savedLoc2)
        emitRM_Abs("LDA", pc, currentLoc, "jmp to end")
        emitRestore()
        if TraceCode:
            emitComment("<- if")
    elif tree.kind == StmtKind.UNTILK.value:
        if TraceCode:
            emitComment("-> do until")
        p1 = tree.child[0]
        p2 = tree.child[1]
        savedLoc1 = emitSkip(0)
        emitComment("repeat: jump after body comes back here")
        cGen(p1)
        cGen(p2)
        emitRM_Abs("JEQ", ac, savedLoc1, "repeat: jmp back to body")
        if TraceCode:
            emitComment("<- do until")

    elif tree.kind == StmtKind.WHILEK.value:
        if TraceCode:
            emitComment("-> while")
        p1 = tree.child[0]
        p2 = tree.child[1]
        savedLoc1 = emitSkip(0)
        emitComment("while: jump after body comes back here")
        cGen(p1)
        saveLoc2 = emitSkip(1)
        cGen(p2)
        cGen(p1)
        emitRM_Abs("JNE", ac, savedLoc1, "while: jmp back to exp")
        currentLoc = emitSkip(0)
        emitBackup(saveLoc2)
        
        emitRM_Abs("JEQ", ac, currentLoc, "while: false")
        emitRestore()


            
        if TraceCode:
            emitComment("<- while")
    elif tree.kind == StmtKind.CINK.value:
        emitRO("IN",ac,0,0,"read integer value");
        loc = st_lookup(tree.attr);
        emitRM("ST",ac,loc,gp,"read: store value");
    elif tree.kind == StmtKind.COUTK.value:
        #generate code for expression to write */
        if(tree.child[0].nodekind.value == NodeKind.EXPK.value and tree.child[0].kind == ExpKind.STRINGK.value):
            emitRO("OUTS",tree.child[0].attr,0,0,"write str")    
        else:
            cGen(tree.child[0])
            #now output it */
            emitRO("OUT",ac,0,0,"write ac")  
    elif tree.kind == StmtKind.ASSIGNS.value:
        if TraceCode:
            emitComment("-> assign")
        
        cGen(tree.child[0])
        
        loc = st_lookup(tree.attr)
        emitRM("ST", ac, loc, gp, "assign: store value")
        
        if TraceCode:
            emitComment("<- assign")
    elif tree.kind == StmtKind.MAINK.value:
        cGen(tree.child[0])



def genExp(tree:TreeNode):
    global tmpOffset,TraceCode,ac,ac1,pc,mp,gp
    loc = 0
    p1, p2 = None, None
    if tree.kind == ExpKind.CONSTFK.value:
        if TraceCode: 
            emitComment("-> Const")
        emitRM("LDF",ac,tree.attr,0,"load const") # LDF es una carga de una constante REAL (Float)
        if TraceCode: 
            emitComment("<- Const")

        pass
    elif tree.kind == ExpKind.CONSTIK.value:
        if TraceCode: 
            emitComment("-> Const")

        emitRM("LDC",ac,tree.attr,0,"load const")
        if TraceCode: 
            emitComment("<- Const")

    elif tree.kind == ExpKind.IDK.value:
        if TraceCode:
            emitComment("-> Id")
        loc = st_lookup(tree.attr)
        emitRM("LD",ac,loc,gp,"load id value")
        if TraceCode:
            emitComment("<- Id")

    elif tree.kind == ExpKind.OPK.value: # Start OpK
        if TraceCode:
            emitComment("-> Op")
        p1 = tree.child[0]
        p2 = tree.child[1]

        cGen(p1)

        emitRM("ST",ac,tmpOffset,mp,"op: push left") # tmpOffset--
        tmpOffset-=1
        
        cGen(p2)
        
        tmpOffset += 1
        emitRM("LD",ac1,tmpOffset,mp,"op: load left") # ++tmpOffset

        if ( tree.attr == TokenType.PLUS.value):
            emitRO("ADD",ac,ac1,ac,"op +")
        

        elif tree.attr == TokenType.MINUS.value:
            emitRO("SUB",ac,ac1,ac,"op -")
        
        elif tree.attr == TokenType.TIMES.value:
            emitRO("MUL",ac,ac1,ac,"op *")
        
        elif tree.attr == TokenType.OVER.value:
            emitRO("DIV",ac,ac1,ac,"op /")
        
        elif tree.attr == TokenType.RES.value:
            emitRO("RES",ac,ac1,ac,"op %")

        elif tree.attr == TokenType.LESST.value:
            emitRO("SUB",ac,ac1,ac,"op <")
            emitRM("JLT",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp") 
            emitRM("LDC",ac,1,ac,"true case")

        elif tree.attr == TokenType.LESSET.value:
            emitRO("SUB",ac,ac1,ac,"op <=")
            emitRM("JLE",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp") 
            emitRM("LDC",ac,1,ac,"true case")
        
        elif tree.attr == TokenType.EQ.value:
            emitRO("SUB",ac,ac1,ac,"op =")
            emitRM("JEQ",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp")
            emitRM("LDC",ac,1,ac,"true case")

        elif tree.attr == TokenType.GREATERT.value:
            emitRO("SUB",ac,ac1,ac,"op >")
            emitRM("JGT",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp") 
            emitRM("LDC",ac,1,ac,"true case")

        elif tree.attr == TokenType.GREATERET.value:
            emitRO("SUB",ac,ac1,ac,"op >=")
            emitRM("JGE",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp")
            emitRM("LDC",ac,1,ac,"true case")

        elif tree.attr == TokenType.DIFF.value:
            emitRO("SUB",ac,ac1,ac,"op <>")
            emitRM("JNE",ac,2,pc,"br if true")
            emitRM("LDC",ac,0,ac,"false case")
            emitRM("LDA",pc,1,pc,"unconditional jmp")
            emitRM("LDC",ac,1,ac,"true case")

        else:
            emitComment("BUG: Unknow operator")

        if TraceCode:
            emitComment("<- Op")
        
        # OpK end



def codeGen(syntaxTree:TreeNode, codefile):
    global mp,ac,pc
    
    s = "File: " + codefile
    openFile(codefile)
    emitComment("TINY Compilation to TM Code")
    emitComment(s)
    
    emitComment("Standard prelude:")
    emitRM("LD", mp, 0, ac, "load maxaddress from location 0")
    emitRM("ST", ac, 0, ac, "clear location 0")
    emitComment("End of standard prelude.")
    cGen(syntaxTree)
    emitComment("End of execution.")
    emitRO("HALT", 0, 0, 0, "")
    closeFile()



def cGen(tree:TreeNode):
    if tree is not None:
        if tree.nodekind.value == NodeKind.STMTK.value:
            genStmt(tree)
        elif tree.nodekind.value == NodeKind.EXPK.value:
            genExp(tree)
        cGen(tree.sibling)

