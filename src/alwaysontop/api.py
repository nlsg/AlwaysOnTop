from typing import Iterator
import pygetwindow as gw
import win32gui
import win32con


def get_window_handle(window_title: str) -> int:
    if not window_title or (hwnd := win32gui.FindWindow(None, window_title)) == 0:
        raise Exception(
            f"Window '{window_title}' not found. It might have been closed. Please refresh the list."
        )
    return hwnd


def set_always_on_top(window: int | str, on_top: bool):
    window_handle = window if isinstance(window, int) else get_window_handle(window)
    win32gui.SetWindowPos(
        window_handle,
        (win32con.HWND_TOPMOST if on_top else win32con.HWND_NOTOPMOST),
        0,
        0,
        0,
        0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE,
    )


def iter_window_titles(excludes: list[str]) -> Iterator[str]:
    for window in gw.getWindowsWithTitle(""):
        if window.title and window.title not in excludes:
            yield window.title
