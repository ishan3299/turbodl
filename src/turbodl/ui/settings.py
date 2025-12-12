from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QDialogButtonBox, 
                             QTabWidget, QWidget, QFormLayout, QLineEdit, QCheckBox)

class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("TurboDL Settings")
        self.resize(500, 300)
        
        layout = QVBoxLayout(self)
        
        tabs = QTabWidget()
        layout.addWidget(tabs)
        
        # General Tab
        general_tab = QWidget()
        gen_layout = QFormLayout(general_tab)
        gen_layout.addRow("Default Download Directory:", QLineEdit("/home/ishan-patel/Downloads"))
        gen_layout.addRow("Max Concurrent Downloads:", QLineEdit("3"))
        tabs.addTab(general_tab, "General")
        
        # Connection Tab
        conn_tab = QWidget()
        conn_layout = QFormLayout(conn_tab)
        conn_layout.addRow("Default Max Connections:", QLineEdit("16"))
        conn_layout.addRow("Minimum Split Size (MB):", QLineEdit("4"))
        tabs.addTab(conn_tab, "Connection")
        
         # System Tab
        sys_tab = QWidget()
        sys_layout = QFormLayout(sys_tab)
        sys_layout.addRow(QCheckBox("Start with System"))
        sys_layout.addRow(QCheckBox("Minimize to Tray on Close"))
        tabs.addTab(sys_tab, "System")
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
