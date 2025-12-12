from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTableWidget, QTableWidgetItem, QHeaderView,
                             QLabel, QProgressBar, QSystemTrayIcon, QMenu, QApplication)
from PyQt6.QtCore import Qt, QTimer, pyqtSignal
from PyQt6.QtGui import QIcon, QAction

class MainWindow(QMainWindow):
    def __init__(self, engine):
        super().__init__()
        self.engine = engine
        self.setWindowTitle("TurboDL - Advanced Download Manager")
        self.resize(1000, 600)
        
        # Central Widget
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Toolbar
        toolbar_layout = QHBoxLayout()
        self.btn_add = QPushButton("Add URL")
        self.btn_pause = QPushButton("Pause All")
        self.btn_resume = QPushButton("Resume All")
        self.btn_settings = QPushButton("Settings")
        
        toolbar_layout.addWidget(self.btn_add)
        toolbar_layout.addWidget(self.btn_pause)
        toolbar_layout.addWidget(self.btn_resume)
        toolbar_layout.addStretch()
        toolbar_layout.addWidget(self.btn_settings)
        layout.addLayout(toolbar_layout)
        
        # Download Table
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["GID", "Name", "Status", "Size", "Speed", "Progress"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        layout.addWidget(self.table)
        
        # Status Bar
        self.status_label = QLabel("Ready")
        self.statusBar().addWidget(self.status_label)
        
        # Timer for updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_downloads)
        self.timer.start(1000)
        
        # Connect signals
        self.btn_pause.clicked.connect(self.engine.pause_all)
        self.btn_resume.clicked.connect(self.engine.resume_all)
        
    def update_downloads(self):
        downloads = self.engine.get_downloads()
        self.table.setRowCount(len(downloads))
        
        total_speed = 0
        
        for row, d in enumerate(downloads):
            # GID
            self.table.setItem(row, 0, QTableWidgetItem(d.gid))
            
            # Name (try to get filename)
            name = d.name if d.name else "Unknown"
            if not name and d.files:
                name = d.files[0].path
            self.table.setItem(row, 1, QTableWidgetItem(str(name)))
            
            # Status
            self.table.setItem(row, 2, QTableWidgetItem(d.status))
            
            # Size
            size_str = f"{d.completed_length_string()}/{d.total_length_string()}"
            self.table.setItem(row, 3, QTableWidgetItem(size_str))
            
            # Speed
            speed = d.download_speed
            total_speed += speed
            self.table.setItem(row, 4, QTableWidgetItem(d.download_speed_string()))
            
            # Progress
            progress = QProgressBar()
            try:
                p_val = int(d.progress)
            except:
                p_val = 0
            progress.setValue(p_val)
            self.table.setCellWidget(row, 5, progress)
            
        self.status_label.setText(f"Total Speed: {total_speed / 1024 / 1024:.2f} MB/s | Active Downloads: {len(downloads)}")

    def closeEvent(self, event):
        # Minimize to tray instead of closing
        if self.isVisible():
            event.ignore()
            self.hide()
            self.tray_icon.showMessage(
                "TurboDL",
                "Application minimized to tray.",
                QSystemTrayIcon.MessageIcon.Information,
                2000
            )

    def set_tray(self, tray_icon):
        self.tray_icon = tray_icon
