# ScreenNavigator

ScreenNavigator is a powerful desktop utility that allows you to define and navigate between specific sections of your screen or multiple monitors with keyboard shortcuts.

## Features

- Create up to 8 groups with 8 sections each
- Define custom screen areas by clicking and dragging
- Navigate between defined screen sections with customizable keyboard shortcuts
- Works with multiple monitors
- System tray integration for easy access
- Customizable group and section names
- Modern dark-themed UI built with CustomTkinter

## Installation

### Prerequisites

- Python 3.7+
- Required packages:
  - keyboard
  - customtkinter
  - screeninfo
  - pystray
  - Pillow

### Setup

1. Clone the repository:
   ```
   git clone https://github.com/BJ-dev0706/ScreenNavigator.git
   cd ScreenNavigator
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python index.py
   ```

## Usage

### Defining Screen Sections

1. Right-click on any section to define its area
2. Click and drag to select the desired screen area
3. Release to save the selection

### Navigating Between Sections

- Use the default keyboard shortcuts (Ctrl+Shift+1, Ctrl+Shift+2, etc.) to activate a group
- Customize shortcuts in Settings → Edit Shortcuts

### Customizing Groups and Sections

- Left-click on a section to rename it
- Right-click on a group header to rename the group
- Use the "Add Group" button to create new groups
- Use the "Add Section" button within a group to add new sections

## Keyboard Shortcuts

- **Ctrl+Shift+1** through **Ctrl+Shift+8**: Activate groups 1-8
- **Esc**: Exit application

## System Tray

The application minimizes to the system tray. You can:
- Left-click the tray icon to show/hide the main window
- Right-click for additional options (Show/Hide, Exit)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Screenshots

![Main Interface](screenshots/main_interface.png)
![Defining Sections](screenshots/defining_sections.png)