#!/Scripts/python
import os
import time
import keyboard
import mouse
import json
import threading
import customtkinter as ctk
from tkinter import Menu

# Storage for recorded events and settings
recorded_events = []
recording = False
settings = {
    "app_name": "Tiny Task",
    "theme": "Dark",
    "start_key": "F1",
    "stop_key": "F2",
    "replay_key": "F3",
    "path": ".\\record.json",
    "on_top": "True",
}

# Initialize CustomTkinter
ctk.set_appearance_mode(settings["theme"])
ctk.set_default_color_theme("blue")

path = os.path.join(settings["path"])

# Create main app window
app = ctk.CTk()
app.title(settings["app_name"])
app.geometry("500x350+0+0")
app.attributes("-topmost", settings["on_top"])


def record_events():
    """ Record keyboard and mouse events """
    global recorded_events, recording
    recorded_events = []
    recording = True
    update_ui_state(True)  # Disable buttons during recording

    print("Recording started... Press", settings["stop_key"], "to stop.")
    start_time = time.time()

    def on_key_event(event):
        recorded_events.append({
            'type': 'keyboard',
            'event': event.event_type,
            'key': event.name,
            'time': time.time() - start_time
        })

    def on_mouse_event(event):
        global recorded_events
        event_data = {'type': 'mouse', 'time': time.time() - start_time}

        if isinstance(event, mouse.MoveEvent):
            x, y = mouse.get_position()
            event_data.update({'event': 'move', 'x': x, 'y': y})
        elif isinstance(event, mouse.ButtonEvent):
            x, y = mouse.get_position()
            event_data.update(
                {'event': 'click', 'button': event.button, 'pressed': event.event_type == 'down', 'x': x, 'y': y})
        elif isinstance(event, mouse.WheelEvent):
            x, y = mouse.get_position()
            event_data.update({'event': 'scroll', 'delta': event.delta, 'x': x, 'y': y})

        recorded_events.append(event_data)

    keyboard.hook(on_key_event)
    mouse.hook(on_mouse_event)

    keyboard.wait(settings["stop_key"])
    stop_recording()


def stop_recording():
    """ Stop recording and save events """
    global recording
    recording = False
    keyboard.unhook_all()
    mouse.unhook_all()
    save_events()
    update_ui_state(False)  # Enable buttons after stopping recording
    print("Recording stopped.")


def save_events():
    """ Save recorded events to a file """
    if settings["path"]:
        with open(settings["path"], "w") as f:
            json.dump(recorded_events, f, indent=4)
        print(f"Events saved to {settings['path']}")


def load_events():
    """ Load recorded events from a file """
    if settings["path"]:
        try:
            with open(settings["path"], "r") as f:
                return json.load(f)
        except FileNotFoundError:
            print("No saved macro found.")
            return []
    return []


def replay_events():
    """ Replay recorded keyboard and mouse actions """
    events = load_events()
    if not events:
        print("No events to replay.")
        return

    print("Replaying actions...")
    start_time = time.time()
    update_ui_state(True)  # Disable buttons during replay

    for event in events:
        time.sleep(max(0, event['time'] - (time.time() - start_time)))

        if event['type'] == 'keyboard':
            if event['event'] == 'down':
                keyboard.press(event['key'])
            else:
                keyboard.release(event['key'])

        elif event['type'] == 'mouse':
            if event['event'] == 'move':
                mouse.move(event['x'], event['y'], absolute=True)
            elif event['event'] == 'click':
                mouse.move(event['x'], event['y'], absolute=True, duration=0.05)
                if event['pressed']:
                    mouse.press(event['button'])
                else:
                    mouse.release(event['button'])
            elif event['event'] == 'scroll':
                mouse.wheel(event['delta'])

    print("Replay finished.")
    update_ui_state(False)  # Enable buttons after replay


def update_ui_state(disabled):
    """ Update the UI button states """
    if disabled:
        start_button.configure(state="disabled")
        replay_button.configure(state="disabled")
        stop_button.configure(state="normal")
    else:
        start_button.configure(state="normal")
        replay_button.configure(state="normal")
        stop_button.configure(state="disabled")


def start_recording_thread():
    threading.Thread(target=record_events, daemon=True).start()


def start_replay_thread():
    threading.Thread(target=replay_events, daemon=True).start()


def open_settings():
    """ Open settings window to change theme & key bindings """
    settings_window = ctk.CTkToplevel(app)
    settings_window.title("Settings")
    settings_window.geometry("400x430+500+0")

    prev_settings = settings.copy()

    def save_settings():
        """ Save the new settings """
        settings["theme"] = theme_var.get()
        settings["start_key"] = start_key_entry.get()
        settings["stop_key"] = stop_key_entry.get()
        settings["replay_key"] = replay_key_entry.get()
        settings["on_top"] = on_top_var.get()
        try:
            app.bind(f"<{settings['start_key']}>", lambda event: start_recording_thread())
            app.bind(f"<{settings['stop_key']}>", lambda event: stop_recording())
            app.bind(f"<{settings['replay_key']}>", lambda event: start_replay_thread())
        except:
            pass
        ctk.set_appearance_mode(settings["theme"])
        app.attributes("-topmost", settings["on_top"])
        settings_window.destroy()
        print("Settings saved:", settings)

    def cancel_settings():
        """ Restore previous settings if user cancels """
        settings.update(prev_settings)
        settings_window.destroy()
        print("Settings canceled.")

    theme_var = ctk.StringVar(value=settings["theme"])
    ctk.CTkLabel(settings_window, text="Select Theme:").pack(pady=5)
    theme_dropdown = ctk.CTkOptionMenu(settings_window, variable=theme_var, values=["Light", "Dark", "System"])
    theme_dropdown.pack(pady=5)

    on_top_var = ctk.StringVar(value=settings["on_top"])
    ctk.CTkLabel(settings_window, text="Select Always on top:").pack(pady=5)
    on_top = ctk.CTkOptionMenu(settings_window, variable=on_top_var, values=["True", "False"])
    on_top.pack(pady=5)

    ctk.CTkLabel(settings_window, text="Start Recording Key:").pack(pady=5)
    start_key_entry = ctk.CTkEntry(settings_window, placeholder_text=settings["start_key"])
    start_key_entry.pack(pady=5)

    ctk.CTkLabel(settings_window, text="Stop Recording Key:").pack(pady=5)
    stop_key_entry = ctk.CTkEntry(settings_window, placeholder_text=settings["stop_key"])
    stop_key_entry.pack(pady=5)

    ctk.CTkLabel(settings_window, text="Replay Key:").pack(pady=5)
    replay_key_entry = ctk.CTkEntry(settings_window, placeholder_text=settings["replay_key"])
    replay_key_entry.pack(pady=5)

    button_frame = ctk.CTkFrame(settings_window)
    button_frame.pack(pady=10)

    save_button = ctk.CTkButton(button_frame, text="OK", command=save_settings)
    save_button.pack(side="left", padx=10)

    cancel_button = ctk.CTkButton(button_frame, text="Cancel", fg_color="red", command=cancel_settings)
    cancel_button.pack(side="right", padx=10)


###############################################################################
app.bind(f"<{settings['start_key']}>", lambda event: start_recording_thread())
app.bind(f"<{settings['stop_key']}>", lambda event: stop_recording())
app.bind(f"<{settings['replay_key']}>", lambda event: start_replay_thread())
###############################################################################

# UI Elements
menu = Menu(app)
app.config(menu=menu)

file_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Open", command=load_events)
file_menu.add_command(label="Save", command=save_events)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=app.quit)

settings_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Settings", menu=settings_menu)
settings_menu.add_command(label="Preferences", command=open_settings)

title_label = ctk.CTkLabel(app, text=f"{settings["app_name"]}", font=("Arial", 20))
title_label.pack(pady=10)

start_button = ctk.CTkButton(app, text="Start Recording", command=start_recording_thread)
start_button.pack(pady=10)

stop_button = ctk.CTkButton(app, text="Stop Recording", command=stop_recording, state="disabled")
stop_button.pack(pady=10)

replay_button = ctk.CTkButton(app, text="Replay Actions", command=start_replay_thread)
replay_button.pack(pady=10)

exit_button = ctk.CTkButton(app, text="Exit", command=app.quit, fg_color="red")
exit_button.pack(pady=10)

app.mainloop()
