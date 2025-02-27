import pyautogui
import keyboard
import time
import customtkinter as ctk

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
        (section_width // 2, 3 * section_height // 2),
        (3 * section_width // 2, 3 * section_height // 2),
        (5 * section_width // 2, section_height // 2),
        (7 * section_width // 2, section_height // 2),
        (5 * section_width // 2, 3 * section_height // 2),
        (7 * section_width // 2, 3 * section_height // 2)
    ]

    if 1 <= section_number <= 8:
        pos = positions[section_number - 1]
        pyautogui.moveTo(pos[0], pos[1])
        pyautogui.click()

def main():
    custom_hotkeys = {i: str(i) for i in range(1, 9)}

    def open_hotkey_modal(section_number):
        modal = ctk.CTkToplevel(app)
        modal.title(f"Set Hotkey for Section {section_number}")
        modal.geometry("300x150")

        label = ctk.CTkLabel(modal, text=f"Enter hotkey for Section {section_number}:")
        label.pack(pady=10)

        entry = ctk.CTkEntry(modal, width=100)
        entry.pack(pady=10)
        entry.insert(0, custom_hotkeys[section_number])

        def set_hotkey():
            custom_key = entry.get()
            if custom_key:
                custom_hotkeys[section_number] = custom_key
                print(f"Custom hotkey for Section {section_number} set to 'ctrl+{custom_key}'.")
            modal.destroy()

        set_button = ctk.CTkButton(modal, text="Set", command=set_hotkey)
        set_button.pack(pady=10)

    def toggle_group_1():
        if toggle_var_1.get():
            for i in [1, 2, 3, 4]:
                keyboard.add_hotkey(f"alt+{custom_hotkeys[i]}", lambda i=i: move_to_section(i))
            print("Group 1 enabled.")
        else:
            for i in [1, 2, 3, 4]:
                keyboard.remove_hotkey(f"alt+{custom_hotkeys[i]}")
            print("Group 1 disabled.")
        update_all_groups_toggle()

    def toggle_group_2():
        if toggle_var_2.get():
            for i in [5, 6, 7, 8]:
                keyboard.add_hotkey(f"ctrl+{custom_hotkeys[i]}", lambda i=i: move_to_section(i))
            print("Group 2 enabled.")
        else:
            for i in [5, 6, 7, 8]:
                keyboard.remove_hotkey(f"ctrl+{custom_hotkeys[i]}")
            print("Group 2 disabled.")
        update_all_groups_toggle()

    def toggle_all_groups():
        if toggle_var_all.get():
            if not toggle_var_1.get():
                toggle_var_1.set(True)
                toggle_group_1()
            if not toggle_var_2.get():
                toggle_var_2.set(True)
                toggle_group_2()
            print("All enabled.")
        else:
            if toggle_var_1.get():
                toggle_var_1.set(False)
                toggle_group_1()
            if toggle_var_2.get():
                toggle_var_2.set(False)
                toggle_group_2()
            print("All disabled.")

    def update_all_groups_toggle():
        if toggle_var_1.get() and toggle_var_2.get():
            toggle_var_all.set(True)
        else:
            toggle_var_all.set(False)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.title("Screen Section Mover")
    app.geometry("550x350")

    toggle_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="gray25")
    toggle_frame.pack(pady=10, padx=10, fill="x")

    toggle_var_all = ctk.BooleanVar(value=False)
    toggle_button_all = ctk.CTkSwitch(toggle_frame, text="All", variable=toggle_var_all, command=toggle_all_groups, fg_color="gray40", text_color="white")
    toggle_button_all.grid(row=0, column=1, pady=10, padx=10, sticky="ew")

    toggle_frame.grid_columnconfigure(0, weight=1)
    toggle_frame.grid_columnconfigure(2, weight=1)

    main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="gray30")
    main_frame.pack(pady=10, padx=10, fill="both", expand=True)

    group_1_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="gray35")
    group_1_frame.pack(side="left", padx=10, pady=10, fill="both", expand=True)

    group_2_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color="gray35")
    group_2_frame.pack(side="right", padx=10, pady=10, fill="both", expand=True)

    toggle_var_1 = ctk.BooleanVar(value=False)
    toggle_button_1 = ctk.CTkSwitch(group_1_frame, text="Group 1", variable=toggle_var_1, command=toggle_group_1, fg_color="gray40", text_color="white")
    toggle_button_1.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    group_1_positions = [(1, 0), (1, 1), (2, 0), (2, 1)]
    for i, (row, col) in zip([1, 2, 3, 4], group_1_positions):
        label_text = f"Section {i}"
        label = ctk.CTkLabel(group_1_frame, text=label_text, width=100, height=50, corner_radius=8, fg_color="gray20", text_color="white", font=("Arial", 16))
        label.grid(row=row, column=col, padx=10, pady=10)

        label.bind("<Button-1>", lambda e, i=i: open_hotkey_modal(i))

    toggle_var_2 = ctk.BooleanVar(value=False)
    toggle_button_2 = ctk.CTkSwitch(group_2_frame, text="Group 2", variable=toggle_var_2, command=toggle_group_2, fg_color="gray40", text_color="white")
    toggle_button_2.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")

    group_2_positions = [(1, 0), (1, 1), (2, 0), (2, 1)]
    for i, (row, col) in zip([5, 6, 7, 8], group_2_positions):
        label_text = f"Section {i}"
        label = ctk.CTkLabel(group_2_frame, text=label_text, width=100, height=50, corner_radius=8, fg_color="gray20", text_color="white", font=("Arial", 16))
        label.grid(row=row, column=col, padx=10, pady=10)

        label.bind("<Button-1>", lambda e, i=i: open_hotkey_modal(i))

    app.mainloop()

    keyboard.wait('esc')

if __name__ == "__main__":
    main()