import pyautogui
import keyboard
import time
import customtkinter as ctk
import tkinter as tk
from screeninfo import get_monitors
import tkinter.messagebox as messagebox

def get_combined_screen_size():
    monitors = get_monitors()
    combined_width = sum(monitor.width for monitor in monitors)
    combined_height = max(monitor.height for monitor in monitors)
    print(combined_width, combined_height)
    return combined_width, combined_height

def move_to_section(section_number, positions):
    pos = positions[section_number - 1]
    print(f"Moving to section {section_number} at position {pos}")
    if pos != (0, 0):
        pyautogui.moveTo(pos[0], pos[1])
        pyautogui.click()

def main():
    max_groups = 8
    max_sections_per_group = 8
    section_positions = [(0, 0) for _ in range(max_groups * max_sections_per_group)]
    group_names = {i: f"Group {i}" for i in range(1, 5)}
    section_names = {i: {j: f"Section {j}" for j in range(1, 5)} for i in range(1, 5)}
    group_count = 4
    group_section_counts = {i: 4 for i in range(1, 5)}

    toggle_vars = []
    toggle_buttons = []
    labels = []
    add_section_buttons = []

    def add_group():
        nonlocal group_count
        if group_count >= max_groups:
            print("Maximum number of groups reached.")
            show_warning("Maximum number of groups reached.")
            return

        group_count += 1
        group_names[group_count] = f"Group {group_count}"
        group_section_counts[group_count] = 0
        section_names[group_count] = {}

        group_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=group_frame_color, width=250)
        group_frame.grid(row=(group_count - 1) // 4, column=(group_count - 1) % 4, rowspan=1, columnspan=1, padx=10, pady=10, sticky="nsew")

        toggle_button = ctk.CTkButton(
            group_frame, 
            text=group_names[group_count],
            command=lambda g=group_count: toggle_group(g),
            fg_color="gray50",
            text_color="white",
            height=32
        )
        toggle_button.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        toggle_vars.append(None)  # Keep the list for compatibility
        toggle_buttons.append(toggle_button)

        add_section_button = ctk.CTkButton(group_frame, text="Add Section", command=lambda g=group_count: add_section(g))
        add_section_buttons.append(add_section_button)
        
        for _ in range(4):
            add_section(group_count)

        button_row = (group_section_counts[group_count] + 1) // 2 + 2
        add_section_button.grid(row=button_row, column=0, columnspan=2, pady=5)

        update_ui()
        print(f"Added {group_names[group_count]} with 4 sections initially")

    def add_section(group_number):
        if group_section_counts[group_number] >= max_sections_per_group:
            print(f"Group {group_number} already has the maximum number of sections.")
            show_warning(f"Group {group_number} already has the maximum number of sections.")
            return

        group_section_counts[group_number] += 1
        section_index = group_section_counts[group_number]
        section_names[group_number][section_index] = f"Section {section_index}"
        
        row = (section_index - 1) // 2 + 1
        col = (section_index - 1) % 2

        group_frame = toggle_buttons[group_number - 1].master

        label_text = section_names[group_number][section_index]
        label = ctk.CTkLabel(
            group_frame, text=label_text, width=100, height=50, corner_radius=8,
            fg_color="gray30", text_color="black", font=("Arial", 16)
        )
        label.grid(row=row, column=col, padx=10, pady=10)
        labels.append(label)

        label.bind("<Button-3>", lambda e, g=group_number, i=section_index: define_section(g, i))
        label.bind("<Button-1>", lambda e, i=section_index: open_rename_modal("Section", i))
        label.bind("<Button-1>", lambda e, g=group_number: disable_group_toggle(g))

        if group_number <= len(add_section_buttons):
            add_section_button = add_section_buttons[group_number - 1]
            button_row = (group_section_counts[group_number] + 1) // 2 + 2
            add_section_button.grid(row=button_row, column=0, columnspan=2, pady=5)

        update_ui()
        print(f"Added {section_names[group_number][section_index]} to Group {group_number}")

    def open_rename_modal(item_type, item_number):
        modal = ctk.CTkToplevel(app)
        modal.title(f"Rename {item_type} {item_number}")
        modal.geometry("300x150")

        label = ctk.CTkLabel(modal, text=f"Enter new name for {item_type} {item_number}:")
        label.pack(pady=10)

        entry = ctk.CTkEntry(modal, width=100)
        entry.pack(pady=10)
        if item_type == "Group":
            entry.insert(0, group_names[item_number])
        else:
            entry.insert(0, section_names[item_number][item_number])

        def set_name():
            new_name = entry.get()
            if new_name:
                if item_type == "Group":
                    group_names[item_number] = new_name
                    update_ui()
                elif item_type == "Section":
                    section_names[item_number][item_number] = new_name
                    update_ui()
            modal.destroy()

        set_button = ctk.CTkButton(modal, text="Set", command=set_name)
        set_button.pack(pady=10)

    def define_section(group_number, section_number):
        monitors = get_monitors()
        combined_width = sum(monitor.width for monitor in monitors)
        combined_height = max(monitor.height for monitor in monitors)

        root = tk.Tk()
        # Position window at the absolute (0,0) coordinate of the entire display setup
        root.geometry(f"{combined_width}x{combined_height}-0+0")
        
        # Remove window decorations and make it stay on top
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        root.attributes('-alpha', 0.3)
        
        # Ensure window spans all displays by setting it at the leftmost position
        min_x = min(monitor.x for monitor in monitors)
        min_y = min(monitor.y for monitor in monitors)
        root.geometry(f"+{min_x}+{min_y}")

        # Create a canvas that spans all monitors
        canvas = tk.Canvas(root, cursor="cross", width=combined_width, height=combined_height, 
                          highlightthickness=0)
        canvas.configure(bg='black')
        canvas.pack(fill="both", expand=True)

        # Store coordinates for drawing
        start_x = start_y = 0
        rect_id = None

        def on_click(event):
            nonlocal start_x, start_y
            # Get absolute coordinates relative to the entire display setup
            start_x = root.winfo_pointerx() - root.winfo_rootx()
            start_y = root.winfo_pointery() - root.winfo_rooty()

        def on_drag(event):
            nonlocal rect_id
            if rect_id:
                canvas.delete(rect_id)
            
            # Get current pointer position relative to the entire display setup
            current_x = root.winfo_pointerx() - root.winfo_rootx()
            current_y = root.winfo_pointery() - root.winfo_rooty()
            
            # Draw rectangle using screen coordinates
            rect_id = canvas.create_rectangle(
                start_x, start_y, 
                current_x, current_y, 
                outline='red', width=2
            )

        def on_release(event):
            # Get final position relative to the entire display setup
            end_x = root.winfo_pointerx() - root.winfo_rootx()
            end_y = root.winfo_pointery() - root.winfo_rooty()
            
            # Calculate center point using absolute coordinates
            center_x = (start_x + end_x) // 2
            center_y = (start_y + end_y) // 2
            
            index = (group_number - 1) * max_sections_per_group + (section_number - 1)
            section_positions[index] = (center_x, center_y)
            print(f"Section {section_number} in Group {group_number} defined at {section_positions[index]} (across all displays)")
            root.destroy()

        # Add escape key binding to close the window
        root.bind("<Escape>", lambda e: root.destroy())
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

        root.mainloop()

    def toggle_group(group_number):
        button = toggle_buttons[group_number - 1]
        is_active = button.cget("fg_color") == "green"
        
        if not is_active:
            button.configure(fg_color="green", text=f"{group_names[group_number]} (Active)")
            start_index = (group_number - 1) * max_sections_per_group
            end_index = start_index + group_section_counts[group_number]
            
            for i in range(start_index, end_index):
                move_to_section(i + 1, section_positions)
                time.sleep(0.3)
            print(f"Group {group_number} enabled.")
        else:
            button.configure(fg_color="gray50", text=group_names[group_number])
            print(f"Group {group_number} disabled.")

    def update_ui():
        for group_number in range(1, group_count + 1):
            button = toggle_buttons[group_number - 1]
            current_text = button.cget("text")
            is_active = "(Active)" in current_text
            new_text = f"{group_names[group_number]}{' (Active)' if is_active else ''}"
            button.configure(text=new_text)
            for i in range(1, group_section_counts[group_number] + 1):
                if i in section_names[group_number]:
                    labels[(group_number - 1) * 4 + i - 1].configure(text=section_names[group_number][i])

    def disable_group_toggle(group_number):
        button = toggle_buttons[group_number - 1]
        if button.cget("fg_color") == "green":
            toggle_group(group_number)

    def show_warning(message):
        messagebox.showinfo("Warning", message)

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.title("Screen Section Mover")
    app.geometry("1080x600")

    main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="gray30")
    main_frame.pack(pady=10, padx=10, fill="both", expand=True)

    main_frame.grid_rowconfigure(0, weight=1)
    main_frame.grid_rowconfigure(1, weight=1)
    main_frame.grid_rowconfigure(2, weight=1)
    main_frame.grid_rowconfigure(3, weight=1)
    main_frame.grid_columnconfigure(0, weight=1)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_columnconfigure(2, weight=1)
    main_frame.grid_columnconfigure(3, weight=1)

    group_layouts = [[(0, 0), (0, 1), (1, 0), (1, 1)]] * 4

    group_frame_color = "#B0B0B0"

    for group_number in range(1, 5):
        group_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=group_frame_color, width=250)
        group_frame.grid(row=(group_number - 1) // 4, column=(group_number - 1) % 4, rowspan=1, columnspan=1, padx=10, pady=10, sticky="nsew")

        toggle_button = ctk.CTkButton(
            group_frame, 
            text=group_names[group_number],
            command=lambda g=group_number: toggle_group(g),
            fg_color="gray50",
            text_color="white",
            height=32
        )
        toggle_button.grid(row=0, column=0, columnspan=2, pady=10, padx=10, sticky="ew")
        toggle_vars.append(None)  # Keep the list for compatibility
        toggle_buttons.append(toggle_button)

        layout = group_layouts[group_number - 1]

        for i, (row, col) in enumerate(layout):
            section_index = i + 1
            label_text = section_names[group_number][section_index]
            label = ctk.CTkLabel(
                group_frame, text=label_text, width=100, height=50, corner_radius=8,
                fg_color="gray30", text_color="black", font=("Arial", 16)
            )
            label.grid(row=row + 1, column=col, padx=10, pady=10)
            labels.append(label)

            label.bind("<Button-3>", lambda e, g=group_number, i=section_index: define_section(g, i))
            label.bind("<Button-1>", lambda e, i=section_index: open_rename_modal("Section", i))
            label.bind("<Button-1>", lambda e, g=group_number: disable_group_toggle(g))

        add_section_button = ctk.CTkButton(group_frame, text="Add Section", command=lambda g=group_number: add_section(g))
        add_section_button.grid(row=len(layout) + 1, column=0, columnspan=2, pady=5)
        add_section_button._name = f"!ctkbutton{group_number}"

    for i, toggle_button in enumerate(toggle_buttons, start=1):
        toggle_button.bind("<Button-3>", lambda e, i=i: open_rename_modal("Group", i))

    add_group_button = ctk.CTkButton(app, text="Add Group", command=add_group)
    add_group_button.pack(pady=5)

    app.mainloop()

    keyboard.wait('esc')

if __name__ == "__main__":
    main()