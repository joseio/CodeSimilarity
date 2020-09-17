import pycparser.ply.lex as lex
import pycparser.ply.yacc as yacc
from functools import reduce
import z3
import re

from collections import defaultdict


# Splits input into tokens (Lex)
class SimpleLexer:
    tokens = (
        # 'NULL',
        'INT',  # instant values
        'REAL',
        'CHAR',
        'STRINGS',
        'LBRACK',  # Brackets
        'RBRACK',
        'LPAREN',
        'RPAREN',
        'VARIABLE',
        'DOT',  # Operators
        'ARROW',
        'SIZEOF',
        'GT',
        'GTE',
        'LT',
        'LTE',
        'EQ',
        'NEQ',
        'PLUS',
        'PLUSPLUS',
        'MINUS',
        'MINUSMINUS',
        'TIME',
        'DIVIDE',
        'LSHIFT',
        'RSHIFT',
        'BITAND',
        'BITOR',
        'BITXOR',
        'BITNOT',
        'OR',
        'AND',
        'NOT',
        'MODULO',
        'ASSIGN',
        'QM',
        'COLON',
        'BOOLT',
        'INTT',
        'REALT',
        'COMMA',
        'INTCASTOR',
        'INTARRCASTOR',
        'REALCASTOR',
        'BOOLCASTOR',
        'TOOBIG'
    )

    t_LBRACK = r'\['
    t_RBRACK = r'\]'
    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_DOT = r'\.'
    t_ARROW = r'\-\>'
    t_SIZEOF = r'sizeof'
    t_GT = r'\>'
    t_GTE = r'\>\='
    t_LT = r'\<'
    t_LTE = r'\<\='
    t_EQ = r'\=\='
    t_NEQ = r'\!\='
    t_PLUS = r'\+'
    t_PLUSPLUS = r'\+\+'
    t_MINUS = r'\-'
    t_MINUSMINUS = r'\-\-'
    t_TIME = r'\*'
    t_DIVIDE = r'\/'
    t_LSHIFT = r'\<\<'
    t_RSHIFT = r'\>\>'
    t_BITAND = r'\&'
    t_BITOR = r'\|'
    t_BITXOR = r'\^'
    t_BITNOT = r'\~'
    t_OR = r'\|\|'
    t_AND = r'\&\&'
    t_NOT = r'\!'
    t_MODULO = r'\%'
    t_ASSIGN = r'\='
    t_QM = r'\?'
    t_COLON = r'\:'
    t_BOOLT = r'bool'
    # t_NULL = r'null'
    t_INTT = r'(int|char|long|unsigned|short|uint|ulong|uchar|ushort|byte|sbyte)'
    t_REALT = r'(float|double)'
    t_COMMA = r','
    # Accounts for `int []` and `long int []`
    t_INTARRCASTOR = r'\([ \t\n]*(int|char|long|unsigned|short|uint|ulong|uchar|ushort|byte|sbyte)([ \t\n]*(int|char|long|unsigned|short|uint|ulong|uchar|ushort|byte|sbyte))*[ \t\n]*\[\][ \t\n]*\)'
    # Three lines below detect `(TYPE)` with any potential whitespace b/t parens
    t_INTCASTOR = r'\([ \t\n]*(int|char|long|unsigned|short|uint|ulong|uchar|ushort|byte|sbyte)([ \t\n]*(int|char|long|unsigned|short|uint|ulong|uchar|ushort|byte|sbyte))*[ \t\n]*\)'
    t_REALCASTOR = r'\([ \t\n]*(float|double)[ \t\n]*\)'
    t_BOOLCASTOR = r'\([ \t\n]*bool[ \t\n]*\)'
    t_TOOBIG = r'\([ \t\n]*expression too big[ \t\n]*\)'
    # t_UNICODE= r''
    # Exponent
    # t_EXPONENT = r'(int|uint|long|ulong|unsigned|short|ushort)\E[\+]*[\-]*(int|uint|long|ulong|unsigned|short|ushort)'
    # t_EXPONENT = r'(int|uint|long|ulong|unsigned|short|ushort)\E(int|uint|long|ulong|unsigned|short|ushort)'

    t_ignore = ' \t'

    def t_VARIABLE(self, t):
        r'[a-zA-Z_][a-zA-Z0-9_]*'
        table = {
            'bool': 'BOOLT',
            'int': 'INTT',
            'char': 'INTT',
            'unsigned': 'INTT',
            'long': 'INTT',
            'unsigned': 'INTT',
            'short': 'INTT',
            'uint': 'INTT',
            'ulong': 'INTT',
            'byte': 'INTT',
            'sbyte': 'INTT',
            'uchar': 'INTT',
            'ushort': 'INTT',
            'double': 'REALT',
            'float': 'REALT',
        }
        t.type = table.get(t.value, 'VARIABLE')
        return t

    # Error handling rule
    def t_error(self, t):
        print("Illegal character '%s', treating as string" % t.value[0])
        t.lexer.skip(1)
        return t

    def t_REAL(self, t):
        r'[+-]?((\d+)(\.\d+)([eE](\+|-)?(\d+))? | (\d+)[eE](\+|-)?(\d+))([lL]|[fF])?'
        t.value = float(t.value)
        return t

    def t_INT(self, t):
        r'[+-]?\d+([uU]|[lL]|[uU][lL]|[lL][uU])?'
        t.value = int(t.value.replace('u', '').replace(
            'U', '').replace('l', '').replace('L', ''))
        return t

    def t_CHAR(self, t):
        r"\'[^\|\.]\'"
        t.value = ord(str(t.value[1:-1]))
        return t

    def t_STRINGS(self, t):
        r'"[^"|\"]*"'
        t.value = str(t.value[1:-1])
        return t

    def __init__(self, **kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    def test(self):
        # data = 'a != (int[])null&&a[2] + a[3] < 4&&-51 < a[0]&&a[0] < 51&&-51 < a[1]&&a[1] < 51&&-51 < a[2]&&a[2] < 51&&a.Length == 3&&a[1] >= a[0]&&a[0] >= a[1]&&a[2] >= a[0]&&a[0] >= a[2]&&a[0] + a[2] * a[1]&&int s = a[0] - a[2]&&s > a[2] - a[1]&&(a[2]!=1 || a[2]!=4)&&4u < (uint)(1 + x)&&a[5] == \'c\'&&cmp("string", a)&&Math.floor(a[0])&&a[2] < a[1] ? a[0] % a[1] : a[1] % a[0]&&double s5 = 0.98&&s1 + -(double)((int)s0) != 0.49&&a[1] = (bool)a[2]'.split('&&')
        # data = 'a != (int[])null&&-101 < a[0]&&a[0] < 101&&-101 < a[1]&&a[1] < 101&&2 < a.Length&&-101 < a[2]&&a[2] < 101&&Math.Abs(0.33333333333333331 * (double)(a[0] + a[1] + a[2] + 1)) < 1E+16&&a.Length == 3L&&(a[0] != 13 || a[1] != -5)'.split('&&')
        a = 'return a != (int[])null&&-51 < a[0L]&&\\r\\n a[0L] < 51&&-51 < a[1L]&&a[1L] < 51&&-51 < a[2L]&&a[2L] < 51&&-51 < a[3L]&&\\r\\n a[3L] < 51&&-51 < a[4L]&&a[4L] < 51&&5L < a.Length&&-51 < a[5L]&&a[5L] < 51&&\\r\\n a[1L] < a[0L]&&a[4L] < a[3L]&&a[5L] < a[3L]&&a[4L] < a[2L]&&a[5L] < a[2L]&&\\r\\n a[4L] < a[0L]&&a[5L] < a[0L]&&a.Length == 6L&&a.Length == 6L&&a[2L] >= a[0L]&&\\r\\n a[3L] >= a[2L]&&a[0L] >= a[1L]&&a[4L] >= a[1L]&&a[5L] >= a[4L]&&a[0L] >= a[5L]'
        a = a.replace('\\r', '').replace('\\n', '').replace("\\'", "'").replace(
            'return', '').replace(';', '&&').replace('\\\\', '\\').strip().split('&&')
        data = a
        for d in data:
            self.lexer.input(d)
            print('\n---\ninput:', d)
            while True:
                tok = self.lexer.token()
                if not tok:
                    break
                print(tok)
        print('LEXER TEST FINISHED')


# Determines meaning of tokens and validates syntax (Yacc)
class SimpleParser:
    precedence = (
        ('left', 'ASSIGN'),
        ('right', 'QM', 'COLON'),
        ('left', 'OR'),
        ('left', 'AND'),
        ('left', 'BITOR'),
        ('left', 'BITXOR'),
        ('left', 'BITAND'),
        ('left', 'EQ', 'NEQ'),
        ('left', 'LT', 'GT', 'GTE', 'LTE'),
        ('left', 'LSHIFT', 'RSHIFT'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'TIME', 'DIVIDE', 'MODULO'),
        ('right', 'MINUS', 'PLUS', 'SIZEOF', 'NOT', 'BITNOT', 'PLUSPLUS', 'MINUSMINUS',
            'INTCASTOR', 'INTARRCASTOR', 'REALCASTOR', 'BOOLCASTOR'),            # Unary minus operator
        ('left', 'LBRACK', 'LPAREN', 'DOT', 'ARROW', 'PLUSPLUS', 'MINUSMINUS'),
    )

    type_switch = {
        'bool': z3.Bool,
        'uchar': z3.Int,
        'uint': z3.Int,
        'ulong': z3.Int,
        'byte': z3.Int,
        'sbyte': z3.Int,
        'ushort': z3.Int,
        'char': z3.Int,
        'int': z3.Int,
        'long': z3.Int,
        'short': z3.Int,
        'float': z3.Real,
        'double': z3.Real,
        'intArray': lambda x: z3.Array(x, z3.IntSort(), z3.IntSort()),
        'realArray': lambda x: z3.Array(x, z3.RealSort(), z3.IntSort()),
        'string': lambda x: z3.Array(x, z3.IntSort(), z3.IntSort()),
        # <-- No clue if correct (04/17/2020)
        'stringArray': lambda x: z3.Array(x, z3.IntSort(), z3.IntSort())
    }

    unary_ops = {
        '!': z3.Not,
        '-': lambda x: -x,
        '+': lambda x: +x,
        # TODO (?): INTARRCASTOR. Look into ArraySort().
        # 'INTARRCASTOR': lambda x: x if x.sort() != z3.ArraySort(z3.IntSort(), z3.IntSort()) else z3.Array(x, z3.IntSort(), z3.IntSort()),
        # 'INTARRCASTOR': None,
        # 'INTCASTOR': lambda x: x if x.sort() != z3.RealSort()  else z3.ToInt(x),
        'INTCASTOR': lambda x: x if isinstance(x, int) else (int(x) if isinstance(x, float) else (x if x.sort() != z3.RealSort() else z3.ToInt(x))),
        'REALCASTOR': lambda x: x if isinstance(x, float) else (float(x) if isinstance(x, int) else (x if x.sort() != z3.IntSort() else z3.ToReal(x)))
        # 'REALCASTOR': lambda x: x if x.sort() != z3.IntSort() else z3.ToReal(x)
    }

    binary_ops = {
        '>': lambda x, y: x > y,
        '>=': lambda x, y: x >= y,
        '<': lambda x, y: x < y,
        '<=': lambda x, y: x <= y,
        '==': lambda x, y: x == y,
        '!=': lambda x, y: x != y,
        '+': lambda x, y: x + y,
        '-': lambda x, y: x - y,
        '*': lambda x, y: x * y,
        '/': lambda x, y: x / y,
        '%': lambda x, y: x % y,
        '||': z3.Or,
        '&&': z3.And,
    }

    tokens = (
        # 'NULL',
        'INT',  # instant values
        'REAL',
        'CHAR',
        'STRINGS',
        'LBRACK',  # Brackets
        'RBRACK',
        'LPAREN',
        'RPAREN',
        'VARIABLE',
        'DOT',  # Operators
        'ARROW',
        'SIZEOF',
        'GT',
        'GTE',
        'LT',
        'LTE',
        'EQ',
        'NEQ',
        'PLUS',
        'PLUSPLUS',
        'MINUS',
        'MINUSMINUS',
        'TIME',
        'DIVIDE',
        'LSHIFT',
        'RSHIFT',
        'BITAND',
        'BITOR',
        'BITXOR',
        'BITNOT',
        'OR',
        'AND',
        'NOT',
        'MODULO',
        'ASSIGN',
        'QM',
        'COLON',
        'BOOLT',
        'INTT',
        'REALT',
        'COMMA',
        'INTCASTOR',
        'INTARRCASTOR',
        'REALCASTOR',
        'BOOLCASTOR',
        'TOOBIG'
    )

    def __init__(self, lexer, types, hooks=None, **kwargs):
        # self.parser = yacc.yacc(module=self, **kwargs)
        self.types = defaultdict(lambda: 'int')
        self.types.update(types)
        self.function_hooks = hooks if hooks else dict()
        self.lexer = lexer
        self.errored = False
        self.context = dict()
        self.parser = yacc.yacc(module=self, **kwargs)

    def p_end(self, p):
        """end : expr
               | empty
        """
        if len(p) == 2:
            self.result = p[1] if not self.errored else False
            # print('p[1], self.errored',p[1], self.errored)
            # print('result:', self.result, 'errored: ', self.errored)
            self.errored = False

    def p_types(self, p):
        """inttype : INTT
           realtype : REALT
           booltype : BOOLT
        """
        if len(p) == 2:
            p[0] = p[1]

    def p_leftv_expr(self, p):
        """expr : leftv
        """
        p[0] = p[1]

    def p_define_new(self, p):
        """leftv : inttype  VARIABLE
                 | realtype VARIABLE
                 | booltype VARIABLE
                 | leftv DOT VARIABLE
                 | VARIABLE
        """
        if p.slice[1].type == 'inttype':
            p[0] = z3.Int(p[2])
            p.slice[0].name = p[2]
            name = p[2]
            self.types[name] = 'int'
        elif p.slice[1].type == 'realtype':
            p[0] = z3.Real(p[2])
            p.slice[0].name = p[2]
            name = p[2]
            self.types[name] = 'double'
        elif p.slice[1].type == 'booltype':
            p[0] = z3.Bool(p[2])
            p.slice[0].name = p[2]
            name = p[2]
            self.types[name] = 'bool'
        elif len(p) == 2:
            if p[1] in self.context:
                p[0] = self.context[p[1]]
                p.slice[0].name = p[1]
                name = p[1]
                # print('{} in context, get {}'.format(name, p[0]))
            else:
                if p[1] not in self.types:
                    print(
                        'Warning: Type of {} is undefined, using default type: int'.format(p[1]))
                p[0] = self.type_switch[self.types[p[1]]](p[1])
                p.slice[0].name = p[1]
                name = p[1]
        elif len(p) == 4:
            var_name = '{}.{}'.format(p[1], p[3])
            if var_name not in self.types:
                print(
                    'Warning: Type of {} is undefined, using default type: int'.format(var_name))
            p[0] = self.type_switch[self.types[var_name]](var_name)
            p.slice[0].name = var_name
            name = var_name

        if len(p) > 2:
            self.context[name] = p[0]

    def p_variable_value(self, p):
        """expr : STRINGS
                | REAL
                | CHAR
                | INT
        """
        p[0] = p[1]

    def p_assign(self, p):
        """expr : leftv ASSIGN expr
        """
        key = getattr(p.slice[1], 'name')
        self.context[key] = p[3]
        p[1] = p[3]
        p[0] = True

    def p_expression(self, p):
        """expr : expr LBRACK expr RBRACK
                | LPAREN expr RPAREN
        """
        if len(p) == 4:  # binary ops, paren, element access
            if p.slice[2].type == 'binary_op':
                p[0] = self.binary_ops[p[2]](p[1], p[3])
            elif p.slice[1].type == 'LPAREN':
                p[0] = p[2]
        elif len(p) == 5:  # array access
            p[0] = p[1][p[3]]

    def p_qsmark_choice(self, p):
        """expr : expr QM expr COLON expr
        """
        p[0] = z3.If(p[1], p[3], p[5])
        print(p[1], p[3], p[5])

    def p_binary_ops(self, p):
        """expr : expr GT expr
                | expr GTE expr
                | expr LT expr
                | expr LTE expr
                | expr EQ expr
                | expr NEQ expr
                | expr PLUS expr
                | expr TIME expr
                | expr MINUS expr
                | expr DIVIDE expr
                | expr MODULO expr
                | expr OR expr
                | expr AND expr
        """
        if len(p) == 4:
            # print(p[1], p[3], p[2])
            p[0] = self.binary_ops[p[2]](p[1], p[3])
            # print(p[0])
        elif len(p) == 2:
            p[0] = p[1]

    def p_unary_ops(self, p):
        """expr : MINUS expr
                | NOT expr
        """
        p[0] = self.unary_ops[p[1]](p[2])

    def p_casting(self, p):
        """expr : INTCASTOR expr
                | INTARRCASTOR expr
                | REALCASTOR expr
                | BOOLCASTOR expr
        """
        p[0] = self.unary_ops[p.slice[1].type](p[2])

    def p_function(self, p):
        """expr : leftv LPAREN paramList RPAREN
           paramList : paramList COMMA expr
                     | expr
        """
        if len(p) == 5:
            # TODO: Add `Math.Abs()` checker here!!!!

            if str(p[1]) not in self.function_hooks:
                print(
                    'Function {} not found, treating as plain string'.format(p[1]))
            p[0] = self.function_hooks[str(p[1])](*p[3])
        elif len(p) == 4:
            p[0] = p[1] + [p[3], ]
        elif len(p) == 2:
            p[0] = [p[1], ]

    # def p_casting(self, p):
    #   """castor : LPAREN inttype RPAREN
    #             | LPAREN realtype RPAREN
    #   """
    #   if p.slice[2].type == 'inttype':
    #     p[0] = '2int'
    #   elif p.slice[2].type == 'realtype':
    #     p[0] = '2real'

    def p_empty(self, p):
        """empty :
        """
        pass

    def p_error(self, p):
        print("Syntax error, treating as string: {}".format(p))
        self.errored = True
        raise ValueError('Syntax error')

    def test(self, data):
        # data = 'a != (int[])null&&a[2] + a[3] < 4&&-51 < a[0]&&a[0] < 51&&-51 < a[1]&&a[1] < 51&&-51 < a[2]&&a[2] < 51&&a.Length == 3&&a[1] >= a[0]&&a[0] >= a[1]&&a[2] >= a[0]&&a[0] >= a[2]&&a[0] + a[2] * a[1]&&int s = a[0] - a[2]&&s > a[2] - a[1]&&(a[2]!=1 || a[2]!=4)&&4u < (uint)(1 + a[4])&&a[5] == \'c\'&&Math.floor(a[0])&&a[2] < a[1] ? a[0] % a[1] : a[1] % a[0]&&double s0 = 0.98&&s1 = 0.6&&s1 + -(double)((int)s0) != 0.49'.split('&&')
        # data = 'a != (int[])null&&-51 < a[0]&&a[0] < 51&&1 < a.Length&&-51 < a[1]&&a[1] < 51&&a[1] < a[0]&&a.Length == 2&&a[0] >= a[1]'.split('&&')
        # data = data.replace('\\r\\n', '')
        # data = data.split('&&')
        models = []
        errors = []
        toAdd = False  # Don't add the preamble
        for d in data:
            if not d:
                continue
            # print(d)
            try:
                # print(d)
                ret = self.parse(d)
                # print(ret)

                if type(ret) == z3.z3.ArithRef:
                    ret = z3.If(ret == 0, True, False)
            except (ValueError, KeyError) as e:
                ret = None
            except z3.z3types.Z3Exception as e:
                ret = None
                print('Z3 error', e)

            # Changed 'ret == False' -> 'ret is False' to avoid triggering int 0
            if ret is False or ret == None:
                errors.append(d)
            else:
                models.append(ret)
        # self.parser.clear_context()
        # Checks if all eles in `models` eval to True
        retVal = '&&'.join(sorted(errors)), z3.simplify(
            reduce(z3.And, models, True)) if len(models) > 0 else z3.BoolVal(True)
        return retVal

    def test2(self, data: list):
        results = []
        for d in data:
            print(d)
            try:
                self.parser.parse(d, lexer=self.lexer)
            except (ValueError, KeyError) as e:
                self.result = None
            except z3.z3types.Z3Exception as e:
                self.result = None
                print('Z3 error', e)
            # except ImportError as e:
                # pass
            print(self.result)
            self.errored = False
            print('-----')
            results.append(self.result)
        return results

    def parse(self, text):
        self.parser.parse(text, lexer=self.lexer.clone())
        return self.result

    def predParse(self, pred):
        models = []
        errors = []
        try:
            ret = self.parse(pred)
            if type(ret) == z3.z3.ArithRef:
                ret = z3.If(ret == 0, True, False)
        except (ValueError, KeyError) as e:
            ret = None
        except z3.z3types.Z3Exception as e:
            ret = None
            print('Z3 error', e)

        # Changed 'ret == False' -> 'ret is False' to avoid triggering int 0
        if ret is False or ret == None:
            errors.append(pred)
        else:
            models.append(ret)
        # Checks if all eles in `models` eval to True
        retVal = '&&'.join(sorted(errors)), z3.simplify(
            reduce(z3.And, models, True)) if len(models) > 0 else z3.BoolVal(True)
        return retVal[1]

    def clear_context(self):
        self.context = dict()


if __name__ == "__main__":
    from config import *
    import re

    def cleanInteriorAnd(pc):
        # Don't split the preamble expressions by '&&'
        expressions = pc.split(';')
        preamble = []
        for expr in expressions:
            if set(expr.split()) & set(TYPES.keys()):
                preamble += [expr]
            else:
                truePC = expr
                break

        truePC.replace(';', '&&')
        level, x = 0, 0
        while x < len(truePC):
            if truePC[x] == '(':
                level += 1
            if truePC[x] == ')':
                level -= 1
            if truePC[x] == '&' and truePC[x+1] == '&':
                if level != 0:
                    x += 1
                else:
                    # Replace '&&' w/ '@@' if not nested inside parens
                    truePC = truePC[:x] + '@@' + truePC[x+2:]
            x += 1
        return '@@'.join(preamble) + '@@' + truePC

    def getUnique(pc):
        # Start from end of array (where there are more likely to be dupes)
        preds = pc.children()[::-1]
        s = z3.Solver()
        res = []
        for x in range(len(preds)):
            for y in range(x+1, len(preds)):
                s.reset()
                s.add(preds[x] != preds[y])
                if s.check().r == -1:
                    break  # Break if not unique
            if s.check().r != -1:
                res.append(preds[x])  # Add unique pred
        return res[::-1]

    def orToAnd(pc):
        for x in range(len(pc)):
            pred = pc[x]
            indx = pred.find('||')
            if indx != -1:
                # leftExpr still has leftover '('
                leftExpr = pred[: indx].strip()
               # rightExpr still has leftover ')'
                rightExpr = pred[indx+2:].strip()
                # Conv OR -> AND and replace current pred
                pc[x] = '!(!' + leftExpr + ') && !(' + rightExpr + ')'
        return pc

    # Check if each portion of predicate of PC1 is contained in PC2
    def deepCheck(preamble1, pc1, preamble2, pc2, parser1, parser2):
        parser1.clear_context()
        parser2.clear_context()
        parser1.test(preamble1)
        parser2.test(preamble2)

        solver, unique = z3.Solver(), []
        # Split pred1 into two sub-preds
        for pred1 in pc1:
            indx = pred1.find('||')
            if indx != -1:
                leftExpr = pred1[: indx].strip()
                # Remove leftover '('
                if leftExpr[0] == '(':
                    leftExpr = leftExpr[1:]
                rightExpr = pred1[indx+2:].strip()
                # Remove leftover ')'
                if rightExpr[-1] == ')':
                    rightExpr = rightExpr[:-1]

                # If PC2 is empty
                if not pc2:
                    return pc1
                # Compare both of PC1's sub-preds to PC2's pred
                for pred2 in pc2:
                    if not leftExpr or not pred2:
                        continue
                    solver.reset()
                    parsedLeft, parsedPred2 = parser1.test(
                        leftExpr), parser2.test(pred2)
                    solver.add(parsedLeft != parsedPred2)
                    # If leftExpr doesn't match pred2, then check rightExpr
                    if solver.check().r != -1:
                        solver.reset()
                        solver.add(parser1.test(rightExpr)
                                   != parser2.test(pred2))
                        # If neither expressions match pred2, add pred1 to unique list
                        if solver.check().r != -1:
                            unique.append(pred1)

        return unique

    l = SimpleLexer()
    # l.test()
    parser1 = SimpleParser(l.lexer, types={'a': 'intArray', 's0': 'bool', 's1': 'bool', 's2': 'bool', 's3': 'int', 's4': 'bool', 's5': 'bool'}, hooks={
        'Math.Abs': lambda x: z3.If(x >= 0, x, -x)})
    parser2 = SimpleParser(l.lexer, types={'a': 'intArray', 's0': 'bool', 's1': 'bool', 's2': 'bool', 's3': 'int', 's4': 'bool', 's5': 'bool'}, hooks={
        'Math.Abs': lambda x: z3.If(x >= 0, x, -x)})

    # merge, cluster 9
    # a = r'bool s0 = a[0L] < a[1L];\r\nbool s1 = a[1L] >= a[0L];\r\nbool s3 = a[0L] < a[2L];\r\nbool s4 = a[2L] >= a[0L];\r\nbool s2 = s4 || s3;\r\nreturn a != (int[])null && -11 < a[0L] && a[0L] < 11 && \r\n                                          -11 < a[1L] && a[1L] < 11 && 2L < a.Length && -11 < a[2L] && a[2L] < 11 && (s1 || s0) && \r\n                                                                                                                     (s2 ? s4 && !s3 ? 0 : -1 : 1) != 0 && a.Length == 3L && (!s1 || s0) && (!s2 || s4 && !s3);'
    a = r'int s1 = (-1 + (int)(a.Length)) / 2;\r\nint s0 = 2 * s1;\r\nint s5 = a[1 + s0];\r\nint s4 = -1 + s1 - s1 == 0L ? s5 : a[-1 + s1];\r\nint s3 = -1 + s1 - 1 + s0 == 0L ? a[s1] : s4;\r\nint s2 = s3;\r\nint s7 = -1 + s0 - s1 == 0L ? s5 : a[-1 + s0];\r\nint s6 = -1 + s0 - 1 + s0 == 0L ? a[s1] : s7;\r\nint s9 = s0 - s1 == 0L ? s5 : a[s0];\r\nint s8 = s0 - 1 + s0 == 0L ? a[s1] : s9;\r\nlong s12 = -1 + (int)(a.Length);\r\nint s15 = -s1 == 0L ? s5 : a[0L];\r\nint s14 = -(1 + s0) == 0L ? a[s1] : s15;\r\nint s13 = s14;\r\nint s17 = 1L - s1 == 0L ? s5 : a[1L];\r\nint s16 = 1L - 1 + s0 == 0L ? a[s1] : s17;\r\nint s11 = 1L - s12 == 0L ? s13 : s16;\r\nint s10 = s11;\r\nint s20 = 2L - s1 == 0L ? s5 : a[2L];\r\nint s19 = 2L - 1 + s0 == 0L ? a[s1] : s20;\r\nint s18 = 2L - s12 == 0L ? s13 : s19;\r\nlong s22 = (int)(a.Length) - 2;\r\nint s25 = s12 - s1 == 0L ? s5 : a[s12];\r\nint s24 = s12 - 1 + s0 == 0L ? a[s1] : s25;\r\nint s23 = s24;\r\nint s28 = s22 - s1 == 0L ? s5 : a[s22];\r\nint s27 = s22 - 1 + s0 == 0L ? a[s1] : s28;\r\nint s26 = s22 - s12 == 0L ? s13 : s27;\r\nint s21 = s22 == 1L ? s23 : s22 == 0L ? s10 : s26;\r\nint s29 = 1L - s22 == 0L ? s10 : s23;\r\nreturn a != (int[])null && -11 < a[0L] && a[0L] < 11 && \r\n                                          -11 < a[1L] && a[1L] < 11 && -11 < a[2L] && a[2L] < 11 && -11 < a[3L] && a[3L] < 11 && \r\n                                                                                                                   a[0L] >= a[3L] && a[0L] >= a[2L] && 3L < a.Length && a[1L] < a[3L] && a[3L] >= a[2L] && \r\n                                                                                                                                                                                         2L < a.Length && a[2L] >= a[1L] && 1L < a.Length && a.Length == 4L && a.Length == 4L && \r\n                                                                                                                                                                                                                                                               a.Length == 4L && a.Length == 4L && 2 + s0 >= (int)(a.Length) && 3 + 4 * s1 >= (int)(a.Length) && \r\n                                                                                                                                                                                                                                                                                                                                4 + 4 * s1 >= (int)(a.Length) && s2 >= s6 && s2 >= s8 && s10 >= s18 && s21 >= s29; '
    a = a.replace('\\r', '').replace('\\n', '').replace("\\'", "'").replace(
        'return', '').replace('\\\\', '\\').strip()
    a = cleanInteriorAnd(a)
    a_clean = list(map(lambda x: x.strip(), a.split('@@')))
    # a_clean = orToAnd(a_clean)
    x = parser1.test(a_clean)[1]
    # parser1.clear_context()

    # merge, cluster 8
    # b = r'return a != (int[])null && -11 < a[0L] && a[0L] < 11 && \r\n                                          -11 < a[1L] && a[1L] < 11 && 2L < a.Length && -11 < a[2L] && a[2L] < 11 && a[0L] < a[1L] && \r\n                                                                                                                     a.Length == 3L && a[0L] != a[1L] && a[1L] != a[2L] && a[1L] >= a[2L] && a[0L] >= a[2L];'
    b = r'long s1 = (int)(a.Length) - 2;\r\nlong s4 = -1 + (int)(a.Length);\r\nint s10 = ((int)(a.Length) - 2) / 2;\r\nint s9 = 2 * s10;\r\nint s8 = 1 + s9;\r\nlong s7 = s8;\r\nint s11 = -s10 == 0L ? a[s7] : a[0L];\r\nint s6 = -s7 == 0L ? a[s10] : s11;\r\nint s5 = s6;\r\nint s13 = 2L - s10 == 0L ? a[s7] : a[2L];\r\nint s12 = 2L - s7 == 0L ? a[s10] : s13;\r\nint s3 = 2L - s4 == 0L ? s5 : s12;\r\nint s2 = s3;\r\nint s18 = s4 - s10 == 0L ? a[s7] : a[s4];\r\nint s17 = s4 - s7 == 0L ? a[s10] : s18;\r\nint s16 = s17;\r\nint s15 = -s4 == 0L ? s5 : s16;\r\nint s22 = s1 - s10 == 0L ? a[s7] : a[s1];\r\nint s21 = s1 - s7 == 0L ? a[s10] : s22;\r\nint s20 = s1 == 0L ? s16 : s21;\r\nint s19 = s1 - s4 == 0L ? s5 : s20;\r\nint s14 = s1 == 0L ? s2 : s1 == 2L ? s15 : s19;\r\nint s0 = -s1 == 0L ? s2 : s14;\r\nint s27 = 1L - s10 == 0L ? a[s7] : a[1L];\r\nint s26 = 1L - s7 == 0L ? a[s10] : s27;\r\nint s25 = 1L - s4 == 0L ? s5 : s26;\r\nint s24 = s25;\r\nint s23 = 1L - s1 == 0L ? s2 : s24;\r\nint s30 = -1 + s10 - s10 == 0L ? a[s7] : a[-1 + s10];\r\nint s29 = -1 + s10 - s7 == 0L ? a[s10] : s30;\r\nint s28 = s29;\r\nint s32 = s9 - s10 == 0L ? a[s7] : a[s9];\r\nint s31 = s9 - s7 == 0L ? a[s10] : s32;\r\nint s34 = -1 + s9 - s10 == 0L ? a[s7] : a[-1 + s9];\r\nint s33 = -1 + s9 - s7 == 0L ? a[s10] : s34;\r\nreturn a != (int[])null && -11 < a[0L] && a[0L] < 11 && -11 < a[1L] && \r\n                                                        a[1L] < 11 && -11 < a[2L] && a[2L] < 11 && -11 < a[3L] && a[3L] < 11 && a[1L] < a[3L] && \r\n                                                                                                                                a[0L] >= a[2L] && a[0L] >= a[3L] && 3L < a.Length && a[1L] < a[2L] && a[2L] >= a[3L] && \r\n                                                                                                                                                                                                      2L < a.Length && s0 < s23 && 1L < a.Length && a.Length != 0L && a.Length == 4L && \r\n                                                                                                                                                                                                                                                                      a.Length == 4L && -1 + (int)(a.Length) >= s8 && -1 + (int)(a.Length) >= -1 + s9 && \r\n                                                                                                                                                                                                                                                                                                                      -1 + (int)(a.Length) >= s9 && s28 >= s31 && s28 >= s33 && s2 >= s24; '
    b = b.replace('\\r', '').replace('\\n', '').replace("\\'", "'").replace(
        'return', '').replace('\\\\', '\\').strip()
    b = cleanInteriorAnd(b)

    b_clean = list(map(lambda x: x.strip(), b.split('@@')))
    # print(orToAnd(b_clean))
    # b_clean = orToAnd(b_clean)
    y = parser2.test(b_clean)[1]
    # xy = getUnique(y[1])

    # xx = z3.simplify(reduce(z3.And, xy, True)) if len(xy) > 0 else z3.BoolVal(True)

    # Test to see what preds they mismatch on:
    xx, yy, gg, lUnique, rUnique = x.children(
    ), y.children(), z3.Solver(), [], []
    for predx in xx:
        for predy in yy:
            gg.reset()
            gg.add(predx != predy)
            if gg.check().r == -1:
                break  # Break if both preds match
        if gg.check().r != -1:
            lUnique.append(predx)  # Add unique pred
    # Both loops necessary for full pairwise (all permutations checked)
    for predy in yy:
        for predx in xx:
            gg.reset()
            gg.add(predy != predx)
            if gg.check().r == -1:
                break  # Break if both preds match
        if gg.check().r != -1:
            rUnique.append(predy)  # Add unique pred

    print('leftUnique preds:', lUnique)
    print('rightUnique preds:', rUnique)
    print('-----')

    print('type(x) = {}, {}:\n'.format(type(x), x))
    print('type(y) = {}, {}:\n'.format(type(y), y))
    # print('type(xx) = {}, {}:\n'.format(type(xx), xx))
    print('-----')

    # print('y\'s children:')
    # gg = y[1].children()
    # gh = z3.Solver()
    # gh.add(gg[-3] != gg[-2])
    # print(gh.check().r == -1)
    # print('-----')

    z3.solve(x != y)
    s = z3.Solver()
    s.add(x != y)
    # s.add(z3.Or(z3.Not(y[1]), x[1]) != True)

    # s.check.r(): 1 (eq is true...PCs are inqeuiv) or -1 (eq is false...PCSs are equiv)
    print(s.check().r == -1)
    # If above prints False, the eqs are INEQ, else if it prints True, they're EQUIV

# Uncomment the code below to run the implication checker on each PC:
    # If the two PCs are INEQUIV
    if s.check().r == 1:

        a_preamble, b_preamble, a_rem, b_rem = [], [], [], []
        # Get preambles for both PCs
        for i in range(len(a_clean)):
            expr = a_clean[i]
            if set(expr.split()) & set(TYPES.keys()):
                a_preamble += [expr]
            else:
                a_rem = a_clean[i:]
                break

        for i in range(len(b_clean)):
            expr = b_clean[i]
            if set(expr.split()) & set(TYPES.keys()):
                b_preamble += [expr]
            else:
                b_rem = b_clean[i:]
                break

        # Do deeper check..remove preds shared b/t the two PCs
        a_remNew, b_remNew = [], []
        for xPred in a_rem:
            if xPred not in b_rem:
                a_remNew.append(xPred)
        for yPred in b_rem:
            if yPred not in a_rem:
                b_remNew.append(yPred)

        # allUnique = #unique preds in a_remNew and b_remNew, excluding the empty ('') pred
        allUnique = set(a_remNew) | set(b_remNew)
        allUnique = len(set(filter(lambda x: x != '', allUnique)))
        currUnique = set()

        for pred1 in a_remNew:
            for pred2 in b_remNew:
                # Check if pred1 -> pred2 and pred2 -> pred1
                s.reset()
                if not pred1 or not pred2:
                    continue
                parsedPred1 = parser1.predParse(pred1)
                parsedPred2 = parser2.predParse(pred2)

                s.add(z3.Or(z3.Not(parsedPred1), parsedPred2) != True)
                res1 = s.check().r == -1
                s.reset()
                s.add(z3.Or(z3.Not(parsedPred2), parsedPred1) != True)
                res2 = s.check().r == -1
                if res1 and res2:
                    print(pred1, ' EQUALS ', pred2)
                    currUnique.update([pred1, pred2])
                elif res1:
                    print(pred1, ' IMPLIES ', pred2)
                    currUnique.update([pred1, pred2])
                elif res2:
                    print(pred2, ' IMPLIES ', pred1)
                    currUnique.update([pred1, pred2])
        # If num. preds matched == total num. unique preds, then CLUSTER them
        print(len(currUnique), allUnique)
        if len(currUnique) == allUnique:
            print('CLUSTER THESE')
        else:
            print('DONT CLUSTER THESE')


# Uncomment code below to find the preds unique to each PC:

        # a_preamble, b_preamble, a_rem, b_rem = [], [], [], []
        # # Get preambles for both PCs
        # for i in range(len(a_clean)):
        #     expr = a_clean[i]
        #     if set(expr.split()) & set(TYPES.keys()):
        #         a_preamble += [expr]
        #     else:
        #         a_rem = a_clean[i:]
        #         break

        # for i in range(len(b_clean)):
        #     expr = b_clean[i]
        #     if set(expr.split()) & set(TYPES.keys()):
        #         b_preamble += [expr]
        #     else:
        #         b_rem = b_clean[i:]
        #         break

        # # Do deeper check..remove preds shared b/t the two PCs
        # a_remNew, b_remNew = [], []
        # for xPred in a_rem:
        #     if xPred not in b_rem:
        #         a_remNew.append(xPred)
        # for yPred in b_rem:
        #     if yPred not in a_rem:
        #         b_remNew.append(yPred)

        # # Check if sub-pred of PC1 is in PC2, and vice-versa
        # a_unique = deepCheck(a_preamble, a_remNew,
        #                      b_preamble, b_remNew, parser1, parser2)
        # b_unique = deepCheck(b_preamble, b_remNew,
        #                      a_preamble, a_remNew, parser1, parser2)
        # if float(len(a_unique) + len(b_unique)) / len(set(a_clean) | set(b_clean)) <= 0.1:
        #     print(">= 90% MATCH")
        # print('PC1\'s unique preds: ', a_unique)
        # print('PC2\'s unique preds: ', b_unique)
