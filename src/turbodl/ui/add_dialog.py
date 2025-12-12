from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QLabel, QLineEdit, 
                             QDialogButtonBox, QCheckBox, QHBoxLayout, QSpinBox)

class AddDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Download")
        self.resize(400, 150)
        
        layout = QVBoxLayout(self)
        
        # URL Input
        layout.addWidget(QLabel("Download URL:"))
        self.url_input = QLineEdit()
        layout.addWidget(self.url_input)
        
        # Options
        fs_layout = QHBoxLayout()
        self.manual_override = QCheckBox("Manual Override Connections")
        self.manual_override.toggled.connect(self.toggle_override)
        fs_layout.addWidget(self.manual_override)
        
        self.conn_spin = QSpinBox()
        self.conn_spin.setRange(1, 16)
        self.conn_spin.setValue(8)
        self.conn_spin.setEnabled(False)
        fs_layout.addWidget(self.conn_spin)
        
        layout.addLayout(fs_layout)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)
        
    def toggle_override(self, checked):
        self.conn_spin.setEnabled(checked)
        
    def get_data(self):
        return {
            'url': self.url_input.text(),
            'manual': self.manual_override.isChecked(),
            'connections': self.conn_spin.value()
        }
