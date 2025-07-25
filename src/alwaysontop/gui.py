import tkinter as tk
from tkinter import ttk
import re
import atexit
from .api import set_always_on_top, iter_window_titles

# Track pinned windows
pinned_windows = {}
search_pattern = ""


def refresh_windows(tree, root_title):
    global pinned_windows, search_pattern

    try:
        pattern = re.compile(search_pattern, re.IGNORECASE)
    except re.error:
        pattern = None  # invalid regex — show nothing

    window_list = list(iter_window_titles(excludes=[root_title]))

    filtered = []
    for title in window_list:
        if pattern and not pattern.search(title):
            continue
        is_pinned = pinned_windows.get(title, False)
        filtered.append((title, is_pinned))

    # Sort: pinned windows first, then alphabetically
    filtered.sort(key=lambda x: (not x[1], x[0].lower()))

    # Clear and re-populate tree
    for item in tree.get_children():
        tree.delete(item)

    for title, pinned in filtered:
        icon = "📌" if pinned else "❌"
        tree.insert("", tk.END, values=(title, icon))


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

    refresh_windows(tree, "📌 Always On Top")


def unpin_all(tree):
    global pinned_windows
    for title in list(pinned_windows.keys()):
        if pinned_windows[title]:
            set_always_on_top(title, False)
            pinned_windows[title] = False

    refresh_windows(tree, "📌 Always On Top")


def on_search_change(entry, tree, root_title):
    global search_pattern
    search_pattern = entry.get()
    refresh_windows(tree, root_title)


def create_gui():
    root = tk.Tk()
    root.title("📌 Always On Top")
    root.geometry("500x360")
    root.configure(bg="#1a1b26")
    root.resizable(True, True)
    root.attributes("-topmost", True)

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

    # --- Search bar ---
    search_frame = ttk.Frame(main)
    search_frame.pack(fill=tk.X, pady=(0, 10))

    search_label = ttk.Label(search_frame, text="🔍 Filter (regex):")
    search_label.pack(side=tk.LEFT)

    search_entry = ttk.Entry(search_frame)
    search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 0))
    search_entry.bind(
        "<KeyRelease>", lambda e: on_search_change(search_entry, tree, root.title())
    )

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

    scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    tree.bind("<Button-1>", lambda e: toggle_pin(tree, e))

    # Buttons
    button_frame = ttk.Frame(main)
    button_frame.pack(pady=10)

    unpin_all_btn = ttk.Button(
        button_frame,
        text="✖️ Unpin All",
        command=lambda: unpin_all(tree),
    )
    unpin_all_btn.pack()

    # Refresh when window gets focus
    root.bind("<FocusIn>", lambda *_: refresh_windows(tree, root.title()))

    refresh_windows(tree, root.title())
    atexit.register(lambda: unpin_all(tree))
    root.mainloop()
