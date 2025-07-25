import tkinter as tk
from tkinter import ttk
from api import set_always_on_top, iter_window_titles


# Track pinned states internally
pinned_windows = {}


def refresh_windows(tree, status_label, root_title):
    global pinned_windows
    window_list = list(iter_window_titles(excludes=[root_title]))

    # Clean old items
    for item in tree.get_children():
        tree.delete(item)

    for title in window_list:
        pinned = pinned_windows.get(title, False)
        icon = "📌" if pinned else "❌"
        tree.insert("", tk.END, values=(title, icon))

    status_label.config(text="Window list refreshed. Ready.")


def toggle_pin(tree, event):
    global pinned_windows

    region = tree.identify("region", event.x, event.y)
    if region != "cell":
        return

    item = tree.identify_row(event.y)
    if not item:
        return

    window_title = tree.item(item, "values")[0]
    current_state = pinned_windows.get(window_title, False)

    # Toggle state
    new_state = not current_state
    pinned_windows[window_title] = new_state
    set_always_on_top(window_title, new_state)

    # Update icon
    new_icon = "📌" if new_state else "❌"
    tree.item(item, values=(window_title, new_icon))


def create_gui():
    root = tk.Tk()
    root.title("📌 Always On Top")
    root.geometry("500x320")
    root.configure(bg="#1a1b26")
    root.resizable(False, False)
    root.attributes("-topmost", True)

    style = ttk.Style()
    style.theme_use("clam")

    bg_color = "#1a1b26"
    fg_color = "#a9b1d6"
    accent_color = "#7aa2f7"
    button_bg = "#24283b"
    hover_color = "#414868"

    style.configure(
        ".", background=bg_color, foreground=fg_color, font=("Segoe UI", 10)
    )
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

    main = ttk.Frame(root, padding=30)
    main.pack(expand=True, fill=tk.BOTH)

    # --- Treeview: list of windows with icon ---
    columns = ("title", "status")
    tree = ttk.Treeview(main, columns=columns, show="headings", height=10)
    tree.heading("title", text="Window Title")
    tree.heading("status", text="Pin")
    tree.column("title", width=360, anchor=tk.W)
    tree.column("status", width=60, anchor=tk.CENTER)
    tree.pack(expand=True, fill=tk.BOTH)

    # Clickable toggle
    tree.bind("<Button-1>", lambda e: toggle_pin(tree, e))

    # --- Buttons ---
    buttons = ttk.Frame(main)
    buttons.pack(pady=15)

    ttk.Button(
        buttons,
        text="🔄 Refresh",
        command=lambda: refresh_windows(tree, status, root.title()),
    ).pack(side=tk.LEFT, padx=5)

    # --- Status bar ---
    global status
    status = ttk.Label(main, text="Ready", font=("Segoe UI", 9), foreground="#565f89")
    status.pack(pady=(10, 0))

    # Init
    refresh_windows(tree, status, root.title())
    root.mainloop()


if __name__ == "__main__":
    create_gui()
