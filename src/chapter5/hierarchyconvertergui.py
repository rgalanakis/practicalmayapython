from qtshim import QtGui, QtCore, Signal


class HierarchyConverterController(QtCore.QObject):
    selectionChanged = Signal(list)

class ConverterWindow(QtGui.QMainWindow):
    convertClicked = Signal(str)

def create_window(controller, parent=None):
    window = ConverterWindow(parent)
    window.setWindowTitle('Hierarchy Converter')
    # change this line
    statusbar = QtGui.QStatusBar()

    container = QtGui.QWidget(window)
    label = QtGui.QLabel('Prefix:', container)
    textbox = QtGui.QLineEdit(container)
    button = QtGui.QPushButton('Convert', container)

    def onclick():
        window.convertClicked.emit(textbox.text())
    button.clicked.connect(onclick)

    def update_statusbar(newsel):
        if not newsel:
            txt = 'Nothing selected.'
        elif len(newsel) == 1:
            txt = '%s selected.' % newsel[0]
        else:
            txt = '%s objects selected.' % len(newsel)
        statusbar.showMessage(txt)
    controller.selectionChanged.connect(update_statusbar)

    layout = QtGui.QHBoxLayout(container)
    container.setLayout(layout)
    layout.addWidget(label)
    layout.addWidget(textbox)
    layout.addWidget(button)
    window.setCentralWidget(container)
    # add this line
    window.setStatusBar(statusbar)

    return window

def _pytest():
    import random

    controller = HierarchyConverterController()
    def nextsel():
        return random.choice([
            [],
            ['single'],
            ['single', 'double']
        ])

    def onconvert(prefix):
        print 'Convert clicked! Prefix:', prefix
        controller.selectionChanged.emit(nextsel())

    app = QtGui.QApplication([])
    win = create_window(controller)
    win.convertClicked.connect(onconvert)
    win.show()
    app.exec_()

if __name__ == '__main__':
    _pytest()
