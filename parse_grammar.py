import codecs, pprint

with codecs.open('GRAMMAR', 'r', encoding="utf8") as file:
    cts = file.read()

eof = '\0'
cts += eof
pos = 0
char = 1
line = 1

def peek():
    return cts[pos]

def pop():
    global pos, line, char
    c = peek()
    pos += 1
    char += 1
    if peek() == '\n':
        line += 1
        char = 0
    return c

def expect(s):
    for c in s:
        if pop() != c:
            raise RuntimeError(f"unexpected char '{peek()}', expected '{c}', at line {line}, char {char}")

def isprint(c):
    return not c.isspace()

def parse_name():
    name = ''
    while peek() != ':' and isprint(peek()):
        name += pop()
    assert(len(name) >= 1)
    return name

def parse_token():
    token = ''
    optional = False
    while isprint(peek()):
        token += pop()
    if token.endswith('_opt'):
        token = token[:-4]
        optional = True
    return token, optional

def parse_production():
    expect('    ')
    tokens = []
    while True:
        tokens.append(parse_token())
        if peek() == ' ':
            pop()
        else:
            expect('\n')
            return tokens

def parse_rule():
    name = parse_name()
    expect(':\n')
    productions = []
    while peek() == ' ':
        productions.append(parse_production())
    if peek() != eof:
        expect('\n')
    return (name, productions)

def parse_grammar():
    rules_list = []
    while peek() != eof:
        rules_list.append(parse_rule())

    nrules = len(rules_list)

    for x in range(nrules):
        for y in range(x+1, nrules):
            if rules_list[x][0] == rules_list[y][0]:
                raise RuntimeError(f"Duplicate rule: {rules_list[x][0]}")

    rules = {}

    for rule in rules_list:
        rules[rule[0]] = rule[1]

    terminals = set()

    forward_references = {}
    reverse_references = {}

    for rule, productions in rules.items():
        for production in productions:
            for token, optional in production:
                if token not in rules:
                    terminals.add(token)
                else:
                    if rule not in forward_references:
                        forward_references[rule] = set()
                    forward_references[rule].add(token)

                    if token not in reverse_references:
                        reverse_references[token] = set()
                    reverse_references[token].add(rule)

    expected_terminals = { '|', '%=', 'assert', '&', 'raise', 'not',
        'while', 'with', 'NAME', '**', 'from', '<=',
        '&=', '@=', '//=', ';', 'nonlocal', 'if',
        'yield', 'False', '=', 'STRING', '!=',
        'elif', '<<=', 'continue', ')', 'or',
        'finally', '==', '...', '-=', 'lambda',
        'NUMBER', '()', ']', 'and', '%', '/=',
        'for', '**=', 'DEDENT', '^', 'as', '<<',
        'global', 'return', 'in', '(', ',', '/', '>>',
        '->', '}', '.', '>=', '[', '+=', 'break',
        'ENDMARKER', 'None', '*=', '^=', '<>', '*',
        '{', '>>=', 'try', 'is', 'class', 'def', '//',
        ':', 'else', '@', '<', '>', 'await', 'import',
        'pass', '~', 'async', 'NEWLINE', 'True', '|=',
        '-', '+', 'del', 'INDENT', 'except'}

    if terminals != expected_terminals:
        raise RuntimeError(f'bad terminals: unknown = {terminals - expected_terminals}, expected = {expected_terminals - terminals}');

    visited = set()
    to_visit = {'single-input', 'eval-input', 'file-input'}

    while len(to_visit) > 0:
        visiting = to_visit.pop()
        visited.add(visiting)
        if visiting not in forward_references:
            continue
        for reference in forward_references[visiting]:
            if reference not in visited:
                to_visit.add(reference)

    for rule, productions in rules.items():
        if rule not in visited:
            raise RuntimeError(f"unreachable rule {rule}")

    return rules, reverse_references

rules, reverse_references = parse_grammar()

print('digraph {')
for rule, references in reverse_references.items():
    for reference in references:
        print(f'    "{reference}" -> "{rule}"')
print('}')
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(reverse_references)
