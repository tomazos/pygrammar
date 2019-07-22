# pygrammar

GRAMMAR contains a rewrite of Python grammar in a better form:

 - one alternative per line
 - no kleene star or parens
 - `_opt` intead of `[]`
 - `_opt` only applies to single token
 - tokens are literal instead of being inside quotes
 - better rule names

`parse_grammar.py` is a verifier for GRAMMAR that checks:

 - terminals are what we expect / non-terminals refer to defined rules
 - no duplicate rule names
 - all rules are reachable from start rules by series of references (no unused rules)


