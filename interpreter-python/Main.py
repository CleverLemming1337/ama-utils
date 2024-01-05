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

# commands = ["push pop add sub mult lr lm mov set cmov setm nf sfl sfg sfe ext".split()]
commands = {"push":(1,), "pop":(1,), "add":(1, 1, 1), "sub":(1, 1, 1), "mult":(1, 1, 1), "lr":(1, 2), "lm":(2, 1), "mov":(1, 1), \
                   "set":(1, 3), "cmov":(1, 1), "setm":(2, 3), "nf":(), "sfl":(1, 1), "sfg":(1, 1), "sfe":(1, 1), "ext":(4, 1)} # for each element of command a tuple of integers with argument types (see doc)
argTypes = {1:(":", 255), 2:(":", 4_294_967_296), 3:("!", 255), 4:("!", 4_294_967_296), 5:(":", 4)}
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
            raise AMACommandWarning(index+1, f"Too many arguments: {argsGot} instead of {argsExp}. Ignoring {', '.join(args[argsGot-argsExp:])}")
        
        for jindex, j in enumerate(args):
            aTExp = argTypes[command][0] # number of arg tyoe expected
            aTGot = j[0] # char (:, !) of argType got

            # if aTExp != aTGot:
            #     raise AMACommandError(index+1, f"Argument nr. {jindex+1} must be {argTypeNames[]}")

        


        
        
        