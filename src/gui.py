import tkinter as tk
from tkinter import ttk
from api import set_always_on_top, iter_window_titles


# Refresh window list
def refresh_windows(root: tk.Tk):
    # Filter out empty titles and potentially the app's own window
    window_list = list(iter_window_titles(excludes=[root.title()]))

    current_selection = combo.get()
    combo["values"] = window_list

    # Try to keep the current selection if it still exists
    if current_selection in window_list:
        combo.set(current_selection)
    elif window_list:
        combo.set(window_list[0])
    else:
        combo.set("")
    status.config(text="Window list refreshed. Ready.")


# --- GUI Setup ---
root = tk.Tk()
root.title("📌 Always On Top")
root.geometry("500x320")
root.configure(bg="#1a1b26")
root.resizable(False, False)

# --- FIX 1: Make the app itself always on top (the correct way) ---
# This is the native tkinter way, more reliable than the previous method.
root.attributes("-topmost", True)

# --- Styling ---
style = ttk.Style()
style.theme_use("clam")

bg_color = "#1a1b26"
fg_color = "#a9b1d6"
accent_color = "#7aa2f7"
button_bg = "#24283b"
hover_color = "#414868"

style.configure(".", background=bg_color, foreground=fg_color, font=("Segoe UI", 10))
style.configure(
    "TButton",
    background=button_bg,
    foreground=fg_color,
    padding=12,
    borderwidth=0,
    relief="flat",
    font=("Segoe UI", 10, "bold"),
)
style.map(
    "TButton",
    background=[("active", hover_color), ("pressed", accent_color)],
    foreground=[("active", "#ffffff"), ("pressed", "#ffffff")],
)
style.configure(
    "TCombobox",
    fieldbackground=button_bg,
    background=button_bg,
    foreground=fg_color,
    arrowcolor=accent_color,
    padding=8,
    font=("Segoe UI", 10),
)
style.map(
    "TCombobox",
    fieldbackground=[("readonly", button_bg)],
    selectbackground=[("readonly", accent_color)],
    selectforeground=[("readonly", "#ffffff")],
)

# --- Layout ---
main = ttk.Frame(root, padding=30)
main.pack(expand=True, fill=tk.BOTH)

header = ttk.Label(
    main, text="Always On Top", font=("Segoe UI", 24, "bold"), foreground=accent_color
)
header.pack(pady=(0, 20))

subheader = ttk.Label(
    main,
    text="Select a window to pin or unpin:",
    font=("Segoe UI", 12),
    foreground=fg_color,
)
subheader.pack(pady=(0, 15))

combo = ttk.Combobox(main, width=50, state="readonly")
combo.pack(pady=(0, 20))

buttons = ttk.Frame(main)
buttons.pack(pady=15)

refresh_btn = ttk.Button(
    buttons, text="🔄 Refresh", command=lambda: refresh_windows(root)
)
refresh_btn.pack(side=tk.LEFT, padx=5)

pin_btn = ttk.Button(
    buttons, text="📌 Pin Window", command=lambda: set_always_on_top(combo.get(), True)
)
pin_btn.pack(side=tk.LEFT, padx=5)

# --- FIX 3: Added the UNPIN button to the GUI ---
unpin_btn = ttk.Button(
    buttons,
    text="✖️ Unpin Window",
    command=lambda: set_always_on_top(combo.get(), False),
)
unpin_btn.pack(side=tk.LEFT, padx=5)


status = ttk.Label(
    main, text="Ready to pin", font=("Segoe UI", 9), foreground="#565f89"
)
status.pack(pady=(20, 0))

# Init
refresh_windows(root)
root.mainloop()
