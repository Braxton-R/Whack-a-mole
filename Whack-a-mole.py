import sys
from PyQt5.QtWidgets import *
from PyQt5 import QtCore, QtGui
from PyQt5.QtGui import QFont
from PyQt5.QtCore import QTimer
import random

class WhackAMole(QWidget):
    def __init__(self):
        super().__init__()
        # CONSTANTS
        self.NUM_OF_ROWS = 3
        self.NUM_OF_COLS = 3
        self.MIN_NUM_OF_ROWS = 0
        self.MIN_NUM_OF_COLS = 0
        # -1 Because the computer starts counting from 0, not 1
        self.MAX_NUM_OF_ROWS = self.NUM_OF_ROWS - 1
        self.MAX_NUM_OF_COLS = self.NUM_OF_COLS - 1
        # How often the mole is moved in milliseconds
        self.MOVE_MOLE_TIME = 1000
        # Constant size of square buttons
        self.BUTTON_SIZE = 150
        # Constants for the min and max time frame that can be inputted at the start of the game
        self.MIN_GAME_TIME = 10
        self.MAX_GAME_TIME = 60
        # Value that keeps track of the score
        self.score = 0
        # Value that keeps track of the current mole position
        self.current_mole_button = None
        # Starts a timer
        # Length of time depends on user input
        self.start_timer()
        self.init_ui()
        
    # Set up the user interface components of the game
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

        # Creates a repeating timer that moves the mole
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.move_mole)
        self.timer.start(self.MOVE_MOLE_TIME)
        

        self.setLayout(self.layout)
        # Shows the grid and layout
        self.show()

    # Creates a grid of buttons    
    def create_buttons(self):
        self.buttons = [[QPushButton(' ') for col in range(self.NUM_OF_COLS)] for row in range(self.NUM_OF_ROWS)]

        for row in range(self.NUM_OF_ROWS):
            for col in range(self.NUM_OF_COLS):
                button = self.buttons[row][col]
                button.setFixedSize(self.BUTTON_SIZE,self.BUTTON_SIZE)
                button.clicked.connect(lambda ch, row=row, col=col: self.button_clicked())
                self.layout.addWidget(button, row, col)

    # Function that gets called if button is clicked and checks if the mole was hit
    def button_clicked(self):
        button = self.sender()
        # Increases score if the button clicked has the 'MOLE' in it
        if button.text() == 'MOLE':
            button.setText('')
            # Increases score by 1
            self.score += 1
            # Updates the score label in the top left of game
            self.update_score()
            # Randomly moves the mole to a new button
            self.move_mole()

    # Gets user input for a time and starts a timer for that time
    def start_timer(self):
        # Prompts the user to input a time between 10 and 60 seconds for the game duration
        time, ok = QInputDialog.getInt(self, 'Timer', f'Enter a time between {self.MIN_GAME_TIME} and {self.MAX_GAME_TIME} seconds', min = self.MIN_GAME_TIME, max = self.MAX_GAME_TIME)
        if ok:
            # times 1000 to convert time inputted to milliseconds
            TIMER = time*1000
            # Ends game in a certain time period
            QTimer.singleShot(TIMER, self.end_game)
        else:
            sys.exit(app.exec_())

    # Randomly moves the mole to a new button, ensuring it doesn't select the same button twice
    def move_mole(self):
        # Clears previous MOLE button
        if self.current_mole_button:
            self.current_mole_button.setText('')
        
        while True:
            # Randomly selects a button and turns text to 'MOLE'
            row = random.randint(self.MIN_NUM_OF_ROWS,self.MAX_NUM_OF_ROWS)
            col = random.randint(self.MIN_NUM_OF_COLS,self.MAX_NUM_OF_COLS)
            new_mole_button = self.buttons[row][col]
            if new_mole_button != self.current_mole_button:
                self.current_mole_button = new_mole_button
                self.current_mole_button.setText('MOLE')
                break

    # Ends the game whenever this function is called        
    def end_game(self):
        QMessageBox.information(self, 'Game Over!', 'Game over!')
        self.get_score()
        sys.exit(app.exec_())

    # Stores the score variable in a separate txt file
    def get_score(self):
        with open('score.txt', 'w') as file:
            file.write(f'You got a score of: {self.score}')

    # Updates score label
    def update_score(self):
        self.score_label.setText(f'Score: {self.score}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    game = WhackAMole()
    sys.exit(app.exec_())