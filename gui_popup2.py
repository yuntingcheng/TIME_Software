import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QPushButton, QGridLayout, QMainWindow
from PyQt5.QtCore import QRect, QPropertyAnimation, QState, QStateMachine

class MyPopup(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        style1 = "background-color: red"
        style2 = "background-color: black"

        animation = QPropertyAnimation(self, b'styleSheet')
        animation.setDuration(5)

        state1 = QState()
        state2 = QState()
        state1.assignProperty(self, 'styleSheet', style1)
        state2.assignProperty(self, 'styleSheet', style2)

        state1.addTransition(state1.propertiesAssigned, state2)
        state2.addTransition(state2.propertiesAssigned, state1)

        self.machine = QStateMachine()
        self.machine.addDefaultAnimation(animation)
        self.machine.addState(state1)
        self.machine.addState(state2)
        self.machine.setInitialState(state1)
        self.machine.start()

class MainWindow(QMainWindow):
    def __init__(self, *args):
        QMainWindow.__init__(self, *args)
        self.cw = QWidget(self)
        self.setCentralWidget(self.cw)
        self.btn1 = QPushButton("Click me", self.cw)
        self.btn1.setGeometry(QRect(0, 0, 100, 30))
        self.connect(self.btn1, SIGNAL("clicked()"), self.doit)
        self.w = None

    def doit(self):
        self.w = MyPopup()
        self.w.setGeometry(QRect(100, 100, 400, 200))
        self.w.show()

class App(QApplication):
    def __init__(self, *args):
        QApplication.__init__(self, *args)
        self.main = MainWindow()
        self.connect(self, SIGNAL("lastWindowClosed()"), self.byebye )
        self.main.show()

    def byebye( self ):
        self.exit(0)

def main(args):
    global app
    app = App(args)
    app.exec_()

if __name__ == "__main__":
    main(sys.argv)
