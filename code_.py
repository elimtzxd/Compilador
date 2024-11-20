
pc = 7

mp = 6

gp = 5

ac = 0

ac1 = 1
#endif

code = None

TraceCode = True
emitLoc = 0
highEmitLoc = 0
def emitComment(c):
        
    global emitLoc,highEmitLoc,TraceCode,code
    if TraceCode:
        code.write("* %s\n" % c)

def emitRO(op, r, s, t, c):
        
    global emitLoc,highEmitLoc,TraceCode,code
    code.write("%3d:  %5s  %s,%s,%s " % (emitLoc, op, r, s, t))
    emitLoc += 1
    if TraceCode:
        code.write("\t%s" % c)
    code.write("\n")
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc

def emitRM(op, r, d, s, c):
        
    global emitLoc,highEmitLoc,TraceCode,code
    code.write("%3d:  %5s  %s,%s(%s) " % (emitLoc, op, r, d, s))
    emitLoc += 1
    if TraceCode:
        code.write("\t%s" % c)
    code.write("\n")
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc

def emitSkip(howMany):
        
    global emitLoc,highEmitLoc,TraceCode,code
    i = emitLoc
    emitLoc += howMany
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc
    return i

def emitBackup(loc):
        
    global emitLoc,highEmitLoc,TraceCode,code
    if loc > highEmitLoc:
        emitComment("BUG in emitBackup")
    emitLoc = loc

def emitRestore():
        
    global emitLoc,highEmitLoc,TraceCode,code
    emitLoc = highEmitLoc

def emitRM_Abs(op, r, a, c):
        
    global emitLoc,highEmitLoc,TraceCode,code
    code.write("%3d:  %5s  %d,%d(%d) " % (emitLoc, op, r, a-(emitLoc+1), pc))
    emitLoc += 1
    if TraceCode:
        code.write("\t%s" % c)
    code.write("\n")
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc
def closeFile():
    global code
    code.close()
def openFile(fileName):
    global code
    code = open(fileName,"w")
