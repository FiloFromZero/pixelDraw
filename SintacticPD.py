"""
This module represents the behavior of a syntactic analyzer for PixelDraw.

Authors: Nicolás Alberto Rodríguez Delgado <niarodriguezd@udistrital.edu.co> <20202020019>
         Cristian----
"""

# <S>           -> <instruction>
# <instruction> -> <size> | <color> | <point> | <rectangle> | <repeat>
# <size>        -> "tamaño"<espace><integer>"x"<integer>
# <color>       -> "color"<espace><COLORNAME> | "color"<espace><COLORHEX>
# <point>       -> "punto"<espace><integer><espace><integer>
# <rectangle>   -> "rectangulo"<espace><integer><espace><integer><espace><integer><espace><integer>
# <repeat>      -> "repetir"<espace><integer><espace>"{" <instruction>* "}"
# <integer>     -> <digit>+
# <digit>       -> "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"
# <COLORNAME>   -> <letters>+
# <COLORHEX>    -> "#"<DIGITHEX><DIGITHEX><DIGITHEX><DIGITHEX><DIGITHEX><DIGITHEX>
# <DIGITHEX>    -> <digit>|"A"..."F"|"a"..."f"
# <letters>     -> (a-zA-Z)+
# <espace>      -> " "+

class SintacticAnalyzerPixelDraw:
    def __init__(self, tokens):
        # Store the list of tokens to be parsed
        self.tokens = tokens
        # Initialize the current token
        self.current_token = None
        # Position in the token list
        self.pos = -1
        # Advance to the first token
        self.advance()

    def advance(self):
        # Move to the next token in the list
        self.pos += 1
        if self.pos < len(self.tokens):
            self.current_token = self.tokens[self.pos]
        else:
            # If there are no more tokens, set current_token to None
            self.current_token = None

    def parse(self):
        # Main parsing loop: process instructions until tokens are exhausted
        while self.current_token is not None:
            self.instruccion()

    def instruccion(self):
        # Determine the type of instruction based on the current token
        if self.current_token.type_ == "TAMANIO":
            self.tamano()
        elif self.current_token.type_ == "COLOR":
            self.color()
        elif self.current_token.type_ == "PUNTO":
            self.punto()
        elif self.current_token.type_ == "RECTANGULO":
            self.rectangulo()
        elif self.current_token.type_ == "REPETIR_INI":
            self.repetir()
        else:
            # If the token does not match any known instruction, raise an error
            self.error("instrucción válida")

    def tamano(self):
        # Handle the TAMANIO (size) instruction
        if self.current_token.type_ == "TAMANIO":
            print(f"Detectado tamaño: {self.current_token.value}")
            self.advance()
        else:
            self.error("TAMANIO")

    def error(self, esperado):
        # Raise a syntax error with a descriptive message
        raise SyntaxError(f"Error de sintaxis: se esperaba {esperado}, pero se encontró {self.current_token}")
