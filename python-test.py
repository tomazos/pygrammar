# chained-assignment
# tuple-expression : ternary-expression
# tuple-expression : ternary-expression = ternary-expression
# tuple-expression augmented-assignment-operator yield-expression
# tuple-expression augmented-assignment-operator expression-list-ternary
# del-statement
# pass-statement
# flow-statement
# import-statement
# global-statement
# nonlocal-statement
# assert-statement

x = 3
x += 2
assert(x == 5)
x -= 2
assert(x == 3)
x *= 4
assert(x == 12)
x /= 4
assert(x == 3)
x %= 2
assert(x == 1)
x = 7
x &= 8 + 1 + 4
assert(x == 5)
x |= 4 + 8
assert(x == 13)
x ^= 10
assert(x == 7)
x <<= 2
assert(x == 28)
x >>= 2
assert(x == 7)
x **= 2
assert(x == 49)
x /= 10
assert(x == 4.9)
x = 19
x //= 5
assert(x == 3)

class C:

# @=
#     /=
#     %=
#     &=
#     |=
#     ^=
#     <<=
#     >>=
#     **=
#     //=

