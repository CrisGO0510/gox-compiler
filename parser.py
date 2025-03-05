class Program:
    def __init__(self, statements):
        self.statements = statements

    def __repr__(self):
        return f'Program({self.statements})'
    

class Assignment:
    def __init__(self, location , expression):
        self.location  = location 
        self.expression  = expression 

    def __repr__(self):
        return f'Assignment({self.location }, {self.expression })'
    

class Vardecl:
    def __init__(self, id, type = None, expression = None):
        self.type = type
        self.expression = expression
        self.id = id


class IfStmt: 
    def __init__(self, expression, if_statement = [], else_statement = []):
        self.expression = expression
        self.if_statement = if_statement
        self.else_statement = else_statement


class WhileStmt:
    def __init__(self, expression, statement = []):
        self.expression = expression
        self.statement = statement


class BreakStmt:
    def __init__(self):
        pass


class ContinueStmt:
    def __init__(self):
        pass


class ReturnStmt:
    def __init__(self, expression):
        self.expression = expression


class PrintStmt:
    def __init__(self, expression):
        self.expression = expression


