import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import random

class WhackAMole(QWidget):
    def __init__(self):
        super().__init__()
        self.NUM_OF_ROWS = 3
        self.NUM_OF_COLS = 3
        self.MIN_NUM_OF_ROWS = 0
        self.MIN_NUM_OF_COLS = 0
        # -1 Because the computer starts counting from 0, not 1
        self.MAX_NUM_OF_ROWS = self.NUM_OF_ROWS - 1
        self.MAX_NUM_OF_COLS = self.NUM_OF_COLS - 1
        self.score = 0
        self.current_mole_button = None
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
        
        self.move_mole()

        self.setLayout(self.layout)
        self.show()

    # Creates a grid of buttons    
    def create_buttons(self):
        self.buttons = [[QPushButton(' ') for col in range(self.NUM_OF_COLS)] for row in range(self.NUM_OF_ROWS)]

        for row in range(self.NUM_OF_ROWS):
            for col in range(self.NUM_OF_COLS):
                button = self.buttons[row][col]
                button.setFixedSize(150,150)
                button.clicked.connect(lambda ch, row=row, col=col: self.button_clicked())
                self.layout.addWidget(button, row, col)

    def button_clicked(self):
        button = self.sender()
        if button.text() == 'MOLE':
            button.setText('')
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

    def move_mole(self):
        # Randomly selects a button and turns text to 'MOLE'
        row = random.randint(self.MIN_NUM_OF_ROWS,self.MAX_NUM_OF_ROWS)
        col = random.randint(self.MIN_NUM_OF_COLS,self.MAX_NUM_OF_COLS)
        self.buttons[row][col].setText('MOLE')
            
    def end_game(self):
        QMessageBox.information(self, 'Game Over!', 'Game over!')
        self.get_score()
        sys.exit(app.exec_())

    # Stores the score variable in a seperate txt file
    def get_score(self):
        with open('score.txt', 'w') as file:
            file.write(f'You got a score of: {self.score}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = WhackAMole()
    sys.exit(app.exec_())