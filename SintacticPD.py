"""
This module represents the behavior of a syntactic analyzer for PixelDraw.

Authors: Nicolás Alberto Rodríguez Delgado <niarodriguezd@udistrital.edu.co> <20202020019>
         Cristian----
"""

# Updated Grammar:
# <S>           -> <instruction>*
# <instruction> -> <clear> | <pixel> | <line> | <rect> | <frame> | <circle> | <color> | <size> | <legacy>
# <clear>       -> "clear"
# <pixel>       -> "pixel" <coordinate>
# <line>        -> "line" <coordinate> "to" <coordinate>
# <rect>        -> "rect" <coordinate> <dimension>
# <frame>       -> "frame" <coordinate> <dimension>
# <circle>      -> "circle" <coordinate> "radius" <number>
# <color>       -> "color" <COLORNAME> | "color" <COLORHEX>
# <size>        -> "size" <dimension>
# <coordinate>  -> "(" <number> "," <number> ")"
# <dimension>   -> "(" <number> "," <number> ")"
# <number>      -> <digit>+
# <digit>       -> "0"|"1"|"2"|"3"|"4"|"5"|"6"|"7"|"8"|"9"
# <COLORNAME>   -> <letters>+
# <COLORHEX>    -> "#"<DIGITHEX><DIGITHEX><DIGITHEX><DIGITHEX><DIGITHEX><DIGITHEX>
# <DIGITHEX>    -> <digit>|"A"..."F"|"a"..."f"
# <letters>     -> (a-zA-Z)+
# <legacy>      -> <tamano> | <punto> | <rectangulo> | <repetir>

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
        if self.current_token is None:
            self.error("instrucción válida")
        elif self.current_token.type_ == "CLEAR":
            self.clear()
        elif self.current_token.type_ == "PIXEL":
            self.pixel()
        elif self.current_token.type_ == "LINE":
            self.line()
        elif self.current_token.type_ == "RECT":
            self.rect()
        elif self.current_token.type_ == "FRAME":
            self.frame()
        elif self.current_token.type_ == "CIRCLE":
            self.circle()
        elif self.current_token.type_ == "COLOR":
            self.color()
        elif self.current_token.type_ == "SIZE":
            self.size()
        # Legacy instructions
        elif self.current_token.type_ == "TAMANIO":
            self.tamano()
        elif self.current_token.type_ == "PUNTO":
            self.punto()
        elif self.current_token.type_ == "RECTANGULO":
            self.rectangulo()
        elif self.current_token.type_ == "REPETIR_INI":
            self.repetir()
        else:
            # If the token does not match any known instruction, raise an error
            self.error("instrucción válida")

    def clear(self):
        # Handle the CLEAR instruction
        if self.current_token is None:
            self.error("CLEAR")
        elif self.current_token.type_ == "CLEAR":
            print(f"Detectado clear: {self.current_token.value}")
            self.advance()
        else:
            self.error("CLEAR")

    def pixel(self):
        # Handle the PIXEL instruction: pixel (X,Y)
        if self.current_token is None:
            self.error("PIXEL")
        elif self.current_token.type_ == "PIXEL":
            print(f"Detectado pixel: {self.current_token.value}")
            self.advance()
            self.coordinate()
        else:
            self.error("PIXEL")

    def line(self):
        # Handle the LINE instruction: line (X1,Y1) to (X2,Y2)
        if self.current_token is None:
            self.error("LINE")
        elif self.current_token.type_ == "LINE":
            print(f"Detectado line: {self.current_token.value}")
            self.advance()
            self.coordinate()
            if self.current_token and self.current_token.type_ == "TO":
                print(f"Detectado to: {self.current_token.value}")
                self.advance()
                self.coordinate()
            else:
                self.error("TO")
        else:
            self.error("LINE")

    def rect(self):
        # Handle the RECT instruction: rect (X,Y) (W,H)
        if self.current_token is None:
            self.error("RECT")
        elif self.current_token.type_ == "RECT":
            print(f"Detectado rect: {self.current_token.value}")
            self.advance()
            self.coordinate()
            self.dimension()
        else:
            self.error("RECT")

    def frame(self):
        # Handle the FRAME instruction: frame (X,Y) (W,H)
        if self.current_token is None:
            self.error("FRAME")
        elif self.current_token.type_ == "FRAME":
            print(f"Detectado frame: {self.current_token.value}")
            self.advance()
            self.coordinate()
            self.dimension()
        else:
            self.error("FRAME")

    def circle(self):
        # Handle the CIRCLE instruction: circle (X,Y) radius N
        if self.current_token is None:
            self.error("CIRCLE")
        elif self.current_token.type_ == "CIRCLE":
            print(f"Detectado circle: {self.current_token.value}")
            self.advance()
            self.coordinate()
            if self.current_token and self.current_token.type_ == "RADIUS":
                print(f"Detectado radius: {self.current_token.value}")
                self.advance()
                self.number()
            else:
                self.error("RADIUS")
        else:
            self.error("CIRCLE")

    def size(self):
        # Handle the SIZE instruction: size (W,H)
        if self.current_token is None:
            self.error("SIZE")
        elif self.current_token.type_ == "SIZE":
            print(f"Detectado size: {self.current_token.value}")
            self.advance()
            self.dimension()
        else:
            self.error("SIZE")

    def coordinate(self):
        # Handle coordinate: (X,Y)
        if self.current_token is None:
            self.error("coordenada")
        elif self.current_token.type_ == "COORDINATE":
            print(f"Detectada coordenada: {self.current_token.value}")
            self.advance()
        elif self.current_token.type_ == "LPAREN":
            print(f"Detectado LPAREN: {self.current_token.value}")
            self.advance()
            self.number()
            if self.current_token and self.current_token.type_ == "COMMA":
                print(f"Detectado COMMA: {self.current_token.value}")
                self.advance()
                self.number()
                if self.current_token and self.current_token.type_ == "RPAREN":
                    print(f"Detectado RPAREN: {self.current_token.value}")
                    self.advance()
                else:
                    self.error("RPAREN")
            else:
                self.error("COMMA")
        else:
            self.error("coordenada")

    def dimension(self):
        # Handle dimension: (W,H)
        if self.current_token is None:
            self.error("dimensión")
        elif self.current_token.type_ == "DIMENSION":
            print(f"Detectada dimensión: {self.current_token.value}")
            self.advance()
        elif self.current_token.type_ == "LPAREN":
            print(f"Detectado LPAREN: {self.current_token.value}")
            self.advance()
            self.number()
            if self.current_token and self.current_token.type_ == "COMMA":
                print(f"Detectado COMMA: {self.current_token.value}")
                self.advance()
                self.number()
                if self.current_token and self.current_token.type_ == "RPAREN":
                    print(f"Detectado RPAREN: {self.current_token.value}")
                    self.advance()
                else:
                    self.error("RPAREN")
            else:
                self.error("COMMA")
        else:
            self.error("dimensión")

    def number(self):
        # Handle number
        if self.current_token is None:
            self.error("número")
        elif self.current_token.type_ == "NUMBER":
            print(f"Detectado número: {self.current_token.value}")
            self.advance()
        else:
            self.error("número")

    def color(self):
        # Handle the COLOR instruction: color <COLORNAME> | color <COLORHEX>
        if self.current_token is None:
            self.error("COLOR")
        elif self.current_token.type_ == "COLOR":
            print(f"Detectado color: {self.current_token.value}")
            self.advance()
            # Expect a color value (name or hex)
            if self.current_token is None:
                self.error("valor de color")
            elif self.current_token.type_ in ["COLORNAME", "COLORHEX"]:
                print(f"Detectado valor de color: {self.current_token.value}")
                self.advance()
            else:
                self.error("valor de color")
        else:
            self.error("COLOR")

    # Legacy methods for backward compatibility
    def tamano(self):
        # Handle the TAMANIO (size) instruction
        if self.current_token is None:
            self.error("TAMANIO")
        elif self.current_token.type_ == "TAMANIO":
            print(f"Detectado tamaño: {self.current_token.value}")
            self.advance()
        else:
            self.error("TAMANIO")

    def punto(self):
        # Handle the PUNTO (point) instruction
        if self.current_token is None:
            self.error("PUNTO")
        elif self.current_token.type_ == "PUNTO":
            print(f"Detectado punto: {self.current_token.value}")
            self.advance()
        else:
            self.error("PUNTO")

    def rectangulo(self):
        # Handle the RECTANGULO (rectangle) instruction
        if self.current_token is None:
            self.error("RECTANGULO")
        elif self.current_token.type_ == "RECTANGULO":
            print(f"Detectado rectángulo: {self.current_token.value}")
            self.advance()
        else:
            self.error("RECTANGULO")

    def repetir(self):
        # Handle the REPETIR (repeat) block
        if self.current_token is None:
            self.error("REPETIR_INI")
        elif self.current_token.type_ == "REPETIR_INI":
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
