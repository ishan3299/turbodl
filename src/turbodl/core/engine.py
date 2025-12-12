import subprocess
import time
import aria2p
from turbodl.utils.logger import logger
from turbodl.core.tuner import AutoTuner

class DownloadEngine:
    def __init__(self, rpc_port=6800, rpc_secret="turbodl_secret"):
        self.rpc_port = rpc_port
        self.rpc_secret = rpc_secret
        self.aria2_process = None
        self.aria2 = None
        self.tuner = AutoTuner()

    def start_daemon(self):
        """Starts the aria2c daemon process safely."""
        cmd = [
            "aria2c",
            "--enable-rpc",
            "--rpc-listen-all=false",  # Bind to localhost only (secure)
            f"--rpc-listen-port={self.rpc_port}",
            f"--rpc-secret={self.rpc_secret}",
            "--max-connection-per-server=16",
            "--min-split-size=1M",
            "--daemon=false" # Run in foreground so we can kill it easily
        ]
        
        logger.info(f"Starting aria2c daemon: {' '.join(cmd)}")
        try:
            self.aria2_process = subprocess.Popen(
                cmd, 
                stdout=subprocess.PIPE, 
                stderr=subprocess.PIPE
            )
            # Give it a moment to start
            time.sleep(1) 
            
            # Connect aria2p client
            self.aria2 = aria2p.API(
                aria2p.Client(
                    host="http://localhost",
                    port=self.rpc_port,
                    secret=self.rpc_secret
                )
            )
            logger.info("Connected to aria2c RPC successfully.")
            return True
        except Exception as e:
            logger.error(f"Failed to start aria2c: {e}")
            return False

    def stop_daemon(self):
        if self.aria2_process:
            logger.info("Stopping aria2c daemon...")
            self.aria2_process.terminate()
            self.aria2_process.wait()
            self.aria2_process = None

    def add_download(self, url, save_dir=None):
        """
        Adds a download with auto-tuned options.
        """
        # Auto-tune
        tuning_options = self.tuner.analyze_url(url)
        
        options = {
            "max-connection-per-server": str(tuning_options['connections']),
            "split": str(tuning_options['split']),
            "min-split-size": str(tuning_options['min_split_size']),
        }
        
        if save_dir:
            options["dir"] = save_dir

        logger.info(f"Adding download {url} with options: {options}")
        
        try:
            download = self.aria2.add(url, options=options)
            return download
        except Exception as e:
            logger.error(f"Failed to add download: {e}")
            return None

    def get_downloads(self):
        if not self.aria2: return []
        try:
            return self.aria2.get_downloads()
        except:
            return []

    def pause_all(self):
        if self.aria2:
            self.aria2.pause_all()

    def resume_all(self):
        if self.aria2:
            self.aria2.unpause_all()

    def purge_completed(self):
        if self.aria2:
            self.aria2.purge()
