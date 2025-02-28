import pyautogui
import time
try:
    import win32api
    import win32con
    USE_WIN32 = True
except ImportError:
    USE_WIN32 = False

pyautogui.MINIMUM_DURATION = 0
pyautogui.PAUSE = 0

def move_to_section(section_number, positions):
    pos = positions[section_number - 1]
    print(f"Moving to section {section_number} at position {pos}")
    if pos != (0, 0):
        start_time = time.perf_counter()
        if USE_WIN32:
            win32api.SetCursorPos((int(pos[0]), int(pos[1])))
            win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)
        else:
            pyautogui.moveTo(pos[0], pos[1], duration=0)
            pyautogui.click()
        elapsed = time.perf_counter() - start_time
        print(f"Movement took {elapsed:.6f} seconds")

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")
