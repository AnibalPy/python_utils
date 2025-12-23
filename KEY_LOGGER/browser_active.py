import psutil

import psutil
import win32gui
import win32process

apps = {
    "chrome.exe": "Google Chrome",
    "msedge.exe": "Microsoft Edge",
    "brave.exe": "Brave",
    "opera.exe": "Opera",
    "whatsapp.exe": "WhatsApp Desktop",
    "whatsapp.root.exe": "WhatsApp Desktop"
}

def get_visible_process_names():
    visible_processes = set()

    def enum_window_callback(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            _, pid = win32process.GetWindowThreadProcessId(hwnd)
            try:
                proc = psutil.Process(pid)
                visible_processes.add(proc.name().lower())
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        return True

    win32gui.EnumWindows(enum_window_callback, None)
    return visible_processes

visible = get_visible_process_names()
active_apps = [name for exe, name in apps.items() if exe in visible]

if active_apps:
    print("Aplicaciones con ventana visible:")
    for app in active_apps:
        print(f"- {app}")
else:
    print("Ninguna aplicación compatible con ventana visible.")
