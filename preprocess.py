import re

DIRECTIVE_PREFIX = '#'
COMMENT_PREFIX = '//'
MULTILINE_COMMENT_START = '/*'
MULTILINE_COMMENT_END = '*/'

class PreprocesserException(Exception): pass

def find_macro(macros: dict[str, str], line: str) -> tuple[str, int] | None:
    '''
    finds a macro if it exists on a line
    :macros: a dictionary of macros and their expansions
    :line: a line of code from the program
    :returns: a tuple of the found macro and the index of it's first letter
    '''
    for macro in macros:
        matches = re.finditer(fr'\b{macro}\b', line)
        for mtch in matches:
            index = mtch.start(0)
            in_string = False
            prev_bslash = False
            for ch in line[:index]:
                if ch == '\'':
                    if in_string and not prev_bslash or not in_string:
                        in_string = not in_string
                prev_bslash = ch == '\\'
            if in_string:
                continue
            return macro, index
    return None

def preprocess(string: str, macros: dict[str, str] | None = None) -> str:
    '''
    preprocess input
    this removes comments and expands macros
    :string: the input to preprocess
    :returns: processed input
    '''
    if macros is None:
        macros = {}
    new_lines = []
    for line in string.split('\n'):
        line = line.strip()
        if line.startswith(DIRECTIVE_PREFIX):
            parts = line[1:].split(' ', 1)
            if len(parts) == 1:
                name, = parts
                line = ''
            else:
                name, line = parts
            match name:
                case 'def':
                    if not line or len((parts := line.split(' ', 1))) < 2:
                        raise PreprocesserException(f'Expected 2 arguments for def directive')
                    name, rest = parts
                    macros[name] = rest
                    line = ''
                case 'inc':
                    if not line:
                        raise PreprocesserException(f'Expected 1 filename for inc directive')
                    with open(line, 'r') as f:
                        new_lines.append(preprocess(f.read(), macros))
                    line = ''
                case _:
                    raise PreprocesserException(f'Unknown preprocessor directive: {name}')
        elif COMMENT_PREFIX in line:
            index = line.index(COMMENT_PREFIX)
            line = line[:index]
        # substitute macros
        while 1:
            found_tup = find_macro(macros, line)
            if found_tup is None:
                break
            macro, index = found_tup
            line = line[:index] + macros[macro] + line[index + len(macro):]
        new_lines.append(line)
    return '\n'.join(new_lines).strip() + ' '
