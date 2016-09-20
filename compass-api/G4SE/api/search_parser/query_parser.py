import operator

from grako.model import ModelBuilderSemantics

from api.search_parser.patched_search_query import SearchQuery


class SearchSemantics(ModelBuilderSemantics):
    def __init__(self, *args, config='english', **kwargs):
        self.config = config
        super().__init__(*args, **kwargs)

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
        return SearchQuery(ast, config=self.config)

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
