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
        
        # Initialize calculator state
        self.current_input = ""
        self.previous_input = ""
        self.operation = None
        self.memory = 0
        self.history = []
        
        # Set up main window
        self.setWindowTitle("Scientific Calculator")
        self.setFixedSize(600, 800)
        
        # Create central widget and main layout
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout()
        self.central_widget.setLayout(self.main_layout)
        
        # Create UI components
        self.create_display()
        self.create_memory_buttons()
        self.create_tab_system()
        self.create_menu()
        self.create_history_dock()

    def create_display(self):
        self.display = QLineEdit('0')
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("""
            font-size: 32px;
            padding: 15px;
            border: 2px solid #ccc;
            border-radius: 5px;
            margin-bottom: 10px;
        """)
        self.display.setMaxLength(15)
        self.main_layout.addWidget(self.display)

    def create_memory_buttons(self):
        memory_layout = QHBoxLayout()
        
        buttons = [
            ('MC', self.memory_clear),
            ('MR', self.memory_recall),
            ('M+', self.memory_add),
            ('M-', self.memory_subtract),
            ('MS', self.memory_store)
        ]
        
        for text, slot in buttons:
            btn = QPushButton(text)
            btn.setStyleSheet("""
                font-size: 14px;
                padding: 8px;
                margin: 2px;
            """)
            btn.clicked.connect(slot)
            memory_layout.addWidget(btn)
        
        self.main_layout.addLayout(memory_layout)

    # Memory functions
    def memory_clear(self):
        self.memory = 0
    
    def memory_recall(self):
        self.current_input = str(self.memory)
        self.display.setText(self.current_input)
    
    def memory_add(self):
        if self.current_input:
            self.memory += float(self.current_input)
    
    def memory_subtract(self):
        if self.current_input:
            self.memory -= float(self.current_input)
    
    def memory_store(self):
        if self.current_input:
            self.memory = float(self.current_input)

    def create_tab_system(self):
        self.tabs = QTabWidget()
        
        # Basic calculator tab
        basic_tab = QWidget()
        basic_layout = QVBoxLayout()
        basic_tab.setLayout(basic_layout)
        
        # Scientific calculator tab
        scientific_tab = QWidget()
        scientific_layout = QVBoxLayout()
        scientific_tab.setLayout(scientific_layout)
        
        # Add number pads to both tabs
        self.create_basic_number_pad(basic_layout)
        self.create_scientific_pad(scientific_layout)
        
        self.tabs.addTab(basic_tab, "Basic")
        self.tabs.addTab(scientific_tab, "Scientific")
        
        self.main_layout.addWidget(self.tabs)

    def create_basic_number_pad(self, layout):
        grid = QGridLayout()
        
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', 'C', '=', '+'
        ]
        
        for i, text in enumerate(buttons):
            btn = QPushButton(text)
            btn.setStyleSheet("""
                font-size: 24px;
                padding: 15px;
                margin: 3px;
                min-width: 60px;
            """)
            btn.clicked.connect(self.on_button_click)
            
            if text == '=':
                grid.addWidget(btn, i//4, i%4, 1, 1)
            elif text == '0':
                grid.addWidget(btn, i//4, i%4, 1, 2)
            else:
                grid.addWidget(btn, i//4, i%4)
        
        layout.addLayout(grid)

    def create_scientific_pad(self, layout):
        grid = QGridLayout()
        
        buttons = [
            ('√', self.square_root),
            ('x²', self.square),
            ('x^y', self.power),
            ('sin', self.sin_func),
            ('cos', self.cos_func),
            ('tan', self.tan_func),
            ('log', self.log_func),
            ('ln', self.ln_func),
            ('π', self.pi_func),
            ('e', self.e_func)
        ]
        
        for i, (text, slot) in enumerate(buttons):
            btn = QPushButton(text)
            btn.setStyleSheet("""
                font-size: 18px;
                padding: 12px;
                margin: 3px;
            """)
            btn.clicked.connect(slot)
            grid.addWidget(btn, i//3, i%3)
        
        layout.addLayout(grid)

    def on_button_click(self):
        sender = self.sender()
        text = sender.text()
        
        if text.isdigit() or text == '.':
            if self.current_input == '0' and text != '.':
                self.current_input = text
            else:
                self.current_input += text
            self.display.setText(self.current_input)
        elif text == 'C':
            self.current_input = "0"
            self.previous_input = ""
            self.operation = None
            self.display.setText(self.current_input)
        elif text in '+-*/^':
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
                    self.update_history(
                        f"{self.previous_input} {self.operation} {self.current_input}",
                        result
                    )
                    self.current_input = str(result)
                    self.previous_input = ""
                    self.operation = None
                except (ZeroDivisionError, ValueError):
                    self.display.setText("Error")
                    self.current_input = "0"
                    self.previous_input = ""
                    self.operation = None

    def calculate(self, num1, num2, operation):
        operations = {
            '+': lambda x, y: x + y,
            '-': lambda x, y: x - y,
            '*': lambda x, y: x * y,
            '/': lambda x, y: x / y if y != 0 else float('nan'),
            '^': lambda x, y: x ** y
        }
        return operations.get(operation, lambda x, y: 0)(num1, num2)

    # Scientific functions
    def square_root(self):
        if self.current_input:
            try:
                result = math.sqrt(float(self.current_input))
                self.display.setText(str(result))
                self.current_input = str(result)
            except ValueError:
                self.display.setText("Error")

    def square(self):
        if self.current_input:
            result = float(self.current_input) ** 2
            self.display.setText(str(result))
            self.current_input = str(result)

    def power(self):
        if self.current_input:
            self.previous_input = self.current_input
            self.current_input = ""
            self.operation = '^'

    def sin_func(self):
        if self.current_input:
            result = math.sin(math.radians(float(self.current_input)))
            self.display.setText(str(result))
            self.current_input = str(result)

    def cos_func(self):
        if self.current_input:
            result = math.cos(math.radians(float(self.current_input)))
            self.display.setText(str(result))
            self.current_input = str(result)

    def tan_func(self):
        if self.current_input:
            result = math.tan(math.radians(float(self.current_input)))
            self.display.setText(str(result))
            self.current_input = str(result)

    def log_func(self):
        if self.current_input:
            try:
                result = math.log10(float(self.current_input))
                self.display.setText(str(result))
                self.current_input = str(result)
            except ValueError:
                self.display.setText("Error")

    def ln_func(self):
        if self.current_input:
            try:
                result = math.log(float(self.current_input))
                self.display.setText(str(result))
                self.current_input = str(result)
            except ValueError:
                self.display.setText("Error")

    def pi_func(self):
        self.current_input = str(math.pi)
        self.display.setText(self.current_input)

    def e_func(self):
        self.current_input = str(math.e)
        self.display.setText(self.current_input)

    def create_menu(self):
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Edit menu
        edit_menu = menubar.addMenu('Edit')
        copy_action = QAction('Copy', self)
        copy_action.setShortcut('Ctrl+C')
        copy_action.triggered.connect(self.copy_to_clipboard)
        edit_menu.addAction(copy_action)
        
        paste_action = QAction('Paste', self)
        paste_action.setShortcut('Ctrl+V')
        paste_action.triggered.connect(self.paste_from_clipboard)
        edit_menu.addAction(paste_action)
        
        # Theme menu
        theme_menu = menubar.addMenu('Theme')
        light_action = QAction('Light', self)
        light_action.triggered.connect(lambda: self.set_theme('light'))
        theme_menu.addAction(light_action)
        
        dark_action = QAction('Dark', self)
        dark_action.triggered.connect(lambda: self.set_theme('dark'))
        theme_menu.addAction(dark_action)

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.display.text())

    def paste_from_clipboard(self):
        clipboard = QApplication.clipboard()
        text = clipboard.text()
        try:
            float(text)  # Validate it's a number
            self.current_input = text
            self.display.setText(text)
        except ValueError:
            pass

    def create_history_dock(self):
        self.history_dock = QDockWidget("History", self)
        self.history_list = QListWidget()
        self.history_dock.setWidget(self.history_list)
        self.addDockWidget(Qt.RightDockWidgetArea, self.history_dock)

    def update_history(self, expression, result):
        entry = f"{expression} = {result}"
        self.history.append(entry)
        self.history_list.addItem(entry)

    def set_theme(self, theme):
        if theme == 'light':
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #f0f0f0;
                    color: #000000;
                }
                QPushButton {
                    background-color: #e0e0e0;
                    border: 1px solid #c0c0c0;
                }
                QLineEdit {
                    background-color: #ffffff;
                    color: #000000;
                }
                QListWidget {
                    background-color: #ffffff;
                    color: #000000;
                }
            """)
        elif theme == 'dark':
            self.setStyleSheet("""
                QMainWindow, QWidget {
                    background-color: #303030;
                    color: #ffffff;
                }
                QPushButton {
                    background-color: #505050;
                    border: 1px solid #606060;
                    color: #ffffff;
                }
                QLineEdit {
                    background-color: #202020;
                    color: #ffffff;
                }
                QListWidget {
                    background-color: #202020;
                    color: #ffffff;
                }
            """)

    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        
        # Number keys
        if key in (Qt.Key_0, Qt.Key_1, Qt.Key_2, Qt.Key_3, Qt.Key_4,
                  Qt.Key_5, Qt.Key_6, Qt.Key_7, Qt.Key_8, Qt.Key_9):
            self.on_button_click_simulate(text)
        
        # Operation keys
        elif text in '+-*/':
            self.on_button_click_simulate(text)
        
        # Enter/Return key
        elif key in (Qt.Key_Enter, Qt.Key_Return):
            self.on_button_click_simulate('=')
        
        # Escape key (clear)
        elif key == Qt.Key_Escape:
            self.on_button_click_simulate('C')
        
        # Decimal point
        elif text == '.':
            self.on_button_click_simulate('.')
        
        # Memory functions
        elif key == Qt.Key_M:
            if event.modifiers() & Qt.ControlModifier:
                if event.modifiers() & Qt.ShiftModifier:
                    self.memory_clear()
                else:
                    self.memory_store()
        
        else:
            super().keyPressEvent(event)

    def on_button_click_simulate(self, text):
        for btn in self.findChildren(QPushButton):
            if btn.text() == text:
                btn.click()
                break

if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = CalculatorApp()
    calculator.show()
    sys.exit(app.exec_())