matched_parens = '(){}[]<>'
iparens = iter(matched_parens)
parens = dict(zip(iparens, iparens))
closing = parens.values()


def has_balanced_parentheses(input_string):
    stack = []
    for c in input_string:
        d = parens.get(c, None)
        if d:
            stack.append(d)
        elif c in closing:
            if not stack or c != stack.pop():
                return False
    return not stack
