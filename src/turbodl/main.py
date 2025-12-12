import sys
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
    app.setApplicationName("TurboDL")
    app.setDesktopFileName("turbodl")
    app.setQuitOnLastWindowClosed(False) # Important for tray support
    
    # Set Window Icon
    import os
    icon_path = os.path.join(os.path.dirname(__file__), "resources", "icon.png")
    from PyQt6.QtGui import QIcon
    app.setWindowIcon(QIcon(icon_path))
    
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
    
    # Run Event Loop
    try:
        exit_code = app.exec()
    except KeyboardInterrupt:
        logger.info("KeyboardInterrupt received from console. Quitting...")
        app.quit()
        exit_code = 0
    except Exception as e:
        logger.error(f"Critical error: {e}")
        exit_code = 1
    finally:
        logger.info("Cleaning up resources...")
        
        # Stop UI updates first
        if window:
            try:
                window.cleanup()
            except:
                pass
        
        # Hide Tray
        if tray:
            try:
                tray.cleanup()
            except:
                pass
        
        # Stop Backend
        if engine:
            try:
                engine.stop_daemon()
            except:
                pass
        
        logger.info("Shutdown complete.")

    sys.exit(exit_code)

if __name__ == "__main__":
    main()
