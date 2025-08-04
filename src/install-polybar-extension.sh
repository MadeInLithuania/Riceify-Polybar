#!/bin/bash

# Riceify Polybar Extension Installer
# This script installs the polybar extension for Riceify

echo "🍚 Installing Riceify Polybar Extension..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Make the polybar script executable
chmod +x "$SCRIPT_DIR/polybar-riceify.py"

echo "✅ Made polybar-riceify.py executable"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

# Test the script
echo "🧪 Testing the polybar extension..."
python3 "$SCRIPT_DIR/polybar-riceify.py" --status

if [ $? -eq 0 ]; then
    echo "✅ Polybar extension test successful"
else
    echo "❌ Polybar extension test failed"
    exit 1
fi

echo ""
echo "🎉 Installation complete!"
echo ""
echo "📋 To use the polybar extension:"
echo "1. Copy the riceify module configuration from polybar-config-example.ini"
echo "2. Add it to your polybar config file (~/.config/polybar/config.ini)"
echo "3. Restart polybar"
echo ""
echo "🔧 Available commands:"
echo "  python3 $SCRIPT_DIR/polybar-riceify.py --status    # Show current rice status"
echo "  python3 $SCRIPT_DIR/polybar-riceify.py --menu      # Show rice menu"
echo "  python3 $SCRIPT_DIR/polybar-riceify.py --list      # List all rices"
echo "  python3 $SCRIPT_DIR/polybar-riceify.py --add <name> # Add new rice"
echo "  python3 $SCRIPT_DIR/polybar-riceify.py --switch <name> # Switch to rice"
echo "  python3 $SCRIPT_DIR/polybar-riceify.py --remove <name> # Remove rice"
echo "  python3 $SCRIPT_DIR/polybar-riceify.py --info <name> # Get rice info"
echo ""
echo "💡 Tip: You can bind keyboard shortcuts to these commands for quick access!" 