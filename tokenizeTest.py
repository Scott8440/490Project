import tokenize

with open('example.py', 'r') as s:
    g = tokenize.generate_tokens(s.readline)
    for toknum, tokval, a, b, c in g:
        print("{}, {}, {}, {}".format(toknum, tokval, a, b))
