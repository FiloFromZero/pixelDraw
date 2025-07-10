"""This module represents the behavior of a lexical analyzer for PixelDraw.

Authors: Nicolás Alberto Rodríguez Delgado <20202020019>
         Daniel Mateo Montoya González <20202020098>
"""

import re


# pylint: disable=too-few-public-methods
class Token:
    """This class represents the data structure of a token.
    It means: a type of token and its value (lexeme)."""

    def __init__(self, type_: str, value):
        self.type_ = type_
        self.value = value

    def __repr__(self):
        return f"Token({self.type_}, {self.value})"


class LexicalAnalyzer:
    """This class represents the behavior of a lexical analyzer for PixelDraw."""

    @staticmethod
    def lex(code):
        """This method receives a code and returns a list of tokens."""
        tokens = []
        token_specification = [
            # Keywords (must come before other patterns to avoid conflicts)
            ("CLEAR",      r"clear"),                                    # clear
            ("PIXEL",      r"pixel"),                                    # pixel
            ("LINE",       r"line"),                                     # line
            ("RECT",       r"rect"),                                     # rect
            ("FRAME",      r"frame"),                                    # frame
            ("CIRCLE",     r"circle"),                                   # circle
            ("TO",         r"to"),                                       # to
            ("SIZE",       r"size"),                                     # size
            ("RADIUS",     r"radius"),                                   # radius
            ("COLOR",      r"color"),                                    # color
            
            # Legacy tokens (for backward compatibility)
            ("TAMANIO",    r"tamaño\s+\d+x\d+"),                         # tamaño WxH
            ("PUNTO",      r"punto\s+\d+\s+\d+"),                         # punto X Y
            ("RECTANGULO", r"rectangulo\s+\d+\s+\d+\s+\d+\s+\d+"),        # rectangulo X Y W H
            ("REPETIR_INI",r"repetir\s+\d+\s+\{"),                        # repetir N {
            ("REPETIR_END",r"\}"),                                        # }
            
            # Symbols
            ("LPAREN",     r"\("),                                       # (
            ("RPAREN",     r"\)"),                                       # )
            ("COMMA",      r","),                                        # ,
            
            # Numbers and coordinates
            ("NUMBER",     r"\d+"),                                      # integers
            ("COORDINATE", r"\(\s*\d+\s*,\s*\d+\s*\)"),                  # (X,Y)
            ("DIMENSION",  r"\(\s*\d+\s*,\s*\d+\s*\)"),                  # (W,H) - same as coordinate
            
            # Color values (words and hex)
            ("COLORNAME",  r"[a-zA-Z]+"),                                # color names like red, blue, etc.
            ("COLORHEX",   r"#[0-9a-fA-F]{6}"),                         # hex colors like #FF0000
            
            # Comments
            ("COMMENT",    r"#.*"),                                      # # comment
            
            # Skip whitespace
            ("SKIP",       r"[ \t\n]+"),                                  # Skip spaces, tabs, newlines
            ("MISMATCH",   r"."),                                         # Any other character
        ]

        tok_regex = "|".join(
            f"(?P<{pair[0]}>{pair[1]})" for pair in token_specification
        )

        for mo in re.finditer(tok_regex, code):
            kind = mo.lastgroup
            value = mo.group()

            if kind is None:
                # This should not happen with our regex, but just in case
                raise RuntimeError(f"Unexpected regex match without group: '{value}'")
            
            if kind == "MISMATCH":
                # throws an error if the character is not recognized
                raise RuntimeError(f"Unexpected token: '{value}'")
            if kind == "SKIP":
                continue
            if kind == "COMMENT":
                # Skip comments
                continue
            tokens.append(Token(kind, value.strip()))

        return tokens 