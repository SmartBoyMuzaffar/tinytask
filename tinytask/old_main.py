import time
import keyboard
import mouse
import json
from pyautogui import *

# Storage for recorded events
recorded_events = []

def record_events():
    """ Record keyboard and mouse events """
    global recorded_events
    recorded_events = []  # Reset events list
    print("Recording started... Press 'Esc' to stop.")

    start_time = time.time()

    def on_key_event(event):
        recorded_events.append({
            'type': 'keyboard',
            'event': event.event_type,  # 'down' or 'up'
            'key': event.name,
            'time': time.time() - start_time
        })

    def on_mouse_event(event):
        """ Handles mouse events properly with accurate coordinates """
        global recorded_events
        event_data = {'type': 'mouse', 'time': time.time() - start_time}

        # Handle mouse move events (with correct coordinates)
        if isinstance(event, mouse.MoveEvent):
            x, y = mouse.get_position()  # Get real-time mouse position
            event_data.update({'event': 'move', 'x': x, 'y': y})

        # Handle mouse button events (clicks)
        elif isinstance(event, mouse.ButtonEvent):
            x, y = mouse.get_position()  # Capture exact click position
            event_data.update({
                'event': 'click',
                'button': event.button,
                'pressed': event.event_type == 'down',
                'x': x, 'y': y
            })

        # Handle mouse wheel events (scrolling)
        elif isinstance(event, mouse.WheelEvent):
            x, y = mouse.get_position()  # Capture exact position when scrolling
            event_data.update({'event': 'scroll', 'delta': event.delta, 'x': x, 'y': y})

        recorded_events.append(event_data)

    # Hook keyboard and mouse events
    keyboard.hook(on_key_event)
    mouse.hook(on_mouse_event)

    # Stop recording when 'Esc' is pressed
    keyboard.wait("esc")
    keyboard.unhook_all()
    mouse.unhook_all()

    print("Recording stopped.")
    save_events()  # Save to file

def save_events():
    """ Save recorded events to a file """
    with open("macro.json", "w") as f:
        json.dump(recorded_events, f, indent=4)
    print("Events saved to 'macro.json'.")

def load_events():
    """ Load recorded events from a file """
    try:
        with open("macro.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("No saved macro found.")
        return []

def replay_events():
    """ Replay recorded keyboard and mouse actions """
    events = load_events()
    if not events:
        print("No events to replay.")
        return

    print("Replaying actions...")
    start_time = time.time()

    for event in events:
        # Wait until it's time for this event
        time.sleep(max(0, event['time'] - (time.time() - start_time)))

        if event['type'] == 'keyboard':
            if event['event'] == 'down':
                keyboard.press(event['key'])
            else:
                keyboard.release(event['key'])


        elif event['type'] == 'mouse':

            if event['event'] == 'move':

                mouse.move(event['x'], event['y'], absolute=True)  # Smooth movement

            elif event['event'] == 'click':

                mouse.move(event['x'], event['y'], absolute=True,
                           duration=0.1)  # Ensure click happens at correct position

                if event['pressed']:

                    mouse.press(event['button'])

                else:

                    mouse.release(event['button'])

            elif event['event'] == 'scroll':

                mouse.wheel(event['delta'])  # Fixed scrolling

    print("Replay finished.")

# User Menu
print("Options:")
print("1: Record Actions")
print("2: Replay Actions")
choice = input("Enter your choice: ")

if choice == "1":
    record_events()
elif choice == "2":
    replay_events()
else:
    print("Invalid choice!")
