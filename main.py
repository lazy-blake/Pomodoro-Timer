from tkinter import Tk, Canvas, PhotoImage, Label, Button
import math
from PIL import Image, ImageTk

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
BLACK = "#333446"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
rep = 0
text = ""
timer = None


# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    window.after_cancel(timer)  # cancel the countdown if it's running
    checkmark_label.config(text="")
    title_label.config(text="Timer", fg=GREEN)
    canvas.itemconfig(timer_text, text="00:00")
    global rep
    rep = 0  # reset the repetition count


# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    # this function will be called when the start button is pressed
    # it will increment the repetition count and set the timer for work or break
    global rep
    rep += 1
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60
    work_sec = WORK_MIN * 60

    # check the current repetition count and set the countdown timer accordingly
    if rep % 8 == 0:
        # if the repetition count is a multiple of 8, it's a long break
        countdown(long_break_sec)
        title_label.config(text="Break", fg=RED)

    elif rep % 2 == 0:
        # if the repetition count is even, it's a short break
        countdown(short_break_sec)
        title_label.config(text="Break", fg=PINK)
    else:
        countdown(work_sec)
        title_label.config(text="Work", fg=GREEN)


# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def countdown(count):
    # This function will be called every second to update the timer
    # It will convert the count from seconds to minutes and seconds format
    minutes = math.floor(count / 60)  # remove all of the decimal values
    seconds = count % 60
    if seconds < 10:
        seconds = f"0{seconds}"  # ensure seconds are always two digits

    formatted_time = f"{minutes}:{seconds}"

    # Update the timer text on the canvas
    canvas.itemconfig(timer_text, text=formatted_time)

    if count > 0:
        global timer
        timer = window.after(1000, countdown, count - 1)
    elif count == 0:
        start_timer()  # Start the next timer after the current one ends
        if rep % 2 == 0:
            # If it's a break, update the checkmark label
            checkmark_label.config(text=checkmark_label["text"] + "✔")


# ------------------------------DARK MODE-------------------------------#
def toggle_dark_mode():
    if window.cget("bg") == YELLOW:
        # If the current background is yellow, switch to dark mode
        window.config(bg=BLACK)
        canvas.config(bg=BLACK)
        title_label.config(bg=BLACK)
        checkmark_label.config(bg=BLACK, fg=GREEN)
        mode_switch_button.config(bg=BLACK, image=dark_mode_img, highlightthickness=0)
    else:
        window.config(bg=YELLOW)
        canvas.config(bg=YELLOW)
        title_label.config(bg=YELLOW)
        checkmark_label.config(bg=YELLOW, fg=GREEN)
        mode_switch_button.config(bg=YELLOW, image=light_mode_img, highlightthickness=0)


# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)
window.geometry("500x400")  # adjust dimensions as needed


# creating title of the program
title_label = Label(
    text="Timer",
    fg=GREEN,
    bg=YELLOW,
    font=(FONT_NAME, 38, "bold"),
)
title_label.grid(column=1, row=0)

# creating a canvas to hold the image and timer text
canvas = Canvas(width=200, height=224, bg=YELLOW, highlightthickness=0)

# to get hold of the image file, we need to use PhotoImage class
canvas_image = PhotoImage(
    file="C:/Users/akash/OneDrive/Documents/Python/Projects/pomodoro_timer/tomato.png"
)

# to create an image at the center of the canvas with x,y coordinates
canvas.create_image(100, 112, image=canvas_image)
# to create the timer text on the canvas
timer_text = canvas.create_text(
    100, 130, text="00:00", fill="white", font=(FONT_NAME, 35, "bold")
)
canvas.grid(column=1, row=1)

# creating the buttons to start and reset the timer
start_button = Button(text="Start", command=start_timer)
start_button.config(font=(FONT_NAME, 10, "bold"))
start_button.grid(column=0, row=2)

reset_button = Button(text="Reset", command=reset_timer)
reset_button.config(font=(FONT_NAME, 10, "bold"))
reset_button.grid(column=2, row=2)

# creating the checkmark label to show completed work sessions
checkmark_label = Label(
    fg=GREEN,
    bg=YELLOW,
    font=(FONT_NAME, 12, "bold"),
)
checkmark_label.grid(column=1, row=3)

# creating a button to toggle dark mode
light_mode = Image.open(
    "C:/Users/akash/OneDrive/Documents/Python/Projects/pomodoro_timer/light_mode.png"
)
resized_img = light_mode.resize(
    (65, 30), Image.Resampling.LANCZOS
)  # Adjust these values to scale down
light_mode_img = ImageTk.PhotoImage(resized_img)


dark_mode = Image.open(
    "C:/Users/akash/OneDrive/Documents/Python/Projects/pomodoro_timer/dark_mode_2.png"
)
resized_img = dark_mode.resize(
    (65, 30), Image.Resampling.LANCZOS
)  # Adjust these values to scale down
dark_mode_img = ImageTk.PhotoImage(resized_img)

mode_switch_button = Button(
    image=light_mode_img,
    bd=0,
    command=toggle_dark_mode,
    bg=YELLOW,
    highlightthickness=0,
)
mode_switch_button.grid(column=3, row=0)

window.mainloop()
