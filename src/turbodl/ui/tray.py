from PyQt6.QtWidgets import QSystemTrayIcon, QMenu
from PyQt6.QtGui import QIcon, QAction

class TrayManager:
    def __init__(self, app, main_window):
        self.app = app
        self.main_window = main_window
        self.tray_icon = QSystemTrayIcon(QIcon("resources/icon.png"), self.app) # Needs icon
        self.tray_icon.setToolTip("TurboDL")
        
        # Tray Menu
        self.menu = QMenu()
        
        self.action_show = QAction("Show/Hide Window")
        self.action_show.triggered.connect(self.toggle_window)
        self.menu.addAction(self.action_show)
        
        self.menu.addSeparator()
        
        self.action_add = QAction("Start New Download")
        self.action_add.triggered.connect(self.main_window.btn_add.click) # Trigger main window add
        self.menu.addAction(self.action_add)
        
        self.action_pause = QAction("Pause All")
        self.action_pause.triggered.connect(self.main_window.engine.pause_all)
        self.menu.addAction(self.action_pause)
        
        self.action_resume = QAction("Resume All")
        self.action_resume.triggered.connect(self.main_window.engine.resume_all)
        self.menu.addAction(self.action_resume)
        
        self.menu.addSeparator()
        
        self.action_quit = QAction("Quit Application")
        self.action_quit.triggered.connect(self.quit_app)
        self.menu.addAction(self.action_quit)
        
        self.tray_icon.setContextMenu(self.menu)
        self.tray_icon.activated.connect(self.on_activated)
        
        # Pass tray icon to main window so it can use it for notifications
        self.main_window.set_tray(self.tray_icon)

    def show(self):
        self.tray_icon.show()

    def toggle_window(self):
        if self.main_window.isVisible():
            self.main_window.hide()
        else:
            self.main_window.show()
            self.main_window.activateWindow()

    def on_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.toggle_window()

    def quit_app(self):
        self.app.quit()
