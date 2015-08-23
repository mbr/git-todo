import click
import parsley
from visitor import Visitor


class Heading(object):
    def __init__(self, text, underline):
        self.text = text
        self.ctype = underline[0]


class Entry(object):
    def __init__(self, text, ctype):
        self.text = text
        self.ctype = ctype

    @property
    def done(self):
        return self.ctype in ('x', )

    @property
    def important(self):
        return self.ctype in ('!', )


class TODOList(list):
    pass


class Document(list):
    def __init__(self, elems):
        super(Document, self).__init__(e for e in elems if e is not None)


rules = r"""
nl = '\n'
blank_line = nl -> None
char = ~nl anything
line_char = '_' | '-' | '*' | '~' | '=' | '#' | '+'
underline = <line_char+>:l ?(len(l) == l.count(l[0])) -> l

bullet = ('*' | 'x' | '-' | '!')
entry = bullet:b ' ' <char+>:c nl -> Entry(c, b)
list = entry+:entries -> TODOList(entries)

heading = <char+>:c nl underline:l nl ?(len(c) == len(l)) -> Heading(c, l)

doc = ((blank_line+ -> None) | heading | list)+:elems -> Document(elems)
"""

grammar = parsley.makeGrammar(rules, locals())


class Printer(Visitor):
    def visit_Document(self, node):
        return ''.join(self.visit(e) for e in node).strip('\n') + '\n'

    def visit_TODOList(self, node):
        entries = sorted(node, key=lambda n: (n.done, not n.important))
        return '\n'.join(self.visit(e) for e in entries) + '\n\n'

    def visit_Heading(self, node):
        buf = node.text + '\n' + node.ctype * len(node.text) + '\n'
        return click.style(buf, bold=True)

    def visit_Entry(self, node):
        style = {}

        if node.done:
            style['fg'] = 'green'
        else:
            style['fg'] = 'yellow'
            if node.important:
                style['fg'] = 'red'
                style['bold'] = True

        buf = node.ctype + ' ' + node.text
        return click.style(buf, **style)
