#!/bin/bash
set -e

# Resolve the directory where the script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# Move to the project root (assuming script is in packaging/)
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

APP_NAME="turbodl"
VERSION="1.0.3"
BUILD_DIR="build/deb"
DEB_DIR="${BUILD_DIR}/${APP_NAME}_${VERSION}_all"

# Clean
rm -rf build
mkdir -p "${DEB_DIR}/usr/bin"
mkdir -p "${DEB_DIR}/usr/lib/${APP_NAME}"
mkdir -p "${DEB_DIR}/usr/share/applications"
mkdir -p "${DEB_DIR}/usr/share/icons/hicolor/scalable/apps"
mkdir -p "${DEB_DIR}/DEBIAN"

# Copy Source
cp -r src/* "${DEB_DIR}/usr/lib/${APP_NAME}/"
cp main.py "${DEB_DIR}/usr/lib/${APP_NAME}/"
cp requirements.txt "${DEB_DIR}/usr/lib/${APP_NAME}/"

# Copy Control
cp packaging/control "${DEB_DIR}/DEBIAN/"

# Copy Desktop Entry
cp packaging/turbodl.desktop "${DEB_DIR}/usr/share/applications/"

# Create wrapper script
cat > "${DEB_DIR}/usr/bin/${APP_NAME}" <<EOF
#!/bin/bash
export PYTHONPATH="/usr/lib/${APP_NAME}/src"
exec python3 /usr/lib/${APP_NAME}/main.py "\$@"
EOF

chmod +x "${DEB_DIR}/usr/bin/${APP_NAME}"

# Build
dpkg-deb --build "${DEB_DIR}"

echo "Built ${DEB_DIR}.deb"
