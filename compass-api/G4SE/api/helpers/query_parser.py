import operator

from django.contrib.postgres.search import SearchQuery

from grako.model import ModelBuilderSemantics

from api.helpers import search_query


class MySearchQuery(SearchQuery):
    def __repr__(self):
        s = super().__repr__()
        if self.invert:
            s = "!{}".format(s)
        return s
SearchQuery = MySearchQuery


class SearchSemantics(ModelBuilderSemantics):
    def start(self, ast):
        return ast

    def search_query(self, ast):
        return ast

    def combined_query(self, ast):
        left_operator, operation, right_operator = ast
        return operation(left_operator, right_operator)

    def parenthesized_query(self, ast):
        print(ast)
        return ast

    def BIN_OP(self, ast):
        return ast

    def left_paren(self, ast):
        pass

    def right_paren(self, ast):
        pass

    def search_term(self, ast):
        if isinstance(ast, list) and len(ast) == 2:
            operation, argument = ast
            return operation(argument)
        return ast

    def search_word(self, ast):
        return SearchQuery(ast)

    def quoted_string(self, ast):
        # unquote and un-escape
        return ast[1:-1].encode().decode('unicode_escape')

    def literal_search_word(self, ast):
        return ast

    def and_op(self, ast):
        return operator.and_

    def OR_OP(self, ast):
        return operator.or_

    def pipe(self, ast):
        return ast

    def unary_op(self, ast):
        return operator.inv


if __name__ == "__main__":
    def test(s, expected_tokens, expected_value=None):
        val = search_query.UnknownParser().parse(s)
        # print(json.dumps(val, indent=2))
        if val == expected_tokens:
            print('SUCCESS: ', s, "=", val)
        else:
            print("FAIL: in: ", s, "result: ", val, "!=", expected_tokens)

        if expected_value is not None:
            val = search_query.UnknownParser().parse(s, semantics=SearchSemantics())

            if str(val) == str(expected_value):
                print('SUCCESS: ', s, "=", val)
            else:
                print("FAIL: in: ", s, "result: ", val, "!=", expected_value)


    test('a', 'a', SearchQuery('a'))
    test('foo', 'foo', SearchQuery('foo'))
    test('a&b', ['a', '&', 'b'], SearchQuery('a') & SearchQuery('b'))
    test('!a', ['!', 'a'], ~SearchQuery('a'))
    test('!a&b', ['!', 'a', '&', 'b'], (~SearchQuery('a')) & SearchQuery('b'))
    test('a & b', ['a', '&', 'b'], SearchQuery('a') & SearchQuery('b'))
    test('! a', ['!', 'a'], ~SearchQuery('a'))
    test('! a & b', ['!', 'a', '&', 'b'], (~SearchQuery('a')) & SearchQuery('b'))
    test("'a & (!b | !c) & d | e'", "'a & (!b | !c) & d | e'", SearchQuery("a & (!b | !c) & d | e"))
    test('"a & (!b | !c) & d | e"', '"a & (!b | !c) & d | e"', SearchQuery("a & (!b | !c) & d | e"))
    test('""', '""', SearchQuery(""))
    test("''", "''", SearchQuery(""))
    test("'\"'", "'\"'", SearchQuery('"'))
    test('"\'"', '"\'"', SearchQuery("'"))
    test(r"'\''", r"'\''", SearchQuery("'"))
    test('a b', ['a', ' ', 'b'], SearchQuery('a') | SearchQuery('b'))
    test('a  b', ['a', ' ', 'b'], SearchQuery('a') | SearchQuery('b'))
    test('a\t b', ['a', '\t', 'b'], SearchQuery('a') | SearchQuery('b'))
    test('a \tb', ['a', ' ', 'b'], SearchQuery('a') | SearchQuery('b'))
    test('foo  bar', ['foo', ' ', 'bar'], SearchQuery('foo') | SearchQuery('bar'))
    test("(a)", 'a', SearchQuery('a'))
    test("((a))", 'a', SearchQuery('a'))
    test("(a & b)", ['a', '&', 'b'], SearchQuery('a') & SearchQuery('b'))
    test("a & (b & c)", ['a', '&', ['b', '&', 'c']], SearchQuery('a') & (SearchQuery('b') & SearchQuery('c')))
    test("(a | b) & (c | b)", [['a', '&', 'b'], '|', ['c', '&', 'd']], (SearchQuery('a') & SearchQuery('b')) | (SearchQuery('c') & SearchQuery('d')))
    # test("a", SearchQuery('a'))
    # test("!a", ~SearchQuery('a'))
    # # test("!!a", SearchQuery('a'))  # error expected!
    # test("a & b & c", SearchQuery('a') & SearchQuery('b') & SearchQuery('c'))
    # test("a & !b & c", SearchQuery('a') & ~SearchQuery('b') & SearchQuery('c'))
    # test("a | b | c", SearchQuery('a') | SearchQuery('b') | SearchQuery('c'))
    # test("a | !b | c", SearchQuery('a') | ~SearchQuery('b') | SearchQuery('c'))
    # test("a & !b | !c & d | e", SearchQuery('a') & ~SearchQuery('b') | ~SearchQuery('c') & SearchQuery('d') | SearchQuery('e'))
    test(
        "a & (!b | !c) & d | e", ['a', '&', '!', 'b', '|', '!', 'c', '&', 'd', '|', 'e'],
        SearchQuery('a') & (~SearchQuery('b') | ~SearchQuery('c')) & SearchQuery('d') | SearchQuery('e')
    )
    test(
        "!'a & (!b | !c) & d | e' & f | k", ['!', "'a & (!b | !c) & d | e'", '&', 'f', '|', 'k'],
        ~SearchQuery('a & (!b | !c) & d | e') & SearchQuery('f') | SearchQuery('k')
    )
