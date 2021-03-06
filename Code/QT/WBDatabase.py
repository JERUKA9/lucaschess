from PyQt4 import QtGui

import Code.DBgames as DBgames
import Code.BookGuide as BookGuide
import Code.QT.Iconos as Iconos
import Code.QT.Controles as Controles
import Code.QT.Colocacion as Colocacion
import Code.QT.QTVarios as QTVarios
import Code.QT.WBG_Games as WBG_Games
import Code.QT.WBG_Summary as WBG_Summary
import Code.QT.WBG_InfoMove as WBG_InfoMove

class WBDatabase(QTVarios.WDialogo):
    def __init__(self, wParent, procesador):

        icono = Iconos.DatabaseC()
        extparam = "database"
        titulo = _("Database of complete games")
        QTVarios.WDialogo.__init__(self, wParent, titulo, icono, extparam)

        self.procesador = procesador
        self.configuracion = procesador.configuracion

        self.dbGames = DBgames.DBgames(self.configuracion.ficheroDBgames)

        dicVideo = self.recuperarDicVideo()

        self.bookGuide = BookGuide.BookGuide(self)
        self.wsummary = WBG_Summary.WSummary(procesador, self, self.dbGames, siMoves=False)

        self.wgames = WBG_Games.WGames(procesador, self, self.dbGames, self.wsummary, siMoves=False)

        self.registrarGrid(self.wsummary.grid)
        self.registrarGrid(self.wgames.grid)

        self.ultFocus = None

        self.tab = Controles.Tab()
        self.tab.nuevaTab(self.wgames, _("Games"))
        self.tab.nuevaTab(self.wsummary, _("Summary"))
        self.tab.dispatchChange(self.tabChanged)
        self.tab.ponTipoLetra(puntos=procesador.configuracion.puntosTB)

        self.infoMove = WBG_InfoMove.WInfomove(self, siMoves=False)

        self.splitter = splitter = QtGui.QSplitter()
        splitter.addWidget(self.tab)
        splitter.addWidget(self.infoMove)

        layout = Colocacion.H().control(splitter).margen(5)

        self.setLayout(layout)

        self.recuperarVideo(anchoDefecto=1200, altoDefecto=600)
        if not dicVideo:
            dicVideo = {
                'SPLITTER': [800, 380],
                'TREE_1': 25,
                'TREE_2': 25,
                'TREE_3': 50,
                'TREE_4': 661,
            }
        sz = dicVideo.get("SPLITTER", None)
        if sz:
            self.splitter.setSizes(sz)

        self.inicializa()

    def cambiaDBgames(self, fich):
        self.dbGames.close()
        self.dbGames = DBgames.DBgames(self.configuracion.ficheroDBgames)
        self.setdbGames()
        self.wsummary.actualizaPV(None)

    def setdbGames(self):
        self.tab.ponValor(0, "%s: %s" % (_("Database"), self.dbGames.rotulo() ))
        self.wsummary.setdbGames(self.dbGames)
        self.wgames.setdbGames(self.dbGames)

    def tabChanged(self, ntab):
        QtGui.QApplication.processEvents()
        tablero = self.infoMove.tablero
        tablero.desactivaTodas()
        if ntab == 0:
            self.wgames.actualiza()

    def inicializa(self):
        self.wsummary.setInfoMove(self.infoMove)
        self.wgames.setInfoMove(self.infoMove)
        self.setdbGames()
        self.wsummary.actualizaPV(None)
        self.wgames.actualiza(True)

    def terminar(self):
        self.salvar()
        self.accept()

    def salvar(self):
        dicExten = {
            "SPLITTER": self.splitter.sizes(),
        }

        self.guardarVideo(dicExten)

        self.dbGames.close()

    def closeEvent(self, event):
        self.salvar()

