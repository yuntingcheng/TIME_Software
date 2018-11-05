import sys
from PyQt5.QtWidgets import QWidget, QApplication, QFrame, QPushButton, QGridLayout, QVBoxLayout
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

class mcegui(QWidget):
    #initializes mcegui class and calls other init functions
    def __init__(self):
        super(mcegui, self).__init__()
        self.init_ui()
        self.MyPopup()

    def init_ui(self):
        self.setWindowTitle('MCE TIME Data')
        self.parametersquit = QVBoxLayout()
        self.parametersquit.addWidget(QPushButton('Quit'))
        self.grid = QGridLayout()
        self.grid.addLayout(self.parametersquit, 1, 1, 1, 1)
        self.setLayout(self.grid)
        self.setGeometry(10, 10, 1920, 1080)
        self.show()

#calls mcegui class to start GUI
def main(args):
    app = QApplication(args)
    app.setApplicationName('TIME Raw Data Visualization Suite')
    ex = mcegui()
    ex.show()
    app.exec_()

if __name__ == '__main__':
    main(sys.argv)
