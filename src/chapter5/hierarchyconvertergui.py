from PySide import QtGui, QtCore

def create_window():
    win = QtGui.QMainWindow()
    return win


if __name__ == '__main__':
    app = QtGui.QApplication([])
    win = create_window()
    win.show()
    app.exec_()

# Version 2

def create_window():
    # Create the widgets, starting with a window
    window = QtGui.QMainWindow()
    # Create a container that is parented to the window
    container = QtGui.QWidget(window)
    # Create a textbox that is parented to the container
    textbox = QtGui.QTextBox(container)

    # Now, set up the layout.
    layout = QtGui.QHBoxLayout(container)
    container.setLayout(layout)
    layout.addWidget(textbox)


    # Return the window so it can be shown
    return window


# Version 3

def create_window():
    window = QtGui.QMainWindow()
    # Always set the window title to something meaningful!
    window.setTitle("Skeleton Converter")
    container = QtGui.QWidget(window)

    label = QtGui.QLabel("Prefix:", container)
    textbox = QtGui.QTextBox(container)
    button = QtGui.QPushButton("Convert", container)

    layout = QtGui.QHBoxLayout(container)
    container.setLayout(layout)
    # Add them to the layout, first widget added is left-most
    layout.addWidget(label)
    layout.addWidget(textbox)
    layout.addWidget(button)

    return window


# Version 4

def create_window():
    window = QtGui.QMainWindow()
    # Always set the window title to something meaningful!
    window.setTitle("Skeleton Converter")
    container = QtGui.QWidget(window)

    label = QtGui.QLabel("Prefix:", container)
    textbox = QtGui.QTextBox(container)
    button = QtGui.QPushButton("Convert", container)

    window.convertClicked = QtCore.Signal(str)
    def onclick():
        window.convertClicked.emit(textbox.text())
    button.clicked.connect(onclick)

    layout = QtGui.QHBoxLayout(container)
    container.setLayout(layout)
    # Add them to the layout, first widget added is left-most
    layout.addWidget(label)
    layout.addWidget(textbox)
    layout.addWidget(button)

    return window

if __name__ == '__main__':
    def onconvert(prefix):
        print 'Convert clicked! Prefix:', prefix
    app = QtGui.QApplication([])
    win = create_window()
    win.convertClicked.connect(onconvert)
    win.show()
    app.exec_()


# Version 5

class HierarchyConverterController(object):
    selectionChanged = QtCore.Signal()

def create_window(controller):
    window = QtGui.QMainWindow()
    # Always set the window title to something meaningful!
    window.setTitle("Skeleton Converter")
    container = QtGui.QWidget(window)

    label = QtGui.QLabel("Prefix:", container)
    textbox = QtGui.QTextBox(container)
    button = QtGui.QPushButton("Convert", container)

    window.convertClicked = QtCore.Signal(str)
    def onclick():
        window.convertClicked.emit(textbox.text())
    button.clicked.connect(onclick)

    def onSelChanged(newsel):
        sb = window.statusBar()
        if not newsel:
            txt = 'Nothing selected.'
        elif len(newsel) == 1:
            txt = '%s selected.' % newsel[0]
        else:
            txt = '%s objects selected.' % len(newsel)
        sb.setText(txt)
    controller.selectionChanged.connect(onSelChanged)

    layout = QtGui.QHBoxLayout(container)
    container.setLayout(layout)
    # Add them to the layout, first widget added is left-most
    layout.addWidget(label)
    layout.addWidget(textbox)
    layout.addWidget(button)

    return window

if __name__ == '__main__':
    def onconvert():
        print 'Convert clicked!'
    app = QtGui.QApplication([])
    controller = HierarchyConverterController()
    win = create_window(controller)
    win.convertClicked.connect(onconvert)
    win.show()
    app.exec_()


# Version 6

import threading


def _pytest():
    def onconvert():
        print 'Convert clicked!'

    app = QtGui.QApplication([])

    controller = HierarchyConverterController()
    def nextsel():
        while True:
            yield []
            yield ['single']
            yield ['single', 'double']
    getnextsel = nextsel().next

    def starttimer():
        controller.selectionChanged.emit(getnextsel())
        threading.Timer(2, starttimer)
    starttimer()

    win = create_window(controller)
    win.convertClicked.connect(onconvert)
    win.show()
    app.exec_()

if __name__ == '__main__':
    _pytest()


def create_window(controller, parent=None):
    window = QtGui.QMainWindow(parent)
    # Always set the window title to something meaningful!
    window.setTitle("Skeleton Converter")
    container = QtGui.QWidget(window)

    label = QtGui.QLabel("Prefix:", container)
    textbox = QtGui.QTextBox(container)
    button = QtGui.QPushButton("Convert", container)

    window.convertClicked = QtCore.Signal(str)
    def onclick():
        window.convertClicked.emit(textbox.text())
    button.clicked.connect(onclick)

    def onSelChanged(newsel):
        sb = window.statusBar()
        if not newsel:
            txt = 'Nothing selected.'
        elif len(newsel) == 1:
            txt = '%s selected.' % newsel[0]
        else:
            txt = '%s objects selected.' % len(newsel)
        sb.setText(txt)
    controller.selectionChanged.connect(onSelChanged)

    layout = QtGui.QHBoxLayout(container)
    container.setLayout(layout)
    # Add them to the layout, first widget added is left-most
    layout.addWidget(label)
    layout.addWidget(textbox)
    layout.addWidget(button)

    return window
