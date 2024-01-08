This file explains the code used for the interpreter.

## Argument types
AMA has different types of arguments, in the code represented by integers:

| Name | Code | Integer | Max Value |
| ---- | ---- | ------- | --------- |
| Register | :r | 1 | 255 |
| Memory   | %radr | 2 | 4,294,967,296 (2^32) |
| Value (Memory) | $val | 3 | 255 |
| Value (Register) | !val | 4 | 4,294,967,296 (2^32) |
| External | :rop | 4 | 4 |

## Errors
AMA has some own errors.

### `AMARegisterError`
This error occurs when:
- it's tried to change register 0
- it's tried to change register 256+ (not existing)

### `AMASyntaxError`
This is not implemented yet.

### `AMACommandError`
This error is thrown when:
- an unknown command is used
- not enough arguments were given
- wrong argument type were given

## Warnings
There are also some warnings, which don't stop the program:

### `AMACommandWarning`
This warning is Thrown, when:
- too many arguments were given

## Functions

### `checkSyntax(lines: list)`
This function checks the syntax of the given lines.
It throws errors or warnings in case of wrong code.

## Other classes
### `Memory`
This class represents the memory (also the register) with a dictionary as values.
#### Attributes
- `values: dict`: The values saved in the memory (or register)
#### Methods
- `setValue(nr: int, value: int)`: Sets the `nr`th Element of the `values` dict to `nr`
- `getValue(nr: int) -> int`: Returns the `nr`th element of the `values` dict or 0 if not set.

### `Stack`
This class represents a stack.
#### Attributes
- `values: list`: A list of the values (with the first element at 0)
#### Methods
- `push(value: int)`: Appends `value` to `values`
- `pop() -> int`: Returns `values`' last element and removes it