from tkinter import *
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
current_card = {}
to_learn = {}

# Load data
try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    original_data = pandas.read_csv("french_words.csv")
    to_learn = original_data.to_dict(orient="records")
else:
    to_learn = data.to_dict(orient="records")

def next_card():
    global current_card
    current_card = random.choice(to_learn)
    canvas.itemconfig(card_title, text="French", fill="black")
    canvas.itemconfig(card_word, text=current_card["French"], fill="black")
    canvas.itemconfig(card_background, image=card_front_img)

def flip_card():
    canvas.itemconfig(card_background, image=card_back_img)
    canvas.itemconfig(card_title, text="English", fill="white")
    canvas.itemconfig(card_word, text=current_card["English"], fill="white")

def open_input_dialog():
    input_window = Toplevel(window)
    input_window.title("Answer the question")
    input_window.config(padx=20, pady=20, bg=BACKGROUND_COLOR)
    input_window.resizable(False, False)  # Disable resizing for the input dialog window

    input_label = Label(input_window, text="Type your answer:", font=("Arial", 14), bg=BACKGROUND_COLOR)
    input_label.pack()

    user_input = Entry(input_window, width=30)
    user_input.pack()

    def check_answer():
        if user_input.get().lower() == current_card["English"].lower():
            correct_label = Label(input_window, text="Correct!", font=("Arial", 14), fg="green", bg=BACKGROUND_COLOR)
            correct_label.pack()
            input_window.after(1000, input_window.destroy)
            is_known()
        else:
            wrong_label = Label(input_window, text="Wrong answer!", font=("Arial", 14), fg="red", bg=BACKGROUND_COLOR)
            wrong_label.pack()
            Button(input_window, text="Try Again", command=lambda: (wrong_label.destroy(), user_input.delete(0, END))).pack()
            Button(input_window, text="Show Answer", command=lambda: show_answer(input_window)).pack()

    submit_button = Button(input_window, text="Submit", command=check_answer)
    submit_button.pack()

def show_answer(input_window):
    input_window.destroy()
    flip_card()
    window.after(5000, next_card)  # After 5 seconds, move to the next French card

def is_known():
    to_learn.remove(current_card)
    data = pandas.DataFrame(to_learn)
    data.to_csv("words_to_learn.csv", index=False)
    next_card()

# Set up the main window
window = Tk()
window.title("FlashCard")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
window.geometry("900x700")  # Set initial size
window.resizable(False, False)  # Disable window resizing for the main window

# Set up the canvas
canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="card_front.png")
card_back_img = PhotoImage(file="card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 30, "normal"))
canvas.grid(row=0, column=0, columnspan=2)

# Set up the buttons
cross_image = PhotoImage(file="wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_card)
unknown_button.grid(row=1, column=0)

check_image = PhotoImage(file="right.png")
known_button = Button(image=check_image, highlightthickness=0, command=open_input_dialog)
known_button.grid(row=1, column=1)

next_card()

window.mainloop()

