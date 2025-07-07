import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLineEdit, 
                            QPushButton, QWidget, QGridLayout, QHBoxLayout, 
                            QTabWidget, QDockWidget, QListWidget, QMenuBar, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeyEvent

class CalculatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Simple Calculator")
        self.setFixedSize(300, 400)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)
        
        self.create_display()
        self.create_buttons()
        
        self.current_input = ""
        self.previous_input = ""
        self.operation = None
        
    def create_display(self):
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 24px; padding: 10px;")
        self.display.setMaxLength(15)
        self.layout.addWidget(self.display)
        
    def create_buttons(self):
        buttons_layout = QGridLayout()
        
        # Button labels
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]
        
        # Create and add buttons to the grid
        for i, text in enumerate(buttons):
            button = QPushButton(text)
            button.setStyleSheet("font-size: 18px; padding: 10px;")
            button.clicked.connect(self.on_button_click)
            
            row = i // 4
            col = i % 4
            buttons_layout.addWidget(button, row, col)
            
            # Make '=' button span 2 rows
            if text == '=':
                buttons_layout.addWidget(button, row, col, 2, 1)
                
            # Make '0' button span 2 columns
            if text == '0':
                buttons_layout.addWidget(button, row, col, 1, 2)
                # Skip next column since we're spanning
                i += 1
        
        self.layout.addLayout(buttons_layout)
    
    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        
        if text.isdigit():
            self.current_input += text
            self.display.setText(self.current_input)
        elif text == 'C':
            self.current_input = ""
            self.previous_input = ""
            self.operation = None
            self.display.clear()
        elif text in '+-*/':
            if self.current_input:
                self.previous_input = self.current_input
                self.current_input = ""
                self.operation = text
        elif text == '=':
            if self.previous_input and self.current_input and self.operation:
                try:
                    result = self.calculate(
                        float(self.previous_input),
                        float(self.current_input),
                        self.operation
                    )
                    self.display.setText(str(result))
                    self.current_input = str(result)
                    self.previous_input = ""
                    self.operation = None
                except ZeroDivisionError:
                    self.display.setText("Error")
                    self.current_input = ""
                    self.previous_input = ""
                    self.operation = None
    
    def calculate(self, num1, num2, operation):
        if operation == '+':
            return num1 + num2
        elif operation == '-':
            return num1 - num2
        elif operation == '*':
            return num1 * num2
        elif operation == '/':
            return num1 / num2

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec_())