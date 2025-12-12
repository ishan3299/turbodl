import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from PyQt6.QtWidgets import QApplication
from turbodl.core.engine import DownloadEngine
from turbodl.ui.main_window import MainWindow
from turbodl.ui.tray import TrayManager
from turbodl.ui.add_dialog import AddDialog
from turbodl.ui.settings import SettingsDialog
from turbodl.utils.logger import logger

def main():
    logger.info("Starting TurboDL...")
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False) # Important for tray support
    
    # Initialize Engine
    engine = DownloadEngine()
    if not engine.start_daemon():
        logger.error("Could not start download engine.")
        sys.exit(1)
        
    # Initialize UI
    window = MainWindow(engine)
    tray = TrayManager(app, window)
    
    # Connect Add Button
    def show_add_dialog():
        dialog = AddDialog(window)
        if dialog.exec():
            data = dialog.get_data()
            if data['url']:
                # Run add_download in a separate thread to prevent UI freezing
                from threading import Thread
                
                def add_task(url, options):
                    logger.info(f"Starting background task for {url}")
                    engine.add_download(url) 
                
                # Note: For a production app, we should pass 'data' completely and handle callbacks
                # but for now, firing and forgetting is better than freezing.
                t = Thread(target=add_task, args=(data['url'], None))
                t.daemon = True
                t.start()
                
    window.btn_add.clicked.connect(show_add_dialog)
    
     # Connect Settings Button
    def show_settings_dialog():
        dialog = SettingsDialog(window)
        dialog.exec()
        
    window.btn_settings.clicked.connect(show_settings_dialog)
    
    tray.show()
    window.show()
    
    logger.info("Application initialized.")
    
    exit_code = app.exec()
    
    logger.info("Shutting down...")
    engine.stop_daemon()
    sys.exit(exit_code)

if __name__ == "__main__":
    main()
