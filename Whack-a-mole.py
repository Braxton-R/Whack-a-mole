import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class WhackAMole(QWidget):
    def __init__(self):
        super().__init__()
        self.NUM_OF_ROWS = 3
        self.NUM_OF_COLS = 3
        self.score = 0
        # Starts timer
        self.start_timer()
        self.init_ui()
        
    # Set up the main layout
    def init_ui(self):
        
        self.setWindowTitle('Whack-A-Mole')
        self.setGeometry(100, 100, 600, 600)

        self.layout = QVBoxLayout()
        self.score_label = QLabel(f'Score: {self.score}', self)
        self.score_label.setFont(QFont('Arial', 10))
        self.layout.addWidget(self.score_label)

        self.layout = QGridLayout()

        # Creates a grid of buttons using create_buttons function
        self.create_buttons()

        self.setLayout(self.layout)
        self.show()

    # Creates a grid of buttons    
    def create_buttons(self):
        self.buttons = [[QPushButton(' ') for col in range(self.NUM_OF_COLS)] for row in range(self.NUM_OF_ROWS)]

        for row in range(self.NUM_OF_ROWS):
            for col in range(self.NUM_OF_COLS):
                button = self.buttons[row][col]
                button.setFixedSize(150,150)
                button.clicked.connect(lambda ch, row=row, col=col: self.button_clicked(row, col))
                self.layout.addWidget(button, row, col)

    def button_clicked(self, row, col):
        print(f'Button at ({row}, {col}) clicked')
        button = self.sender()
        if button.text() == 'MOLE':
            self.score += 1
            self.move_mole()

    # Gets user input for a time and starts a timer for that time
    def start_timer(self):
        time, ok = QInputDialog.getInt(self, 'Timer', 'Enter a time between 10 and 60 seconds', min = 10, max = 60)
        if ok:
            timer = time*1000
            # Ends game in a certain time period
            QTimer.singleShot(timer, self.end_game)
        else:
            sys.exit(app.exec_())

    def mole_clicked(self):
        pass

    def move_mole(self):
        pass

    def end_game(self):
        QMessageBox.information(self, 'Game Over!', 'Game over!')
        sys.exit(app.exec_())

    def get_score(self):
        pass            

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = WhackAMole()
    sys.exit(app.exec_())