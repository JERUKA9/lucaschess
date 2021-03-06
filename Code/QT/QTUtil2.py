import time

from PyQt4 import QtCore, QtGui

from Code.Constantes import *
import Code.VarGen as VarGen
import Code.QT.QTUtil as QTUtil
import Code.QT.Colocacion as Colocacion
import Code.QT.Iconos as Iconos
import Code.QT.Controles as Controles

def dicTeclas():
    dic = {
        16777234: kMoverAtras,
        16777236: kMoverAdelante,
        16777235: kMoverAtras,
        16777237: kMoverAdelante,
        16777232: kMoverInicio,
        16777233: kMoverFinal
    }
    return dic

def leeCarpeta(owner, carpeta, titulo=None):
    if titulo is None:
        titulo = _("Open Directory")
    return QtGui.QFileDialog.getExistingDirectory(owner, titulo, carpeta,
                                                  QtGui.QFileDialog.ShowDirsOnly | QtGui.QFileDialog.DontResolveSymlinks)

def _lfTituloFiltro(extension, titulo):
    if titulo is None:
        titulo = _("File")
    if " " in extension:
        filtro = extension
    else:
        pathext = "*.%s" % extension
        if extension == "*" and VarGen.isLinux:
            pathext = "*"
        filtro = _("File") + " %s (%s)" % (extension, pathext)
    return titulo, filtro

def leeFichero(owner, carpeta, extension, titulo=None):
    titulo, filtro = _lfTituloFiltro(extension, titulo)
    resp = QtGui.QFileDialog.getOpenFileName(owner, titulo, carpeta, filtro)
    # if resp : #+pyside
    # resp = resp[0] #+pyside
    return resp

def leeCreaFichero(owner, carpeta, extension, titulo=None):
    titulo, filtro = _lfTituloFiltro(extension, titulo)
    fd = QtGui.QFileDialog(owner, titulo)
    fd.setFilter(filtro)
    fd.setDirectory(carpeta)
    fd.setFileMode(fd.AnyFile)
    # fd.setOptions(fd.ShowDirsOnly)
    if fd.exec_():
        fileNames = fd.selectedFiles()
        return fileNames[0] if fileNames else None
    else:
        return None

def salvaFichero(pantalla, titulo, carpeta, filtro, siConfirmarSobreescritura=True):
    if siConfirmarSobreescritura:
        resp = QtGui.QFileDialog.getSaveFileName(pantalla, titulo, carpeta, filtro)
    else:
        resp = QtGui.QFileDialog.getSaveFileName(pantalla, titulo, carpeta, filtro,
                                                 options=QtGui.QFileDialog.DontConfirmOverwrite)
        # if resp : #+pyside
        # resp = resp[0] #+pyside
    return resp

class MensEspera(QtGui.QWidget):
    def __init__(self, parent, mensaje, siCancelar, siMuestraYa, opacity, posicion, fixedSize, titCancelar, background, pmImagen=None):

        assert parent is not None

        super(MensEspera, self).__init__(parent)

        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.FramelessWindowHint)
        self.setStyleSheet("QWidget, QLabel { background: %s }" % background)
        lbi = QtGui.QLabel(self)
        lbi.setPixmap(pmImagen if pmImagen else Iconos.pmMensEspera())
        if fixedSize:
            self.setFixedWidth(fixedSize)

        self.owner = parent

        self.posicion = posicion

        self.lb = lb = Controles.LB(parent, resalta(mensaje)).ponFuente(Controles.TipoLetra(puntos=12)).ponWrap()

        if siCancelar:
            self.siCancelado = False
            if not titCancelar:
                titCancelar = _("Cancel")
            self.btCancelar = Controles.PB(self, titCancelar, rutina=self.cancelar, plano=False).ponIcono(
                Iconos.Cancelar()).anchoFijo(100)

        ly = Colocacion.G().control(lbi, 0, 0, 3, 1).control(lb, 1, 1)
        if siCancelar:
            ly.controlc(self.btCancelar, 2, 1)

        ly.margen(12)
        self.setLayout(ly)
        self.teclaPulsada = None

        self.setWindowOpacity(opacity)
        if siMuestraYa:
            self.muestra()

    def cancelar(self):
        self.siCancelado = True

    def cancelado(self):
        QTUtil.refreshGUI()
        return self.siCancelado

    def activarCancelar(self, siActivar):
        self.btCancelar.setVisible(siActivar)
        QTUtil.refreshGUI()
        return self

    def keyPressEvent(self, event):
        QtGui.QWidget.keyPressEvent(self, event)
        self.teclaPulsada = event.key()

    def rotulo(self, nuevo):
        self.lb.ponTexto(resalta(nuevo))
        QTUtil.refreshGUI()

    def muestra(self):
        self.show()

        v = self.owner
        s = self.size()
        if self.posicion == "c":
            x = v.x() + (v.width() - s.width()) / 2
            y = v.y() + (v.height() - s.height()) / 2
        elif self.posicion == "ad":
            x = v.x() + v.width() - s.width()
            y = v.y() + 4
        self.move(x, y)
        QTUtil.refreshGUI()
        return self

    def final(self):
        QTUtil.refreshGUI()
        self.hide()
        self.close()
        self.destroy()
        QTUtil.refreshGUI()

class ControlMensEspera:
    def __init__(self):
        self.me = None

    def inicio(self, parent, mensaje, siCancelar=False, siMuestraYa=True, opacity=0.80,
               posicion="c", fixedSize=256, titCancelar=None, background=None, pmImagen=None):
        QTUtil.refreshGUI()
        if self.me:
            self.final()
        if background is None:
            background = "#79b600"
        self.me = MensEspera(parent, mensaje, siCancelar, siMuestraYa, opacity, posicion, fixedSize, titCancelar,
                             background, pmImagen)
        QTUtil.refreshGUI()
        return self

    def final(self):
        if self.me:
            self.me.final()
            self.me = None

    def rotulo(self, txt):
        self.me.rotulo(txt)

    def cancelado(self):
        if self.me:
            return self.me.cancelado()
        return True

    def teclaPulsada(self, k):
        if self.me is None:
            return False
        if self.me.teclaPulsada:
            resp = self.me.teclaPulsada == k
            self.me.teclaPulsada = None
            return resp
        else:
            return False

mensEspera = ControlMensEspera()

def mensajeTemporal(pantalla, mensaje, segundos, background=None, pmImagen=None):
    cme = ControlMensEspera()
    me = cme.inicio(pantalla, mensaje, background=background, pmImagen=pmImagen)
    time.sleep(segundos)
    me.final()

class BarraProgreso2(QtGui.QDialog):
    def __init__(self, owner, titulo, formato1="%v/%m", formato2="%v/%m"):
        QtGui.QDialog.__init__(self, owner)

        self.owner = owner

        # self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle(titulo)

        # gb1 + progress
        self.bp1 = QtGui.QProgressBar()
        self.bp1.setFormat(formato1)
        ly = Colocacion.H().control(self.bp1)
        self.gb1 = Controles.GB(self, "", ly)

        # gb2 + progress
        self.bp2 = QtGui.QProgressBar()
        self.bp2.setFormat(formato2)
        ly = Colocacion.H().control(self.bp2)
        self.gb2 = Controles.GB(self, "", ly)

        # cancelar
        bt = Controles.PB(self, _("Cancel"), self.cancelar, plano=False)  # .ponIcono( Iconos.Delete() )
        lyBT = Colocacion.H().relleno().control(bt)

        layout = Colocacion.V().control(self.gb1).control(self.gb2).otro(lyBT)

        self.setLayout(layout)
        self._siCancelado = False

    def closeEvent(self, event):
        self._siCancelado = True
        self.cerrar()

    def mostrar(self):
        self.move(self.owner.x() + (self.owner.width() - self.width()) / 2,
                  self.owner.y() + (self.owner.height() - self.height()) / 2)
        self.show()
        return self

    def mostrarAD(self):
        self.move(self.owner.x() + self.owner.width() - self.width(), self.owner.y())
        self.show()
        return self

    def cerrar(self):
        self.reject()
        QTUtil.refreshGUI()

    def cancelar(self):
        self._siCancelado = True
        self.cerrar()

    def ponRotulo(self, cual, texto):
        gb = self.gb1 if cual == 1 else self.gb2
        gb.ponTexto(texto)

    def ponTotal(self, cual, maximo):
        bp = self.bp1 if cual == 1 else self.bp2
        bp.setRange(0, maximo)

    def pon(self, cual, valor):
        bp = self.bp1 if cual == 1 else self.bp2
        bp.setValue(valor)

    def siCancelado(self):
        QTUtil.refreshGUI()
        return self._siCancelado

class BarraProgreso1(QtGui.QDialog):
    def __init__(self, owner, titulo, formato1="%v/%m"):
        QtGui.QDialog.__init__(self, owner)

        self.owner = owner

        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle(titulo)

        # gb1 + progress
        self.bp1 = QtGui.QProgressBar()
        self.bp1.setFormat(formato1)
        ly = Colocacion.H().control(self.bp1)
        self.gb1 = Controles.GB(self, "", ly)

        # cancelar
        bt = Controles.PB(self, _("Cancel"), self.cancelar, plano=False)
        lyBT = Colocacion.H().relleno().control(bt)

        layout = Colocacion.V().control(self.gb1).otro(lyBT)

        self.setLayout(layout)
        self._siCancelado = False

    def closeEvent(self, event):
        self._siCancelado = True
        self.cerrar()

    def mostrar(self):
        self.move(self.owner.x() + (self.owner.width() - self.width()) / 2,
                  self.owner.y() + (self.owner.height() - self.height()) / 2)
        self.show()
        return self

    def mostrarAD(self):
        self.move(self.owner.x() + self.owner.width() - self.width(), self.owner.y())
        self.show()
        return self

    def cerrar(self):
        self.hide()
        self.reject()
        QTUtil.refreshGUI()

    def cancelar(self):
        self._siCancelado = True
        self.cerrar()

    def ponRotulo(self, texto):
        self.gb1.ponTexto(texto)

    def ponTotal(self, maximo):
        self.bp1.setRange(0, maximo)

    def pon(self, valor):
        self.bp1.setValue(valor)

    def siCancelado(self):
        QTUtil.refreshGUI()
        return self._siCancelado

class BarraProgreso(QtGui.QProgressDialog):
    # ~ bp = QTUtil2.BarraProgreso( self, "me", 5 ).mostrar()
    # ~ n = 0
    #~ for n in range(5):
    #~ prlk( n )
    #~ bp.pon( n )
    #~ time.sleep(1)
    #~ if bp.siCancelado():
    #~ break
    #~ bp.cerrar()

    def __init__(self, owner, titulo, mensaje, total):
        QtGui.QProgressDialog.__init__(self, mensaje, _("Cancel"), 0, total, owner)
        self.total = total
        self.actual = 0
        self.setWindowModality(QtCore.Qt.WindowModal)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)
        self.setWindowTitle(titulo)
        self.owner = owner

    def mostrar(self):
        if self.owner:
            self.move(self.owner.x() + (self.owner.width() - self.width()) / 2,
                      self.owner.y() + (self.owner.height() - self.height()) / 2)
        self.show()
        return self

    def mostrarAD(self):
        if self.owner:
            self.move(self.owner.x() + self.owner.width() - self.width(), self.owner.y())
        self.show()
        return self

    def cerrar(self):
        self.setValue(self.total)
        self.close()

    def mensaje(self, mens):
        self.setLabelText(mens)

    def siCancelado(self):
        QTUtil.refreshGUI()
        return self.wasCanceled()

    def ponTotal(self, total):
        self.setMaximum(total)
        self.pon(0)

    def pon(self, valor):
        self.setValue(valor)
        self.actual = valor

    def inc(self):
        self.pon(self.actual + 1)

def resalta(mens, tipo=4):
    return ("<h%d>%s</h%d>" % ( tipo, mens, tipo)).replace("\n", "<br>")

def mensaje(parent, mens, titulo=None, siResalta=True, siArribaDerecha=False):
    w = Mensaje(parent, mens, titulo, siResalta)
    if siArribaDerecha:
        w.move(parent.x() + parent.width() - w.width(), parent.y())
        # w.show()
    w.muestra()

class Mensaje(QtGui.QDialog):
    def __init__(self, parent, mens, titulo=None, siResalta=True):
        super(Mensaje, self).__init__(parent)

        if titulo is None:
            titulo = _("Message")
        if siResalta:
            mens = resalta(mens)

        self.setWindowTitle(titulo)
        self.setWindowFlags(QtCore.Qt.Dialog | QtCore.Qt.WindowTitleHint)
        # ~ self.setStyleSheet("QDialog, QLabel { background: #79b600 }")

        lbi = QtGui.QLabel(self)
        lbi.setPixmap(Iconos.pmInformacion())

        lbm = Controles.LB(self, mens)
        bt = Controles.PB(self, _("Continue"), rutina=self.accept, plano=False)

        ly = Colocacion.G().control(lbi, 0, 0).control(lbm, 0, 1).controld(bt, 1, 1)

        ly.margen(10)
        self.setLayout(ly)

    def muestra(self):
        QTUtil.refreshGUI()
        self.exec_()
        QTUtil.refreshGUI()

def mensError(parent, mens):
    msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, _("Error"), resalta(mens), parent=parent)
    msgBox.addButton(_("Continue"), QtGui.QMessageBox.ActionRole)
    msgBox.exec_()

def mensErrorSobreControl(owner, mens, control):
    msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Warning, _("Error"), resalta(mens), parent=owner)
    msgBox.addButton(_("Continue"), QtGui.QMessageBox.ActionRole)
    msgBox.move(owner.x() + control.x(), owner.y() + control.y())
    msgBox.exec_()

def pregunta(parent, mens, etiSi=None, etiNo=None):
    msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Question, _("Question"), resalta(mens), parent=parent)
    if etiSi is None:
        etiSi = _("Yes")
    if etiNo is None:
        etiNo = _("No")
    siButton = msgBox.addButton(etiSi, QtGui.QMessageBox.YesRole)
    msgBox.addButton(etiNo, QtGui.QMessageBox.NoRole)
    msgBox.exec_()
    return msgBox.clickedButton() == siButton

def preguntaCancelar(parent, mens, si, no):
    msgBox = QtGui.QMessageBox(QtGui.QMessageBox.Question, _("Question"), resalta(mens), parent=parent)
    siButton = msgBox.addButton(si, QtGui.QMessageBox.YesRole)
    noButton = msgBox.addButton(no, QtGui.QMessageBox.NoRole)
    msgBox.addButton(_("Cancel"), QtGui.QMessageBox.RejectRole)
    msgBox.exec_()
    cb = msgBox.clickedButton()
    if cb == siButton:
        resp = True
    elif cb == noButton:
        resp = False
    else:
        resp = None
    return resp

def tbAcceptCancel(parent, siDefecto=False, siReject=True):
    liAcciones = [( _("Accept"), Iconos.Aceptar(), parent.aceptar ),
                  None,
                  ( _("Cancel"), Iconos.Cancelar(), parent.reject if siReject else parent.cancelar ),
    ]
    if siDefecto:
        liAcciones.append(None)
        liAcciones.append(( _("Default"), Iconos.Defecto(), parent.defecto ))
    liAcciones.append(None)

    return Controles.TBrutina(parent, liAcciones)

# class Proceso(QtCore.QProcess):

# def __init__( self, exe ):

# QtCore.QProcess.__init__( self )
# self.setWorkingDirectory ( os.path.abspath(os.path.dirname(exe)) )
# self.start( exe, [] )

# self.waitForStarted()

# def escribeLinea( self, linea ):
# self.write( str(linea + "\n") )

# def esperaRespuesta( self, segundos = None ):
# if segundos:
# total = segundos*1000
# self.waitForReadyRead(total)
# #~ bloque = 100
# #~ while not self.waitForReadyRead(bloque):
# #~ total -= bloque
# #~ QtCore.QCoreApplication.processEvents()
# #~ QtGui.QApplication.processEvents()
# #~ if total <= 0:
# #~ return ""

# else:
# self.waitForReadyRead()
# return str(self.readAllStandardOutput())

# def terminar( self ):
# try:
# self.close()
# except:
# pass

def tiposDeLineas():
    li = (
        ( _("No pen"), 0 ),
        ( _("Solid line"), 1 ),
        ( _("Dash line"), 2 ),
        ( _("Dot line"), 3 ),
        ( _("Dash dot line"), 4 ),
        ( _("Dash dot dot line"), 5 ),
    )
    return li

def listaOrdenes():
    li = []
    for k in range(5, 30):
        txt = "%2d" % (k - 4,)
        if k == kZvalue_pieza:
            txt += " => " + _("Piece")
        elif k == kZvalue_piezaMovimiento:
            txt += " => " + _("Moving piece")

        li.append((txt, k))
    return li

def spinBoxLB(owner, valor, desde, hasta, etiqueta=None, maxTam=None):
    ed = Controles.SB(owner, valor, desde, hasta)
    if maxTam:
        ed.tamMaximo(maxTam)
    if etiqueta:
        label = Controles.LB(owner, etiqueta + ": ")
        return ed, label
    else:
        return ed

def comboBoxLB(parent, liOpciones, valor, etiqueta=None):
    cb = Controles.CB(parent, liOpciones, valor)
    if etiqueta:
        return cb, Controles.LB(parent, etiqueta + ": ")
    else:
        return cb

def unMomento(owner):
    return mensEspera.inicio(owner, _("One moment please..."))

def analizando(owner):
    return mensEspera.inicio(owner, _("Analyzing the move...."), posicion="ad")

def ponIconosMotores(lista):
    liResp = []
    for titulo, clave in lista:
        liResp.append((titulo, clave, Iconos.PuntoEstrella() if clave.startswith("*") else Iconos.PuntoVerde() ))
    return liResp

