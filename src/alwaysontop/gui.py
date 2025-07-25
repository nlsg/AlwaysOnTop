import tkinter as tk
from tkinter import ttk
from .api import set_always_on_top, iter_window_titles

# Track pinned windows
pinned_windows = {}


def refresh_windows(tree, status_label, root_title):
    global pinned_windows
    window_list = list(iter_window_titles(excludes=[root_title]))

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

    new_state = not current_state
    pinned_windows[window_title] = new_state
    set_always_on_top(window_title, new_state)

    new_icon = "📌" if new_state else "❌"
    tree.item(item, values=(window_title, new_icon))


def create_gui():
    root = tk.Tk()
    root.title("📌 Always On Top")
    root.geometry("500x320")
    root.configure(bg="#1a1b26")
    root.resizable(True, True)
    root.attributes("-topmost", True)

    root.bind("<FocusIn>", lambda *_: refresh_windows(tree, status, root.title()))
    style = ttk.Style()
    style.theme_use("clam")

    bg_color = "#1a1b26"
    fg_color = "#a9b1d6"
    accent_color = "#7aa2f7"
    button_bg = "#24283b"
    hover_color = "#414868"
    row_color = "#24283b"

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

    # Treeview custom styling
    style.configure(
        "Custom.Treeview",
        background=row_color,
        fieldbackground=row_color,
        foreground=fg_color,
        rowheight=28,
        borderwidth=0,
        relief="flat",
    )
    style.map("Custom.Treeview", background=[("selected", hover_color)])

    main = ttk.Frame(root, padding=20)
    main.pack(expand=True, fill=tk.BOTH)

    # --- Treeview with scrollbars ---
    tree_frame = ttk.Frame(main)
    tree_frame.pack(expand=True, fill=tk.BOTH)

    columns = ("title", "status")
    tree = ttk.Treeview(
        tree_frame,
        columns=columns,
        show="headings",
        style="Custom.Treeview",
    )
    tree.heading("title", text="Window Title")
    tree.heading("status", text="Pin")
    tree.column("title", anchor=tk.W)
    tree.column("status", width=60, anchor=tk.CENTER)

    tree.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

    # Scrollbar
    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree.bind("<Button-1>", lambda e: toggle_pin(tree, e))

    # Buttons
    buttons = ttk.Frame(main)
    buttons.pack(pady=10)

    ttk.Button(
        buttons,
        text="🔄 Refresh",
        command=lambda: refresh_windows(tree, status, root.title()),
    ).pack(side=tk.LEFT, padx=5)

    # Status bar
    global status
    status = ttk.Label(main, text="Ready", font=("Segoe UI", 9), foreground="#565f89")
    status.pack(pady=(10, 0))

    refresh_windows(tree, status, root.title())
    root.mainloop()
