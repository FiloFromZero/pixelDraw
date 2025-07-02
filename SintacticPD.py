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

    def color(self):
        # Handle the COLOR instruction
        if self.current_token.type_ == "COLOR":
            print(f"Detectado color: {self.current_token.value}")
            self.advance()
        else:
            self.error("COLOR")

    def punto(self):
        # Handle the PUNTO (point) instruction
        if self.current_token.type_ == "PUNTO":
            print(f"Detectado punto: {self.current_token.value}")
            self.advance()
        else:
            self.error("PUNTO")

    def rectangulo(self):
        # Handle the RECTANGULO (rectangle) instruction
        if self.current_token.type_ == "RECTANGULO":
            print(f"Detectado rectángulo: {self.current_token.value}")
            self.advance()
        else:
            self.error("RECTANGULO")

    def repetir(self):
        # Handle the REPETIR (repeat) block
        if self.current_token.type_ == "REPETIR_INI":
            print(f"Inicio de repetición: {self.current_token.value}")
            self.advance()
            # Process instructions inside the repeat block
            while self.current_token is not None and self.current_token.type_ != "REPETIR_END":
                self.instruccion()
            # Check for the end of the repeat block
            if self.current_token and self.current_token.type_ == "REPETIR_END":
                print("Fin de repetición")
                self.advance()
            else:
                self.error("} (fin de bloque repetir)")
        else:
            self.error("REPETIR_INI")

    def error(self, esperado):
        # Raise a syntax error with a descriptive message
        raise SyntaxError(f"Error de sintaxis: se esperaba {esperado}, pero se encontró {self.current_token}")
