# TurboDL

TurboDL is an advanced, IDM-style download manager for Linux, designed for high performance and seamless integration with the Linux desktop environment.

## Features
- **Modern GUI**: Built with PyQt6 for a native look and feel.
- **Advanced Auto-Tuning**: Automatically upgrades download speeds by optimizing connections and segmentation.
- **System Tray Integration**: Run in the background without cluttering your workspace.
- **Multi-Protocol**: Powered by `aria2c` for robust support of HTTP, HTTPS, FTP, and BitTorrent.

## Installation

### Method 1: Installing the .deb (Recommended)
Download the latest release (`.deb` file) from the [Releases Page](https://github.com/ishan3299/turbodl/releases).
```bash
# Example for v1.0.5
sudo dpkg -i turbodl_1.0.5_all.deb
sudo apt-get install -f  # Fix dependencies if needed
```

### Running from Source
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python main.py
   ```

## Contributing
Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct, and the process for submitting pull requests to us.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
