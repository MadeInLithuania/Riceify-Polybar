# Riceify Polybar Extension

A polybar module for managing and displaying rice configurations directly from your status bar.

## Features

- 🍚 Display current rice status in polybar
- ⚡ Quick rice switching with click actions
- 📋 List all available rices
- ➕ Add new rices from the status bar
- 🗑️ Remove rices with confirmation
- ℹ️ Get detailed rice information
- 🎨 Rofi integration for better UX

## Installation

1. **Make the installation script executable and run it:**
   ```bash
   chmod +x install-polybar-extension.sh
   ./install-polybar-extension.sh
   ```

2. **Add the riceify module to your polybar config:**
   
   Copy the `[module/riceify]` section from `polybar-config-example.ini` to your polybar config file (usually `~/.config/polybar/config.ini`).

3. **Add the module to your bar:**
   
   Add `riceify` to the `modules-left` or `modules-right` line in your bar configuration.

4. **Restart polybar:**
   ```bash
   polybar-msg cmd restart
   ```

## Configuration

### Basic Module Configuration

```ini
[module/riceify]
type = custom/script
exec = python3 ~/Riceify/polybar-riceify.py --status
click-left = python3 ~/Riceify/polybar-riceify.py --menu
click-right = rofi -show riceify -modi riceify:python3 ~/Riceify/polybar-riceify.py --menu
format-padding = 1
format-foreground = #f0c674
format-background = #282a2e
```

### Advanced Configuration with Menu

```ini
[module/riceify-menu]
type = custom/menu
format-spacing = 1
label-open = 🍚
label-open-foreground = #f0c674
label-close = ✕
label-close-foreground = #cc6666
label-separator = |
label-separator-foreground = #373b41

menu-0-0 = Add Rice
menu-0-0-exec = rofi -dmenu -p "Rice name:" | xargs -I {} python3 ~/Riceify/polybar-riceify.py --add {}
menu-0-1 = Switch Rice
menu-0-1-exec = python3 ~/Riceify/polybar-riceify.py --list | rofi -dmenu -p "Select rice:" | xargs -I {} python3 ~/Riceify/polybar-riceify.py --switch {}
menu-0-2 = Remove Rice
menu-0-2-exec = python3 ~/Riceify/polybar-riceify.py --list | rofi -dmenu -p "Remove rice:" | xargs -I {} python3 ~/Riceify/polybar-riceify.py --remove {}
menu-0-3 = List Rices
menu-0-3-exec = python3 ~/Riceify/polybar-riceify.py --list | rofi -dmenu -p "Rices:"
```

## Usage

### Command Line Interface

The polybar extension can be used directly from the command line:

```bash
# Show current rice status
python3 ~/Riceify/polybar-riceify.py --status

# Display rice menu
python3 ~/Riceify/polybar-riceify.py --menu

# List all rices
python3 ~/Riceify/polybar-riceify.py --list

# Add a new rice
python3 ~/Riceify/polybar-riceify.py --add "my-rice"

# Switch to a rice
python3 ~/Riceify/polybar-riceify.py --switch "my-rice"

# Remove a rice
python3 ~/Riceify/polybar-riceify.py --remove "my-rice"

# Get rice information
python3 ~/Riceify/polybar-riceify.py --info "my-rice"
```

### Polybar Integration

- **Left click**: Shows rice menu
- **Right click**: Opens rofi with rice options
- **Status display**: Shows current rice and total count

### Keyboard Shortcuts

You can bind keyboard shortcuts to rice operations using your window manager or desktop environment:

```bash
# Example i3wm bindings
bindsym $mod+r exec python3 ~/Riceify/polybar-riceify.py --menu
bindsym $mod+Shift+r exec rofi -dmenu -p "Rice name:" | xargs -I {} python3 ~/Riceify/polybar-riceify.py --add {}
```

## Rofi Integration

For better user experience, you can integrate with rofi:

1. **Add rofi modi** to your rofi config:
   ```bash
   rofi -show riceify -modi riceify:python3 ~/Riceify/polybar-riceify.py --menu
   ```

2. **Create a rofi theme** (optional):
   Copy the rofi theme section from `polybar-config-example.ini` to your rofi theme file.

## Troubleshooting

### Common Issues

1. **Script not found**: Make sure the path to `polybar-riceify.py` is correct in your polybar config.

2. **Permission denied**: Run the installation script to make the file executable:
   ```bash
   chmod +x ~/Riceify/polybar-riceify.py
   ```

3. **Python not found**: Ensure Python 3 is installed:
   ```bash
   python3 --version
   ```

4. **Rice directory not found**: The script will create the directory structure automatically when you add your first rice.

### Debug Mode

To debug issues, run the script with verbose output:
```bash
python3 ~/Riceify/polybar-riceify.py --status
```

## File Structure

```
Riceify/
├── polybar-riceify.py              # Main polybar extension script
├── polybar-config-example.ini      # Example polybar configuration
├── install-polybar-extension.sh    # Installation script
├── POLYBAR_README.md              # This file
└── Headers/
    └── Rice.h                     # Original Riceify C++ header
```

## Dependencies

- Python 3.6+
- polybar
- rofi (optional, for better UX)
- rsync (for rice operations)

## Contributing

Feel free to submit issues and enhancement requests!

## License

This extension follows the same license as the main Riceify project. 
