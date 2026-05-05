#region Imports
import tkinter as tk
#endregion

#region GUI
root = tk.Tk()
root.title("Test")
root.geometry("1000x650")
root.configure(bg="black")
root.resizable(width=False, height=False)

HEIGHT = 650
WIDTH = 1000
BAR_HEIGHT = 50
BAR_WIDTH = 500

taskbar = tk.Frame(root, bg="gray")
inner_frame = tk.Frame(taskbar, bg="gray")
inner_frame.pack(fill="both", expand=True, padx=10, pady=10)

# Create buttons
weatherBtn = tk.Button(inner_frame, text="Weather")
musicBtn = tk.Button(inner_frame, text="Music")
newsBtn = tk.Button(inner_frame, text="News")
settingsBtn = tk.Button(inner_frame, text="Settings")

# Put them in a list
buttons = [weatherBtn, musicBtn, newsBtn, settingsBtn]

# Place them evenly using grid
for i, btn in enumerate(buttons):
    btn.grid(row=0, column=i, padx=10, sticky="ew")
    inner_frame.grid_columnconfigure(i, weight=1)

current_y = HEIGHT  # start hidden

toggle_btn = tk.Button(root, text="Toggle Taskbar")
toggle_btn.place(relx=0.5, y=HEIGHT, anchor="s")  # start at bottom

STEP_FACTOR = 0.25   # 0.2–0.3 is good
MIN_STEP = 1
DELAY = 5

def animate_to(target_y):
    global current_y

    def step():
        global current_y

        distance = target_y - current_y

        # Smooth easing movement
        move = int(distance * STEP_FACTOR)

        if abs(move) < MIN_STEP:
            move = MIN_STEP if distance > 0 else -MIN_STEP

        current_y += move

        # Clamp to target
        if abs(target_y - current_y) < 2:
            current_y = target_y

        root.update_idletasks()
        btn_height = toggle_btn.winfo_height()

        # Move taskbar
        x_pos = (WIDTH - BAR_WIDTH) // 2
        taskbar.place(x=x_pos, y=current_y, width=BAR_WIDTH, height=BAR_HEIGHT)

        # Move button
        if current_y >= HEIGHT:
            toggle_btn.place_configure(y=HEIGHT, anchor="s")
        else:
            toggle_btn.place_configure(y=current_y - btn_height, anchor="n")

        if current_y != target_y:
            root.after(DELAY, step)

    step()

def toggle_taskbar():
    if current_y >= HEIGHT:
        animate_to(HEIGHT - BAR_HEIGHT)  # open
    else:
        animate_to(HEIGHT)               # close

toggle_btn.config(command=toggle_taskbar)

root.mainloop()
#endregion

#region Music Player
#endregion

#region File Writer
#endregion

#region Weather App
#endregion

#region Web Scrapper
#endregion

#region Settings
#endregion

#region Runner
#endregion