This file explains the code used for the interpreter.

## Argument types
AMA has different types of arguments, in the code represented by integers:

| Name | Code | Integer | Max Value |
| ---- | ---- | ------- | --------- |
| Register | :r | 1 | 255 |
| Memory   | :radr | 2 | 4,294,967,296 (2^32) |
| Value (Memory) | !val | 3 | 255 |
| Value (Register) | !val | 4,294,967,296 (2^32) |
| External | :rop | 4 | 4 |

## Errors
AMA has some own errors.

### `AMARegisterError`
This error occurs when:
- it's tried to change register 0
- it's tried to change register 256+ (not existing)

### `AMASyntaxError`