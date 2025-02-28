import pyautogui

def move_to_section(section_number, positions):
    pos = positions[section_number - 1]
    print(f"Moving to section {section_number} at position {pos}")
    if pos != (0, 0):
        pyautogui.moveTo(pos[0], pos[1])
        pyautogui.click()

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")
