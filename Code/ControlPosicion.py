import Code.TrListas as TrListas
import Code.SAK as SAK

FEN_INICIAL = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

class ControlPosicion:
    """
    Lleva el control del tablero, piezas en cada casilla, posibilidad de mover de una a otra, asi como el turno....
    A FEN record contains six fields. The separator between fields is a space. The fields are:

       1. Piece placement (from white's perspective). Each rank is described, starting with rank 8 and ending with rank 1; within each rank, the contents of each square are described from file a through file h. Following the Standard Algebraic Notation (SAN), each piece is identified by a single letter taken from the standard English names (pawn = "P", knight = "N", bishop = "B", rook = "R", queen = "Q" and king = "K").[1] White pieces are designated using upper-case letters ("PNBRQK") while Black take lowercase ("pnbrqk"). Blank squares are noted using digits 1 through 8 (the number of blank squares), and "/" separate ranks.
       2. Active color. "w" means white moves next, "b" means black.
       3. Castling availability. If neither side can castle, this is "-". Otherwise,
       this has one or more letters: "K" (White can castle kingside),
       "Q" (White can castle queenside), "k" (Black can castle kingside), and/or "q" (Black can castle queenside).
       4. En passant target square in algebraic notation. If there's no en passant target square, this is "-". If a pawn has just made a 2-square move, this is the position "behind" the pawn. This is recorded regardless of whether there is a pawn in position to make an en passant capture.
       5. Halfmove clock: This is the number of halfmoves since the last pawn advance or capture. This is used to determine if a draw can be claimed under the fifty-move rule.
       6. Fullmove number: The number of the full move. It starts at 1, and is incremented after Black's move.
    """

    def __init__(self):
        self.liExtras = []
        self.sak = SAK.sak

    def posInicial(self):
        """
        Se situa en el comienzo normal.
        """
        self.leeFen(FEN_INICIAL)
        # self.leeFen( "8/8/k7/2Q2pK1/1P3Pb1/2PR4/8/8 w - - 7 53")
        # self.leeFen( "r1bqkbnr/pp1ppppp/2n5/8/3QP3/8/PPP2PPP/RNB1KBNR w KQkq - 1 4" )
        # self.leeFen( "2kn1b1r/pp3ppp/5n2/1Np2pN1/5B2/4P3/PPP2PPP/2KR4 w - - 0 1" )
        # self.leeFen( "7k/4Q3/8/6K1/8/8/8/8 w - - 0 1" ) # Mate en 2/3 para blancas
        # self.leeFen( "7K/4q3/8/6k1/8/8/8/8 w - - 0 1" ) # Mate en 2/3 para negras
        # self.leeFen( "7K/4q3/Q7/6k1/8/8/8/8 w - - 0 1" ) # Mate en 2/3 para negras
        # self.leeFen( "8/3P3k/8/8/8/8/7K/8 w - - 0 1" ) # Peon a punto de coronar -> promocion
        # ~ self.leeFen( "7K/8/7k/4Q3/8/8/8/8 w - - 0 1" ) # Tablas
        #~ self.leeFen( "8/8/8/4k1P1/8/8/6P1/2K5 w - - 0 1" )
        # self.leeFen( "r3k1nr/pp1n1ppp/4p3/1N6/3N4/8/PP2KP1q/R1B1b3 w - - 0 1" ) # Mate a las blancas
        #~ self.leeFen( "r1b1kbnr/pp3ppp/4p3/4n3/3N4/N7/PP2BPqP/R1BQK2R w - - 0 1" )
        #~ self.leeFen( "2kr1b1r/2p1pppp/p7/3pPb2/1q3P2/2N1P3/PPP3PP/R1BQK2R w KQ - 0 1" )
        #~ self.leeFen( "4rk2/1bpq1rpQ/1pn1p2p/p2pP3/3P1N2/P1PB4/2P2PPP/R5K1 w  - 0 1" )
        #~ self.leeFen( "R3R2K/P6P/2PPq12/1PB1PpQ1/8/p1pp1p1B/bp3p1p/r5rk w - - 6 21" )
        #~ self.leeFen( "3k4/1p3ppp/2q1p3/1p6/8/N1P3Pb/P2n3P/6K1 w - - 2 40" )
        # self.leeFen( "2bq1b2/p1ppp3/7p/1rPP1Q2/3k3P/P4R2/4PPP1/2R1KB2 w - - 0 22" ) # Mate de mas de una forma
        #~ self.leeFen( "1rbq1b2/p1pppk2/7p/1PPP4/4Q2P/P6R/4PPP1/R3KB2 w Q - 0 18" )
        #~ r2qkb1r/1pP1pppp/p2p4/1B6/4P1n1/2N5/PPP2PPP/R1B1K2R b KQkq - 0 10
        return self

    def logo(self):
        # ~ self.leeFen( "8/4q1k1/1R2bpn1/1N2n1b1/1B2r1r1/1Q6/1PKNBR2/8 w - - 0 1" )
        self.leeFen("8/4Q1K1/1r2BPN1/1n2N1B1/1b2R1R1/1q6/1pknbr2/8 w - - 0 1")
        return self

    def copia(self):
        p = ControlPosicion()
        p.casillas = self.casillas.copy()
        p.enroques = self.enroques
        p.alPaso = self.alPaso
        p.siBlancas = self.siBlancas
        p.jugadas = self.jugadas
        p.movPeonCap = self.movPeonCap
        return p

    def legal(self):
        if self.enroques != '-':
            dic = {"K": ( "K", "R", "e1", "h1" ), "k": ( "k", "r", "e8", "h8" ), "Q": ( "K", "R", "e1", "a1" ),
                   "q": ( "k", "r", "e8", "a8" )}
            enr = ""
            for tipo in self.enroques:
                rey, torre, posRey, posTorre = dic[tipo]
                if self.siExistePieza(rey, posRey) and self.siExistePieza(torre, posTorre):
                    enr += tipo
            self.enroques = enr
            # if len(self.alPaso) == 2:
            # letra = self.alPaso[0]
            # numero = self.alPaso[1]
            # #deben existir
            # num = "5" if numero == "6" else "4"
            # peon = "P" if numero == "6" else "p"
            # let = chr( ord(letra)-1 )
            # si = False
            # if let >= 'a':
            # si = self.siExistePieza( peon, let + num )
            # if not si:
            # let = chr( ord(letra)+1 )
            # if let <= 'h':
            # si = self.siExistePieza( peon, let + num )
            # if not si:
            # self.alPaso = "-"

    def leeFen(self, fen):
        fen = fen.strip()
        if "/" not in fen:
            fen = FEN_INICIAL

        d = {}
        for i in range(8):
            for j in range(8):
                cCol = chr(i + 97)
                cFil = chr(j + 49)
                d[cCol + cFil] = None
        self.casillas = d

        li = fen.split(" ")
        if len(li) == 4:
            li.append("0")
            li.append("1")
        posicion, color, self.enroques, self.alPaso, mp, jg = li

        self.siBlancas = color == "w"
        self.jugadas = int(jg)
        if self.jugadas < 1:
            self.jugadas = 1
        self.movPeonCap = int(mp)

        for x, linea in enumerate(posicion.split("/")):
            cFil = chr(48 + 8 - x)
            nc = 0
            for c in linea:
                if c.isdigit():
                    nc += int(c)
                else:
                    cCol = chr(nc + 97)
                    self.casillas[cCol + cFil] = c
                    nc += 1

        self.legal()

        return self

    # def fenInverso(self):
        # cp = ControlPosicion()

        # d = {}
        # for casilla, v in self.casillas.iteritems():
            # cCol = casilla[0]
            # cFil = str(9 - int(casilla[1]))
            # d[cCol + cFil] = v
        # cp.casillas = d

        # enroques = self.enroques
        # if enroques != "-":
            # r = ""
            # for c in enroques:
                # if c.isupper():
                    # r += c.lower()
                # else:
                    # r += c.upper()
            # enroques = r
        # cp.enroques = enroques
        # ap = self.alPaso
        # if ap != "-":
            # ap = ap[0] + str(9 - int(ap[1]))
        # cp.alPaso = ap

        # cp.jugadas = self.jugadas
        # cp.movPeonCap = self.movPeonCap

        # cp.siBlancas = not self.siBlancas

        # return cp.fen()

    def setSAK(self):
        nSin = 0
        posicion = ""
        for i in range(8, 0, -1):
            cFil = chr(i + 48)
            fila = ""
            for j in range(8):
                cCol = chr(j + 97)
                clave = cCol + cFil
                v = self.casillas[clave]
                if v is None:
                    nSin += 1
                else:
                    if nSin:
                        fila += "%d" % nSin
                        nSin = 0
                    fila += v
            if nSin:
                fila += "%d" % nSin
                nSin = 0

            posicion += fila
            if i > 1:
                posicion += "/"
        color = "w" if self.siBlancas else "b"

        self.legal()

        self.sak.setXFEN(posicion, color, self.enroques, self.alPaso, self.movPeonCap, self.jugadas)

    def getSAK(self):
        self.leeFen(self.sak.getFEN())

    def fenBase(self):
        nSin = 0
        posicion = ""
        for i in range(8, 0, -1):
            cFil = chr(i + 48)
            fila = ""
            for j in range(8):
                cCol = chr(j + 97)
                clave = cCol + cFil
                v = self.casillas[clave]
                if v is None:
                    nSin += 1
                else:
                    if nSin:
                        fila += "%d" % nSin
                        nSin = 0
                    fila += v
            if nSin:
                fila += "%d" % nSin
                nSin = 0

            posicion += fila
            if i > 1:
                posicion += "/"
        color = "w" if self.siBlancas else "b"
        return posicion + " " + color

    def fenDGT(self):
        nSin = 0
        resp = ""
        for i in range(8, 0, -1):
            cFil = chr(i + 48)
            for j in range(8):
                cCol = chr(j + 97)
                clave = cCol + cFil
                v = self.casillas[clave]
                if v is None:
                    nSin += 1
                else:
                    if nSin:
                        resp += "%d" % nSin
                        nSin = 0
                    resp += v
        return resp

    def fen(self):
        posicion = self.fenBase()

        self.legal()

        return "%s %s %s %d %d" % (posicion, self.enroques, self.alPaso, self.movPeonCap, self.jugadas)

    def fenM2(self):
        """
        Se utiliza en analisis
        """
        fen = self.fen()
        li = fen.split(" ")
        return " ".join(li[:4])

    def siExistePieza(self, pieza, a1h8=None):
        if a1h8:
            return self.casillas[a1h8] == pieza
        else:
            n = 0
            for v in self.casillas.itervalues():
                if v == pieza:
                    n += 1
            return n

    def capturas(self):
        """
        Devuelve las piezas capturadas, liNuestro, liOponente. ( pieza, numero )
        """

        dic = {}
        for pieza, num in ( ("P", 8), ("R", 2), ("N", 2), ("B", 2), ("Q", 1), ("K", 1) ):
            dic[pieza] = num
            dic[pieza.lower()] = num

        for pieza in self.casillas.itervalues():
            if pieza and dic[pieza] > 0:
                dic[pieza] -= 1

        return dic, self.siBlancas

    def moverPV(self, pv):
        return self.mover(pv[:2], pv[2:4], pv[4:])

    def mover(self, desdeA1H8, hastaA1H8, coronacion=None):
        self.setSAK()

        mv = self.sak.moveExPV(desdeA1H8, hastaA1H8, coronacion)
        if not mv:
            return ( False, "Error" )

        self.liExtras = []

        # PZ desde:2 hasta:2 Prom KQ E x
        hasta = mv[3:5]
        prom = mv[5].strip()
        enrK = mv[6] == "K"
        enrQ = mv[6] == "Q"
        enPa = mv[7] == "E"
        # enCp = mv[8] == "x"

        if prom:
            if self.siBlancas:
                prom = prom.upper()
            else:
                prom = prom.lower()
            self.liExtras.append(("c", hasta, prom))

        elif enrK:
            if self.siBlancas:
                self.liExtras.append(( "m", "h1", "f1" ))
            else:
                self.liExtras.append(( "m", "h8", "f8" ))

        elif enrQ:
            if self.siBlancas:
                self.liExtras.append(( "m", "a1", "d1" ))
            else:
                self.liExtras.append(( "m", "a8", "d8" ))

        elif enPa:
            capt = self.alPaso.replace("6", "5").replace("3", "4")
            self.liExtras.append(("b", capt))
        self.getSAK()  # despues de liExtras, por si enpassant, para que

        return ( True, self.liExtras )

    # def tablero(self):
        # resp = "   " + "+---" * 8 + "+" + "\n"
        # for fila in "87654321":
            # resp += " " + fila + " |"
            # for columna in "abcdefgh":
                # pieza = self.casillas[columna + fila]
                # if pieza is None:
                    # resp += "   |"
                    # # ~ resp += "-"+columna+fila + "|"
                # else:
                    # resp += " " + pieza + " |"
            # resp += " " + fila + "\n"
            # resp += "   " + "+---" * 8 + "+" + "\n"
        # resp += "    "
        # for columna in "abcdefgh":
            # resp += " " + columna + "  "

        # return resp

    def pgn(self, desde, hasta, coronacion=None):
        self.setSAK()
        return self.sak.getPGN(desde, hasta, coronacion)

    def pv2dgt(self, desde, hasta, coronacion=None):
        pOri = self.casillas[desde]

        # Enroque
        if pOri in "Kk":
            n = ord(desde[0]) - ord(hasta[0])
            if abs(n) == 2:
                orden = "ke8kc8ra8rd8" if n == 2 else "ke8kg8rh8rf8"
                if pOri == "k":
                    return orden
                else:
                    return orden.replace("k", "K").replace("8", "1")
        # Promotion
        if coronacion:
            coronacion = coronacion.upper() if self.siBlancas else coronacion.lower()
            return pOri + desde + coronacion + hasta

        # Al paso
        if pOri in "Pp" and hasta == self.alPaso:
            if self.siBlancas:
                otro = "p"
                dif = -1
            else:
                otro = "P"
                dif = +1
            casilla = "%s%d" % (hasta[0], int(hasta[1]) + dif)
            return pOri + desde + pOri + hasta + otro + casilla + "." + casilla

        return pOri + desde + pOri + hasta

    def pgnSP(self, desde, hasta, coronacion=None):
        dConv = TrListas.dConv()
        resp = self.pgn(desde, hasta, coronacion)
        for k in dConv.keys():
            if k in resp:
                resp = resp.replace(k, dConv[k])
        return resp

    def siJaque(self):
        self.setSAK()
        return self.sak.isCheck()

    def siTerminada(self):
        self.setSAK()
        li = self.sak.getExMoves()
        return len(li) == 0

    def siFaltaMaterial(self):
        # Rey y Rey
        # Rey + Caballo y Rey
        # Rey + Caballo y Rey y Caballo
        # Rey + alfil y Rey
        # Rey + alfil y Rey + alfil
        negras = ""
        blancas = ""
        for v in self.casillas.itervalues():
            if v:
                if v in "RrQqPp":
                    return False
                if v in "kK":
                    continue
                if v.isupper():
                    blancas += v
                else:
                    negras += v
        lb = len(blancas)
        ln = len(negras)
        if lb > 1 or ln > 1:
            return False

        if lb == 0 and ln == 0:
            return True

        todas = blancas.lower() + negras
        if todas in ["b", "n", "bn", "nb", "bb"]:
            return True

        return False

    def numPiezas(self, pieza):
        if not self.siBlancas:
            pieza = pieza.lower()
        num = 0
        for i in range(8):
            for j in range(8):
                cCol = chr(i + 97)
                cFil = chr(j + 49)
                if self.casillas[cCol + cFil] == pieza:
                    num += 1
        return num

    def totalPiezas(self):
        num = 0
        for i in range(8):
            for j in range(8):
                cCol = chr(i + 97)
                cFil = chr(j + 49)
                if self.casillas[cCol + cFil]:
                    num += 1
        return num

    def pesoWB(self):
        dpesos = {"Q": 110, "N": 30, "B": 32, "R": 50, "P": 10}
        peso = 0

        dposk = {True: [0, 0], False: [0, 0]}
        for i in range(8):
            for j in range(8):
                pieza = self.casillas[chr(i + 97) + chr(j + 49)]
                if pieza == "K":
                    dposk[True] = i, j
                elif pieza == "k":
                    dposk[False] = i, j

        for i in range(8):
            for j in range(8):
                pieza = self.casillas[chr(i + 97) + chr(j + 49)]
                if pieza and pieza.upper() != "K":
                    siW = pieza.isupper()
                    ck, fk = dposk[not siW]
                    d = 14 - (abs(i - ck) + abs(j - fk))
                    valor = d * dpesos[pieza.upper()]
                    if not siW:
                        valor = -valor
                    peso += valor
        return peso

    def distanciaPiezaKenemigo(self, a1):
        pieza = self.casillas[a1]
        if pieza is None:
            return 15
        k = "k" if pieza.isupper() else "K"
        for i in range(8):
            for j in range(8):
                if self.casillas[chr(i + 97) + chr(j + 49)] == k:
                    c = ord(a1[0]) - 97
                    f = int(a1[1]) - 1
                    return abs(i - c) + abs(j - f) - 1

    def siPeonCoronando(self, desdeA1H8, hastaA1H8):
        pieza = self.casillas[desdeA1H8]
        if (not pieza) or (pieza.upper() != "P"):  # or self.casillas[hastaA1H8] is not None:
            return False
        if pieza == "P":
            ori = 7
            dest = 8
        else:
            ori = 2
            dest = 1

        if not (int(desdeA1H8[1]) == ori and int(hastaA1H8[1]) == dest ):
            return False

        return True
