import re

token_patron = {
    "KEYWORD": r'\b(if|else|while|for|return|int|float|void|print|println)\b',
    "IDENTIFIER": r'\b[a-zA-Z_][a-zA-Z0-9_]*\b',
    "NUMBER": r'\b\d+(\.\d+)?\b',
    "OPERATOR": r'(==|!=|<=|>=|[+\-*/=<>])',
    "DELIMITER": r'[(),;{}]',
    "WHITESPACE": r'\s+',
}

def identificar_tokens(texto):
    patron_general = "|".join(f"(?P<{t}>{p})" for t, p in token_patron.items())
    patron_regex = re.compile(patron_general)
    return [(m.lastgroup, m.group()) for m in patron_regex.finditer(texto) if m.lastgroup != "WHITESPACE"]