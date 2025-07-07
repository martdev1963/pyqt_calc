import sys
import math
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLineEdit, 
                            QPushButton, QWidget, QGridLayout, QHBoxLayout, 
                            QTabWidget, QDockWidget, QListWidget, QMenuBar, QAction)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QKeyEvent

"""
-----------------------------------------------------------------------------------------------------------------------
Enhancing Your PyQt5 Calculator with Advanced Features

Let's extend your calculator with memory functions, keyboard support, 
and scientific operations. Here's a comprehensive upgrade to your existing code:
https://chat.deepseek.com/a/chat/s/97d613c1-7b19-42b1-925c-f02e994a830a
-----------------------------------------------------------------------------------------------------------------------
"""

# 1. Memory Functions Implementation
class CalculatorApp(QMainWindow):
    def __init__(self):
        # ... existing init code ...
        self.memory = 0
        self.create_memory_buttons()
     
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
            btn.setStyleSheet("font-size: 14px; padding: 5px;")
            btn.clicked.connect(slot)
            memory_layout.addWidget(btn)
        
        self.layout.insertLayout(1, memory_layout)  # Insert below display
    
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



