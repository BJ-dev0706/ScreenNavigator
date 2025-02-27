import pyautogui
import keyboard
import time

def get_combined_screen_size():
    primary_screen = pyautogui.size()
    combined_width = primary_screen.width * 2
    combined_height = primary_screen.height
    return combined_width, combined_height

def move_to_section(section_number):
    screen_width, screen_height = get_combined_screen_size()
    section_width = screen_width // 4
    section_height = screen_height // 2

    positions = [
        (section_width // 2, section_height // 2),
        (3 * section_width // 2, section_height // 2),
        (5 * section_width // 2, section_height // 2),
        (7 * section_width // 2, section_height // 2),
      23  (section_width // 2, 3 * section_height // 2),
        (3 * section_width // 2, 3 * section_height // 2),
        (5 * section_width // 2, 3 * section_height // 2),
        (7 * section_width // 2, 3 * section_height // 2)
    ]

    if 1 <= section_number <= 8:
        pos = positions[section_number - 1]
        pyautogui.moveTo(pos[0], pos[1])
        pyautogui.click()

def main():
    print("Press keys 1-8 to move to the corresponding section of the screen.")
    for i in range(1, 9):
        keyboard.add_hotkey(str(i), lambda i=i: move_to_section(i))

    print("Press 'esc' to exit.")
    keyboard.wait('esc')

if __name__ == "__main__":
    main()