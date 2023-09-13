import ttkbootstrap as tb
import ttkbootstrap as ttk
import screen_brightness_control as sbc
from time import strftime
from configparser import ConfigParser
import os

# Read config file
config = ConfigParser()
config.read('options.ini')

# Create window
root = tb.Window(themename="superhero")
root.title("Desktop Brightness App")
root.geometry("1280x720")

# UI for date and time
label_date_time = tb.Label(root)
label_date_time.place(x=1170, y=0)


def date_time():
    date_and_time = strftime('%m-%d-%Y %H:%M:%S')
    label_date_time.config(text=date_and_time)
    label_date_time.after(1000, date_time)


def get_monitors():
    for monitor in sbc.list_monitors():
        print("Listed all monitors: ", monitor)


def set_brightness(val):
    label_brightness.config(text=f"Brightness: {int(scale_1.get())}")
    label_brightness.place(x=600, y=100)
    val = int(scale_1.get())

    if val:
        sbc.set_brightness(val)
        print("Brightness is now:", val)
        config['OPTIONS']['brightness'] = str(val)
        with open('options.ini', 'w') as configfile:
            config.write(configfile)


# UI theme option
theme_list = root.style.theme_names()
themes = ttk.StringVar(value=root.style.theme_use())
c_box = tb.Combobox(root, values=theme_list, state="readonly", width=15)
c_box.place(x=1000, y=0)


def change_theme(event):
    root.style.theme_use(c_box.get())
    config['OPTIONS']['theme'] = (event.widget.get())
    with open('options.ini', 'w') as configfile:
        config.write(configfile)


c_box.bind("<<ComboboxSelected>>", change_theme)

# UI for brightness
label_brightness_name = tb.Label(root, text="Adjust Brightness", font=("Arial bold", 13))
label_brightness_name.pack(pady=30)

scale_1 = tb.Scale(root, from_=0, to=100, orient="horizontal", length=200, command=set_brightness)
scale_1.pack(pady=50)

label_brightness = tb.Label(root)
label_brightness.pack(pady=15)

button_to_0 = tb.Button(root, text="0", command=lambda: scale_1.set(1))
button_to_0.place(x=525, y=155)

button_to_25 = tb.Button(root, text="25", command=lambda: scale_1.set(25))
button_to_25.place(x=575, y=155)

button_to_50 = tb.Button(root, text="50", command=lambda: scale_1.set(50))
button_to_50.place(x=625, y=155)

button_to_75 = tb.Button(root, text="75", command=lambda: scale_1.set(75))
button_to_75.place(x=675, y=155)

button_to_100 = tb.Button(root, text="100", command=lambda: scale_1.set(100))
button_to_100.place(x=725, y=155)


def load_last_settings():
    if not os.path.exists('options.ini') or 'OPTIONS' not in config:
        config['OPTIONS'] = {
            'brightness': '0',
            'theme': 'superhero',
        }
        with open('options.ini', 'w') as configfile:
            config.write(configfile)

    brightness = config['OPTIONS'].getint('brightness')
    theme = config['OPTIONS'].get('theme')
    scale_1.set(brightness)
    root.style.theme_use(theme)
    if theme == config['OPTIONS']['theme'] and brightness == config['OPTIONS'].getint('brightness'):

        label_notes = tb.Label(root, text="Reminder: Your last settings have been automatically loaded.",
                               font=("Italic'", 10))
        label_notes.place(x=0, y=0)
    else:
        label_notes = tb.Label(root, text="ERROR: Your last settings have not been loaded.",
                               font=("Italic'", 10))
        label_notes.place(x=0, y=0)


get_monitors()
date_time()
load_last_settings()
root.mainloop()
