from Code.Constantes import *
import Code.ControlPosicion as ControlPosicion
import Code.Jugada as Jugada
import Code.Gestor as Gestor
import Code.QT.QTUtil as QTUtil
import Code.QT.QTUtil2 as QTUtil2

class GestorMateMap(Gestor.Gestor):

    def inicio(self, workmap):
        self.workmap = workmap

        self.ayudas = 0

        fenInicial = workmap.fenAim()

        self.rivalPensando = False

        self.dicEtiquetasPGN = None

        etiqueta = ""
        if "|" in fenInicial:
            li = fenInicial.split("|")

            fenInicial = li[0]
            if fenInicial.endswith(" 0"):
                fenInicial = fenInicial[:-1] + "1"

            nli = len(li)
            if nli >= 2:
                etiqueta = li[1]

        cp = ControlPosicion.ControlPosicion()
        cp.leeFen(fenInicial)

        self.fen = fenInicial

        siBlancas = cp.siBlancas

        self.partida.reset(cp)

        self.partida.pendienteApertura = False

        self.tipoJuego = kJugWorldMap

        self.siJuegaHumano = False
        self.estado = kJugando
        self.siJuegaPorMi = False

        self.siJugamosConBlancas = siBlancas
        self.siRivalConBlancas = not siBlancas

        self.rmRival = None

        self.siTutorActivado = False
        self.pantalla.ponActivarTutor(False)

        self.ayudasPGN = 0

        liOpciones = [k_mainmenu, k_reiniciar, k_configurar, k_utilidades]
        self.pantalla.ponToolBar(liOpciones)

        self.pantalla.activaJuego(True, False, siAyudas=False)
        self.pantalla.quitaAyudas(True, True)
        self.ponMensajero(self.mueveHumano)
        self.ponPosicion(self.partida.ultPosicion)
        self.mostrarIndicador(True)
        self.ponPiezasAbajo(siBlancas)
        self.ponRotulo1(etiqueta)
        self.ponRotulo2( workmap.nameAim() )
        self.pgnRefresh(True)
        QTUtil.xrefreshGUI()

        self.xrival = self.procesador.creaGestorMotor(self.configuracion.tutor, self.configuracion.tiempoTutor, None)

        self.siAnalizadoTutor = False

        self.ponPosicionDGT()

        self.reiniciando = False
        self.rivalPensando = False
        self.siguienteJugada()

    def procesarAccion(self, clave):
        if clave == k_mainmenu:
            self.finPartida()
            self.procesador.trainingMap(self.workmap.mapa)

        elif clave == k_reiniciar:
            self.reiniciar()

        elif clave == k_configurar:
            self.configurar(siSonidos=True, siCambioTutor=True)

        elif clave == k_utilidades:
            self.utilidades()

        else:
            Gestor.Gestor.rutinaAccionDef(self, clave)

    def reiniciar(self):
        if self.rivalPensando:
            return
        self.inicio(self.workmap)

    def finPartida(self):
        self.procesador.inicio()

    def finalX(self):
        self.finPartida()
        return False

    def siguienteJugada(self):
        if self.estado == kFinJuego:
            return
        self.siPiensaHumano = False

        self.estado = kJugando

        self.siJuegaHumano = False
        self.ponVista()

        siBlancas = self.partida.ultPosicion.siBlancas

        if self.partida.numJugadas() > 0:
            jgUltima = self.partida.liJugadas[-1]
            if jgUltima.siJaqueMate:
                self.ponResultado(kGanamos if self.siJugamosConBlancas == jgUltima.siBlancas() else kGanaRival)
                return
            if jgUltima.siAhogado:
                self.ponResultado(kTablas)
                return
            if jgUltima.siTablasRepeticion:
                self.ponResultado(kTablasRepeticion)
                return
            if jgUltima.siTablas50:
                self.ponResultado(kTablas50)
                return
            if jgUltima.siTablasFaltaMaterial:
                self.ponResultado(kTablasFaltaMaterial)
                return

        self.ponIndicador(siBlancas)
        self.refresh()

        siRival = siBlancas == self.siRivalConBlancas
        if siRival:
            self.piensaRival()

        else:
            self.siJuegaHumano = True
            self.activaColor(siBlancas)

    def piensaRival(self):
        self.rivalPensando = True
        self.pensando(True)
        self.desactivaTodas()

        self.rmRival = self.xrival.juega()

        self.pensando(False)
        desde, hasta, coronacion = self.rmRival.desde, self.rmRival.hasta, self.rmRival.coronacion

        if self.mueveRival(desde, hasta, coronacion):
            self.rivalPensando = False
            self.siguienteJugada()
        else:
            self.rivalPensando = False

    def mueveHumano(self, desde, hasta, coronacion=None):
        if self.siJuegaHumano:
            self.paraHumano()
        else:
            self.sigueHumano()
            return False

        movimiento = desde + hasta

        # Peon coronando
        if not coronacion and self.partida.ultPosicion.siPeonCoronando(desde, hasta):
            coronacion = self.tablero.peonCoronando(self.partida.ultPosicion.siBlancas)
            if coronacion is None:
                self.sigueHumano()
                return False
        if coronacion:
            movimiento += coronacion

        siBien, mens, jg = Jugada.dameJugada(self.partida.ultPosicion, desde, hasta, coronacion)

        if siBien:
            self.movimientosPiezas(jg.liMovs)
            self.masJugada(jg, True)
            self.error = ""
            self.siguienteJugada()
            return True
        else:
            self.sigueHumano()
            self.error = mens
            return False

    def masJugada(self, jg, siNuestra):
        self.partida.liJugadas.append(jg)
        self.partida.ultPosicion = jg.posicion

        # Preguntamos al mono si hay movimiento
        if self.siTerminada():
            jg.siJaqueMate = jg.siJaque
            jg.siAhogado = not jg.siJaque

        resp = self.partida.si3repetidas()
        if resp:
            jg.siTablasRepeticion = True
            rotulo = ""
            for j in resp:
                rotulo += "%d," % (j / 2 + 1,)
            rotulo = rotulo.strip(",")
            self.rotuloTablasRepeticion = rotulo

        if self.partida.ultPosicion.movPeonCap >= 100:
            jg.siTablas50 = True

        if self.partida.ultPosicion.siFaltaMaterial():
            jg.siTablasFaltaMaterial = True

        self.ponFlechaSC(jg.desde, jg.hasta)
        self.beepExtendido(siNuestra)

        self.pgnRefresh(self.partida.ultPosicion.siBlancas)
        self.refresh()

        self.ponPosicionDGT()

    def mueveRival(self, desde, hasta, coronacion):
        siBien, mens, jg = Jugada.dameJugada(self.partida.ultPosicion, desde, hasta, coronacion)
        if siBien:
            self.partida.ultPosicion = jg.posicion

            self.masJugada(jg, False)
            self.movimientosPiezas(jg.liMovs, True)

            self.error = ""

            return True
        else:
            self.error = mens
            return False

    def ponResultado(self, quien):
        self.resultado = quien
        self.desactivaTodas()
        self.siJuegaHumano = False
        self.estado = kFinJuego

        if quien == kTablasRepeticion:
            self.resultado = kTablas

        elif quien == kTablas50:
            self.resultado = kTablas

        elif quien == kTablasFaltaMaterial:
            self.resultado = kTablas

        mensaje = _("Game ended")
        if quien == kGanamos:
            mensaje = _("Congratulations you have win %s.")%self.workmap.nameAim()
            self.workmap.winAim(self.partida.pv())

        QTUtil2.mensaje(self.pantalla, mensaje)

        self.desactivaTodas()
        self.refresh()

    def analizaPosicion(self, fila, clave):
        if self.resultado == kGanamos:
            Gestor.Gestor.analizaPosicion(self, fila, clave)

