import pyautogui
import keyboard
import time
import customtkinter as ctk
import tkinter as tk
from screeninfo import get_monitors
import tkinter.messagebox as messagebox
import threading
import pystray
from PIL import Image
import sys
import os

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

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    
    window.geometry(f"{width}x{height}+{x}+{y}")

def main():
    max_groups = 8
    max_sections_per_group = 8
    section_positions = [(0, 0) for _ in range(max_groups * max_sections_per_group)]
    group_names = {i: f"Group {i}" for i in range(1, 5)}
    section_names = {i: {j: f"Section {j}" for j in range(1, 5)} for i in range(1, 5)}
    group_count = 4
    group_section_counts = {i: 4 for i in range(1, 5)}
    group_shortcuts = {i: f'ctrl+shift+{i}' for i in range(1, max_groups + 1)}

    toggle_buttons = []
    labels = []
    add_section_buttons = []
    
    try:
        monitors = get_monitors()
        if not monitors:
            print("No monitors detected. Using fallback values.")
            combined_width, combined_height = 1920, 1080
        else:
            combined_width = sum(monitor.width for monitor in monitors)
            combined_height = max(monitor.height for monitor in monitors)
    except Exception as e:
        print(f"Error detecting monitors: {e}. Using fallback values.")
        combined_width, combined_height = 1920, 1080
    
    def add_group():
        nonlocal group_count
        if group_count >= max_groups:
            print("Maximum number of groups reached.")
            show_warning("Maximum number of groups reached.")
            return

        group_count += 1
        
        columns = min(4, group_count)
        
        group_names[group_count] = f"Group {group_count}"
        group_section_counts[group_count] = 0
        section_names[group_count] = {}
        
        # Assign default shortcut for the new group
        group_shortcuts[group_count] = f'ctrl+shift+{group_count}'
        
        group_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=group_frame_color, width=200)
        group_frame.grid(row=(group_count - 1) // 4, column=(group_count - 1) % 4, rowspan=1, columnspan=1, padx=5, pady=5, sticky="nsew")

        group_frame.grid_columnconfigure(0, weight=1)
        group_frame.grid_columnconfigure(1, weight=1)

        button_frame = ctk.CTkFrame(group_frame, fg_color="transparent")
        button_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")
        
        button_frame.grid_columnconfigure(0, weight=2)
        button_frame.grid_columnconfigure(1, weight=1)

        toggle_button = ctk.CTkButton(
            button_frame, 
            text=group_names[group_count],
            command=lambda g=group_count: toggle_group(g),
            fg_color="gray50",
            text_color="white",
            height=28,
            width=140
        )
        toggle_button.grid(row=0, column=0, pady=5, padx=(10, 5), sticky="ew")
        toggle_buttons.append(toggle_button)

        try:
            reset_icon = ctk.CTkImage(
                light_image=Image.open("assets/reset_icon.png"),
                dark_image=Image.open("assets/reset_icon.png"),
                size=(20, 20)
            )
            delete_icon = ctk.CTkImage(
                light_image=Image.open("assets/delete_icon.png"),
                dark_image=Image.open("assets/delete_icon.png"),
                size=(20, 20)
            )
        except Exception as e:
            print(f"Failed to load icons: {e}")
            reset_icon = None
            delete_icon = None

        button_actions_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_actions_frame.grid(row=0, column=1, pady=5, padx=(0, 10))

        reset_button = ctk.CTkButton(
            button_actions_frame,
            text="",
            image=reset_icon if reset_icon else None,
            command=lambda g=group_count: reset_group_positions(g),
            fg_color="transparent",
            text_color="white",
            height=32,
            width=32,
            corner_radius=8
        )
        reset_button.grid(row=0, column=0, padx=2)

        delete_button = ctk.CTkButton(
            button_actions_frame,
            text="",
            image=delete_icon if delete_icon else None,
            command=lambda g=group_count: delete_group(g),
            fg_color="transparent",
            text_color="white",
            height=32,
            width=32,
            corner_radius=8
        )
        delete_button.grid(row=0, column=1, padx=2)
        
        if not delete_icon:
            delete_button.configure(text="X", fg_color="red", width=20)

        add_section_button = ctk.CTkButton(group_frame, text="Add Section", command=lambda g=group_count: add_section(g))
        add_section_button.grid(row=1, column=0, columnspan=2, pady=5)
        add_section_buttons.append(add_section_button)
        
        for _ in range(4):
            add_section(group_count)

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

        row = ((section_index - 1) // 2) + 2
        col = (section_index - 1) % 2

        group_frame = toggle_buttons[group_number - 1].master.master
        
        group_frame.grid_columnconfigure(0, weight=1)
        group_frame.grid_columnconfigure(1, weight=1)

        label_text = section_names[group_number][section_index]
        label = ctk.CTkLabel(
            group_frame, text=label_text, width=80, height=40, corner_radius=8,
            fg_color="gray30", text_color="black", font=("Arial", 14)
        )
        label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
        labels.append(label)

        label.bind("<Button-3>", lambda e, g=group_number, i=section_index: define_section(g, i))
        label.bind("<Button-1>", lambda e, g=group_number, i=section_index: open_rename_section(g, i))

        update_ui()
        print(f"Added {section_names[group_number][section_index]} to Group {group_number}")

    def open_rename_modal(item_type, item_number):
        modal = ctk.CTkToplevel(app)
        modal.title(f"Rename {item_type} {item_number}")
        
        center_window(modal, 300, 150)
        
        modal.transient(app)
        modal.attributes('-topmost', True)
        modal.grab_set()
        
        label = ctk.CTkLabel(modal, text=f"Enter new name for {item_type} {item_number}:")
        label.pack(pady=10)

        entry = ctk.CTkEntry(modal, width=100)
        entry.pack(pady=10)
        if item_type == "Group":
            entry.insert(0, group_names[item_number])
        else:
            for group_num in range(1, group_count + 1):
                if item_number in section_names[group_num]:
                    entry.insert(0, section_names[group_num][item_number])
                    break

        def set_name():
            new_name = entry.get()
            if new_name:
                if item_type == "Group":
                    group_names[item_number] = new_name
                    update_ui()
                elif item_type == "Section":
                    for group_num in range(1, group_count + 1):
                        if item_number in section_names[group_num]:
                            section_names[group_num][item_number] = new_name
                            update_ui()
                            break
            modal.destroy()

        set_button = ctk.CTkButton(modal, text="Set", command=set_name)
        set_button.pack(pady=10)

    def define_section(group_number, section_number):
        monitors = get_monitors()
        combined_width = sum(monitor.width for monitor in monitors)
        combined_height = max(monitor.height for monitor in monitors)

        app.iconify()
        
        time.sleep(0.2)

        root = tk.Tk()
        root.geometry(f"{combined_width}x{combined_height}-0+0")
        
        root.overrideredirect(True)
        root.attributes('-topmost', True)
        root.attributes('-alpha', 0.3)
        
        min_x = min(monitor.x for monitor in monitors)
        min_y = min(monitor.y for monitor in monitors)
        root.geometry(f"+{min_x}+{min_y}")

        canvas = tk.Canvas(root, cursor="cross", width=combined_width, height=combined_height, 
                          highlightthickness=0)
        canvas.configure(bg='black')
        canvas.pack(fill="both", expand=True)

        instructions = "Click and drag to define section area. Press ESC to cancel."
        canvas.create_text(combined_width//2, 50, text=instructions, fill="white", font=("Arial", 16))

        start_x = start_y = 0
        rect_id = None

        def on_click(event):
            nonlocal start_x, start_y
            start_x = root.winfo_pointerx() - root.winfo_rootx()
            start_y = root.winfo_pointery() - root.winfo_rooty()

        def on_drag(event):
            nonlocal rect_id
            if rect_id:
                canvas.delete(rect_id)
            
            current_x = root.winfo_pointerx() - root.winfo_rootx()
            current_y = root.winfo_pointery() - root.winfo_rooty()
            
            rect_id = canvas.create_rectangle(
                start_x, start_y, 
                current_x, current_y, 
                outline='red', width=2
            )

        def on_release(event):
            end_x = root.winfo_pointerx() - root.winfo_rootx()
            end_y = root.winfo_pointery() - root.winfo_rooty()
            
            center_x = (start_x + end_x) // 2
            center_y = (start_y + end_y) // 2
            
            index = (group_number - 1) * max_sections_per_group + (section_number - 1)
            section_positions[index] = (center_x, center_y)
            print(f"Section {section_number} in Group {group_number} defined at {section_positions[index]} (across all displays)")
            root.destroy()
            app.deiconify()

        def on_escape(event):
            root.destroy()
            app.deiconify()

        root.bind("<Escape>", on_escape)
        canvas.bind("<Button-1>", on_click)
        canvas.bind("<B1-Motion>", on_drag)
        canvas.bind("<ButtonRelease-1>", on_release)

        root.mainloop()

    def open_rename_section(group_number, section_index):
        modal = ctk.CTkToplevel(app)
        modal.title(f"Section {section_index} Options")
        
        center_window(modal, 300, 200)
        
        modal.transient(app)
        modal.attributes('-topmost', True)
        modal.grab_set()
        
        label = ctk.CTkLabel(modal, text=f"Options for {section_names[group_number][section_index]}:")
        label.pack(pady=10)

        entry = ctk.CTkEntry(modal, width=200)
        entry.pack(pady=10)
        entry.insert(0, section_names[group_number][section_index])

        def set_name():
            new_name = entry.get()
            if new_name:
                section_names[group_number][section_index] = new_name
                update_ui()
            modal.destroy()

        def delete():
            modal.destroy()
            delete_section(group_number, section_index)

        button_frame = ctk.CTkFrame(modal, fg_color="transparent")
        button_frame.pack(pady=10, fill="x")
        
        set_button = ctk.CTkButton(button_frame, text="Rename", command=set_name)
        set_button.pack(side="left", padx=10)
        
        delete_button = ctk.CTkButton(button_frame, text="Delete", fg_color="red", command=delete)
        delete_button.pack(side="right", padx=10)

    def toggle_group(group_number):
        start_index = (group_number - 1) * max_sections_per_group
        end_index = start_index + group_section_counts[group_number]
        
        progress_window = ctk.CTkToplevel(app)
        progress_window.title("Processing")
        
        center_window(progress_window, 300, 100)
        
        progress_window.attributes('-topmost', True)
        
        progress_label = ctk.CTkLabel(progress_window, text=f"Processing {group_names[group_number]}...")
        progress_label.pack(pady=10)
        
        progress_bar = ctk.CTkProgressBar(progress_window)
        progress_bar.pack(pady=10, padx=20, fill="x")
        progress_bar.set(0)
        
        progress_window.update()
        
        total_sections = end_index - start_index
        for i, idx in enumerate(range(start_index, end_index)):
            if section_positions[idx] == (0, 0):
                continue
                
            move_to_section(idx + 1, section_positions)
            progress_bar.set((i + 1) / total_sections)
            progress_window.update()
            time.sleep(0.3)
        
        progress_window.destroy()
        
        show_warning(f"Operations completed for {group_names[group_number]}")
        print(f"Operations completed for {group_names[group_number]}")

    def update_ui():
        for group_number in range(1, group_count + 1):
            if group_number <= len(toggle_buttons):
                button = toggle_buttons[group_number - 1]
                button.configure(text=group_names[group_number])
                for i in range(1, group_section_counts[group_number] + 1):
                    if i in section_names[group_number]:
                        for label in labels:
                            if label.master == button.master.master and label.cget("text") == section_names[group_number].get(i, f"Section {i}"):
                                label.configure(text=section_names[group_number][i])
                                break

    def show_warning(message):
        messagebox.showinfo("Warning", message)

    def on_exit():
        icon.stop()
        app.quit()
        sys.exit()

    def toggle_window():
        if app.state() == 'withdrawn':
            app.deiconify()
            app.lift()
            app.focus_force()
        else:
            app.withdraw()

    def reset_group_positions(group_number):
        start_index = (group_number - 1) * max_sections_per_group
        end_index = start_index + group_section_counts[group_number]
        
        for i in range(start_index, end_index):
            section_positions[i] = (0, 0)
        
        print(f"Reset positions for Group {group_number}")
        show_warning(f"Reset positions for Group {group_number}")
        
        if toggle_buttons[group_number - 1].cget("fg_color") == "green":
            toggle_group(group_number)

    def register_shortcuts():
        keyboard.unhook_all()
        
        for group_num, shortcut in group_shortcuts.items():
            if group_num <= group_count and shortcut:
                try:
                    keyboard.add_hotkey(shortcut, 
                                      lambda g=group_num: toggle_group(g))
                    print(f"Registered shortcut {shortcut} for Group {group_num}")
                except Exception as e:
                    print(f"Failed to register shortcut {shortcut}: {e}")
        
        keyboard.add_hotkey('esc', on_exit)
        
        print("Keyboard shortcuts registered")

    def open_shortcuts_dialog():
        dialog = ctk.CTkToplevel(app)
        dialog.title("Keyboard Shortcuts")
        
        center_window(dialog, 400, 400)
        
        dialog.transient(app)
        dialog.attributes('-topmost', True)
        dialog.grab_set()
        
        container = ctk.CTkScrollableFrame(dialog, width=380, height=300)
        container.pack(pady=10, padx=10, fill="both", expand=True)
        
        header_frame = ctk.CTkFrame(container, fg_color="transparent")
        header_frame.pack(fill="x", pady=(0, 10))
        
        ctk.CTkLabel(header_frame, text="Group", font=("Arial", 14, "bold")).pack(side="left", padx=(10, 0))
        ctk.CTkLabel(header_frame, text="Shortcut", font=("Arial", 14, "bold")).pack(side="right", padx=(0, 10))
        
        entries = {}
        for group_num in range(1, group_count + 1):
            row = ctk.CTkFrame(container)
            row.pack(fill="x", pady=5)
            
            group_label = ctk.CTkLabel(row, text=group_names[group_num], width=150)
            group_label.pack(side="left", padx=10)
            
            shortcut_entry = ctk.CTkEntry(row, width=200)
            shortcut_entry.pack(side="right", padx=10)
            shortcut_entry.insert(0, group_shortcuts.get(group_num, ""))
            
            entries[group_num] = shortcut_entry
        
        # Add a help label
        help_label = ctk.CTkLabel(container, text="Format: ctrl+shift+1, alt+f, etc.", 
                                 text_color="gray70", font=("Arial", 12))
        help_label.pack(pady=(10, 0))
        
        def save_shortcuts():
            for group_num, entry in entries.items():
                group_shortcuts[group_num] = entry.get()
            
            register_shortcuts()
            
            dialog.destroy()
            show_warning("Shortcuts updated successfully")
        
        def reset_to_defaults():
            for group_num, entry in entries.items():
                default_shortcut = f'ctrl+shift+{group_num}'
                entry.delete(0, 'end')
                entry.insert(0, default_shortcut)
        
        # Create a button frame for the buttons at the bottom
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(pady=10, fill="x", padx=20)
        
        # Add buttons to the frame
        save_button = ctk.CTkButton(button_frame, text="Save", command=save_shortcuts, width=120)
        save_button.pack(side="left", padx=10)
        
        reset_button = ctk.CTkButton(button_frame, text="Reset to Defaults", command=reset_to_defaults, width=120)
        reset_button.pack(side="left", padx=10)
        
        cancel_button = ctk.CTkButton(button_frame, text="Cancel", command=dialog.destroy, width=120)
        cancel_button.pack(side="right", padx=10)

    def delete_section(group_number, section_index):
        if group_section_counts[group_number] <= 1:
            show_warning(f"Cannot delete the last section in Group {group_number}.\nDelete the entire group instead.")
            return
        
        section_label = None
        for label in labels:
            if label.master == toggle_buttons[group_number - 1].master.master:
                if label.cget("text") == section_names[group_number][section_index]:
                    section_label = label
                    break
        
        if section_label:
            section_label.destroy()
            labels.remove(section_label)
        
        pos_index = (group_number - 1) * max_sections_per_group + (section_index - 1)
        section_positions[pos_index] = (0, 0)
        
        del section_names[group_number][section_index]
        
        group_section_counts[group_number] -= 1
        
        reorganize_sections(group_number)
        
        print(f"Deleted Section {section_index} from Group {group_number}")

    def delete_group(group_number):
        nonlocal group_count
        
        if group_count <= 1:
            show_warning("Cannot delete the last group.")
            return
        
        group_frame = toggle_buttons[group_number - 1].master.master
        
        group_frame.destroy()
        
        toggle_buttons.pop(group_number - 1)
        
        add_section_buttons.pop(group_number - 1)
        
        start_index = (group_number - 1) * max_sections_per_group
        end_index = start_index + max_sections_per_group
        for i in range(start_index, end_index):
            section_positions[i] = (0, 0)
        
        del group_names[group_number]
        del section_names[group_number]
        del group_section_counts[group_number]
        
        group_count -= 1
        
        reorganize_groups()
        
        print(f"Deleted Group {group_number}")

    def reorganize_sections(group_number):
        group_frame = toggle_buttons[group_number - 1].master.master
        
        for widget in group_frame.winfo_children():
            if isinstance(widget, ctk.CTkLabel):
                widget.grid_forget()
        
        section_indices = sorted(section_names[group_number].keys())
        for i, section_index in enumerate(section_indices):
            row = (i // 2) + 2
            col = i % 2
            
            label_text = section_names[group_number][section_index]
            for label in labels:
                if label.master == group_frame and label.cget("text") == label_text:
                    label.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
                    break

    def reorganize_groups():
        nonlocal group_names, section_names, group_section_counts, section_positions, group_shortcuts
        
        old_to_new_group_map = {old_num: new_num for new_num, old_num in 
                               enumerate(sorted(group_names.keys()), 1)}
        
        new_group_names = {}
        new_section_names = {}
        new_group_section_counts = {}
        new_group_shortcuts = {}
        
        for old_group_num, new_group_num in old_to_new_group_map.items():
            new_group_names[new_group_num] = group_names[old_group_num]
            new_section_names[new_group_num] = section_names[old_group_num]
            new_group_section_counts[new_group_num] = group_section_counts[old_group_num]
            if old_group_num in group_shortcuts:
                new_group_shortcuts[new_group_num] = group_shortcuts[old_group_num]
        
        for i in range(1, max_groups + 1):
            if i not in new_group_shortcuts:
                new_group_shortcuts[i] = f'ctrl+shift+{i}'
        
        new_section_positions = [(0, 0) for _ in range(max_groups * max_sections_per_group)]
        
        for old_group_num, new_group_num in old_to_new_group_map.items():
            for section_idx in range(1, group_section_counts[old_group_num] + 1):
                old_pos_idx = (old_group_num - 1) * max_sections_per_group + (section_idx - 1)
                new_pos_idx = (new_group_num - 1) * max_sections_per_group + (section_idx - 1)
                
                if old_pos_idx < len(section_positions):
                    new_section_positions[new_pos_idx] = section_positions[old_pos_idx]
        
        group_names = new_group_names
        section_names = new_section_names
        group_section_counts = new_group_section_counts
        section_positions = new_section_positions
        group_shortcuts = new_group_shortcuts
        
        register_shortcuts()
        
        for i, toggle_button in enumerate(toggle_buttons):
            group_frame = toggle_button.master.master
            group_frame.grid_forget()
            group_frame.grid(row=i // 4, column=i % 4, rowspan=1, columnspan=1, padx=5, pady=5, sticky="nsew")
            
            toggle_button.configure(text=group_names[i + 1])
            
            toggle_button.configure(command=lambda g=i+1: toggle_group(g))
            
            reset_button = None
            for widget in toggle_button.master.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for btn in widget.winfo_children():
                        if isinstance(btn, ctk.CTkButton) and not btn.cget("text"):
                            reset_button = btn
                            break
            
            if reset_button:
                reset_button.configure(command=lambda g=i+1: reset_group_positions(g))
            
            delete_button = None
            for widget in toggle_button.master.winfo_children():
                if isinstance(widget, ctk.CTkFrame):
                    for btn in widget.winfo_children():
                        if isinstance(btn, ctk.CTkButton) and (btn.cget("text") == "X" or btn.cget("image")):
                            delete_button = btn
                            break
            
            if delete_button:
                delete_button.configure(command=lambda g=i+1: delete_group(g))
            
            toggle_button.bind("<Button-3>", lambda e, g=i+1: open_rename_modal("Group", g))
            
            add_section_button = add_section_buttons[i]
            add_section_button.configure(command=lambda g=i+1: add_section(g))
        
        update_ui()

    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("green")

    app = ctk.CTk()
    app.title("Screen Section Mover")
    
    center_window(app, 1000, 800)
    
    app.minsize(1000, 800)
    app.maxsize(1000, 800)
    
    menu_bar = tk.Menu(app)
    app.configure(menu=menu_bar)
    
    file_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="File", menu=file_menu)
    file_menu.add_command(label="Exit", command=on_exit)
    
    help_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Help", menu=help_menu)
    help_menu.add_command(label="About", command=lambda: messagebox.showinfo(
        "About", "Screen Section Mover v1.0\n\nA tool to define and navigate screen sections."
    ))
    help_menu.add_command(label="Shortcuts", command=lambda: messagebox.showinfo(
        "Keyboard Shortcuts", 
        "\n".join([f"{group_names[g]}: {shortcut}" for g, shortcut in group_shortcuts.items() if g <= group_count]) +
        "\n\nEsc: Exit application"
    ))

    settings_menu = tk.Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Settings", menu=settings_menu)
    settings_menu.add_command(label="Edit Shortcuts", command=open_shortcuts_dialog)

    main_frame = ctk.CTkFrame(app, corner_radius=15, fg_color="gray30")
    main_frame.pack(pady=5, padx=5, fill="both", expand=True)

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
        group_frame = ctk.CTkFrame(main_frame, corner_radius=15, fg_color=group_frame_color, width=200)
        group_frame.grid(row=(group_number - 1) // 4, column=(group_number - 1) % 4, rowspan=1, columnspan=1, padx=5, pady=5, sticky="nsew")

        group_frame.grid_columnconfigure(0, weight=1)
        group_frame.grid_columnconfigure(1, weight=1)

        button_frame = ctk.CTkFrame(group_frame, fg_color="transparent")
        button_frame.grid(row=0, column=0, columnspan=2, pady=5, sticky="ew")
        
        button_frame.grid_columnconfigure(0, weight=2)
        button_frame.grid_columnconfigure(1, weight=1)

        toggle_button = ctk.CTkButton(
            button_frame, 
            text=group_names[group_number],
            command=lambda g=group_number: toggle_group(g),
            fg_color="gray50",
            text_color="white",
            height=28,
            width=140
        )
        toggle_button.grid(row=0, column=0, pady=5, padx=(10, 5), sticky="ew")
        toggle_buttons.append(toggle_button)

        try:
            reset_icon = ctk.CTkImage(
                light_image=Image.open("assets/reset_icon.png"),
                dark_image=Image.open("assets/reset_icon.png"),
                size=(20, 20)
            )
            delete_icon = ctk.CTkImage(
                light_image=Image.open("assets/delete_icon.png"),
                dark_image=Image.open("assets/delete_icon.png"),
                size=(20, 20)
            )
        except Exception as e:
            print(f"Failed to load icons: {e}")
            reset_icon = None
            delete_icon = None

        button_actions_frame = ctk.CTkFrame(button_frame, fg_color="transparent")
        button_actions_frame.grid(row=0, column=1, pady=5, padx=(0, 10))

        reset_button = ctk.CTkButton(
            button_actions_frame,
            text="",
            image=reset_icon if reset_icon else None,
            command=lambda g=group_number: reset_group_positions(g),
            fg_color="transparent",
            text_color="white",
            height=32,
            width=32,
            corner_radius=8
        )
        reset_button.grid(row=0, column=0, padx=2)

        delete_button = ctk.CTkButton(
            button_actions_frame,
            text="",
            image=delete_icon if delete_icon else None,
            command=lambda g=group_number: delete_group(g),
            fg_color="transparent",
            text_color="white",
            height=32,
            width=32,
            corner_radius=8
        )
        delete_button.grid(row=0, column=1, padx=2)
        
        if not delete_icon:
            delete_button.configure(text="X", fg_color="red", width=20)

        add_section_button = ctk.CTkButton(group_frame, text="Add Section", command=lambda g=group_number: add_section(g))
        add_section_button.grid(row=1, column=0, columnspan=2, pady=5)
        add_section_buttons.append(add_section_button)

        layout = group_layouts[group_number - 1]

        for i, (row, col) in enumerate(layout):
            section_index = i + 1
            label_text = section_names[group_number][section_index]
            label = ctk.CTkLabel(
                group_frame, text=label_text, width=80, height=40, corner_radius=8,
                fg_color="gray30", text_color="black", font=("Arial", 14)
            )
            label.grid(row=row + 2, column=col, padx=5, pady=5, sticky="nsew")
            labels.append(label)

            label.bind("<Button-3>", lambda e, g=group_number, i=section_index: define_section(g, i))
            label.bind("<Button-1>", lambda e, g=group_number, i=section_index: open_rename_section(g, i))

    for i, toggle_button in enumerate(toggle_buttons, start=1):
        toggle_button.bind("<Button-3>", lambda e, i=i: open_rename_modal("Group", i))

    add_group_button = ctk.CTkButton(app, text="Add Group", command=add_group)
    add_group_button.pack(pady=5)

    try:
        icon_image = Image.open("assets/app_icon.png")
        icon_image = icon_image.resize((64, 64))
    except Exception as e:
        print(f"Failed to load custom icon: {e}")
        icon_image = Image.new('RGB', (64, 64), color='green')

    menu = (
        pystray.MenuItem("Show/Hide", toggle_window),
        pystray.MenuItem("Exit", on_exit)
    )
    
    icon = pystray.Icon(
        "Screen Section Mover",
        icon_image,
        "Screen Section Mover",
        menu
    )
    
    icon.left_click_action = toggle_window

    def on_closing():
        app.withdraw()
    
    app.protocol('WM_DELETE_WINDOW', on_closing)

    icon_thread = threading.Thread(target=icon.run)
    icon_thread.daemon = True
    icon_thread.start()

    register_shortcuts()

    status_bar = ctk.CTkFrame(app, height=25)
    status_bar.pack(side="bottom", fill="x")
    
    status_label = ctk.CTkLabel(status_bar, text="Ready")
    status_label.pack(side="left", padx=10)
    
    shortcuts_button = ctk.CTkButton(status_bar, text="Edit Shortcuts", 
                                    width=100, height=20, 
                                    command=open_shortcuts_dialog)
    shortcuts_button.pack(side="left", padx=10)
    
    version_label = ctk.CTkLabel(status_bar, text="v1.0")
    version_label.pack(side="right", padx=10)

    app.mainloop()

    keyboard.wait('esc')

if __name__ == "__main__":
    main()