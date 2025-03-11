# ScreenNavigator

![ScreenNavigator](./assets/banner.png)

ScreenNavigator is a powerful desktop utility that allows you to define and navigate between specific sections of your screen or multiple monitors with keyboard shortcuts.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Defining Screen Sections](#defining-screen-sections)
  - [Navigating Between Sections](#navigating-between-sections)
  - [Customizing Groups and Sections](#customizing-groups-and-sections)
- [Keyboard Shortcuts](#keyboard-shortcuts)
- [System Tray](#system-tray)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

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
   ```bash
   git clone https://github.com/BJ-dev0706/ScreenNavigator.git
   cd ScreenNavigator
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the application:
   ```bash
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

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [kitchi734@gmail.com](mailto:kitchi734@gmail.com).