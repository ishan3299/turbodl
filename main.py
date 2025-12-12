import sys
import os

# Add src to path so we can import the package without installing it
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
# Add bundled libs
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))

from turbodl.main import main

if __name__ == "__main__":
    main()
