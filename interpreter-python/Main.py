import sys

class AMAError(Exception):
    def __init__(self, line, text):
        self.line = line
        self.text = text
    
    def __str__(self):
        return self.text

class AMARegisterError(AMAError):
    pass

class AMASyntaxError(AMAError):
    pass

class AMACommandError(AMAError):
    pass

class AMAWarning(Warning):
    def __init__(self, line, text):
        self.line = line
        self.text = text
    
    def __str__(self):
        return self.text
    
class AMACommandWarning(AMAWarning):
    pass

class Memory:
    def __init__(self):
        self.values = dict()

    def setValue(self, nr, value):
        self.values[nr] = value

    def getValue(self, nr):
        return self.values[nr] if nr in self.values else 0

class Stack:
    def __init__(self):
        self.values = []
    def push(self, value):
        self.values.append(value)
    def pop(self):
        return self.values.pop()

def add(r1, r2, r3):
    reg.setValue(r3, reg.getValue(r1)+reg.getValue(r2))

def sub(r1, r2, r3):
    reg.setValue(r3, reg.getValue(r1)-reg.getValue(r2))

def mult(r1, r2, r3):
    reg.setValue(r3, reg.getValue(r1)*reg.getValue(r2))

def lr():
    raise AMACommandWarning(None, "Not yet implemented")
lm = lr

def mov(r1, r2):
    reg.setValue(r2, reg.getValue(r1))
    reg.setValue(r1, 0)

def _set(r, val):
    reg.setValue(r, val)

def cmov(r1, r2):
    if flag:
        reg.setValue(r2, reg.getValue(r1))

setm = lr

def nf():
    flag = not flag

def sfl(r1, r2):
    flag = reg.getValue(r1) < reg.getValue(r2)

def sfg(r1, r2):
    flag = reg.getValue(r1) > reg.getValue(r2)

def sfe(r1, r2):
    flag = reg.getValue(r1) == reg.getValue(r2)
    
ext = lm

flag = False
reg = Memory()
mem = Memory()
stack = Stack()
commandFuncs = {"push":stack.push, "pop":stack.pop, "add":add, "sub":sub, "mult":mult, "lr":lr, "lm":lm, "mov":mov, "set":_set, "cmov":cmov, "setm":setm, "nf":nf, "sfl":sfl, "sfg":sfg, "sfe":sfe, "ext":ext}
# commands = ["push pop add sub mult lr lm mov set cmov setm nf sfl sfg sfe ext".split()]
commands = {"push":(1,), "pop":(1,), "add":(1, 1, 1), "sub":(1, 1, 1), "mult":(1, 1, 1), "lr":(1, 2), "lm":(2, 1), "mov":(1, 1), \
                   "set":(1, 4), "cmov":(1, 1), "setm":(2, 3), "nf":(), "sfl":(1, 1), "sfg":(1, 1), "sfe":(1, 1), "ext":(5, 1)} # for each element of command a tuple of integers with argument types (see doc)
argTypes = {1:(":", 255), 2:("%", 4_294_967_296), 3:("$", 255), 4:("!", 4_294_967_296), 5:("%", 4)}
argTypeNames = {1:"register address", 2:"memory address", 3:"memory value", 4:"register value", 5:"external command"}
def checkSyntax(lines):
    """
    Checks the Syntax of `lines` and returns the lines split as command and params.
    """
    instructions = []
    for index, i in enumerate(lines):
        i = i.strip() # remove whitespaces at beginning and end
        if i == "": # empty line
            continue
        if i.startswith(";"): # lines starting with ; are comments
            continue 
        instruction = i.split(";")[0].split() # Remove comments with ; and seperate parameters
        instruction[0] = instruction[0].lower()
        command = instruction[0]         # command
        args = instruction[1:]           # args got
        argsGot = len(args)              # number of args got
        argsExp = len(commands[command]) # number of args expected

        if instruction[0] not in commands:
            raise AMACommandError(index+1, f"Unknown command: {command}")
        
        if argsGot < argsExp:
            raise AMACommandError(index+1, f"Expected {argsExp} arguments but got {argsGot}")
        if argsGot > argsExp:
            raise AMACommandWarning(index+1, f"Too many arguments: {argsGot} instead of {argsExp}. Ignoring last one(s): {', '.join(args[argsGot+1-argsExp:])}")
        
        for jindex, j in enumerate(args):
            
            aTExp = commands[command][jindex] # number of arg tyoe expected
            aTGot = j[0] # char (:, !) of argType got
            try:
                aVal = int(j[1:], 16)
            except ValueError:
                raise AMACommandError(index+1, f"Invalid value for argument nr. {jindex+1}: {aVal}")

            if argTypes[aTExp][0] != aTGot:
                raise AMACommandError(index+1, f"Argument nr. {jindex+1} must be {argTypeNames[aTExp]}")
            
            if aVal > argTypes[aTExp][1]:
                raise AMACommandError(index+1, f"Too high value for argument nr. {jindex+1}: {aVal}")
    
    return instructions

def parseLine(line):
    print(line)

def parseLines(lines):
    try:
        instructions = checkSyntax(lines)
        nInstructions = len(instructions)
        print(instructions, nInstructions)
        while True:
            if reg.getValue(0) >= nInstructions:
                exit(0)
            result = parseLine(instructions[reg.getValue(0)])
            if result != None:
                reg.setItem(0, result)
            else:
                reg.setItem(0, reg.getValue(0)+1)
    except AMAError as err:
        if err.line == None:
            err.line = reg.getValue(0)
        print(f"\033[31m{err.__class__.__name__}: Line {err.line}: {err.text}\033[0m")
        exit(1)
    except AMAWarning as warn:
        if warn.line == None:
            warn.line = reg.getValue(0)
        print(f"\033[33m{warn.__class__.__name__}: Line {warn.line}: {warn.text}\033[0m")
        
version = "0.3.0"
specVersion = "1.4"


if len(sys.argv) < 2:
    print(f"AMA interpreter (Python) {version} (for spec version {specVersion})\nCopyright (c) CleverLemming1337")
    while True:
        parseLines([input("AMA CLI >>> ")])
else:
    with open(sys.argv[1], "r") as f:
        parseLines(f.readlines())

