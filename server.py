from tkinter import *
from tkinter import messagebox
from random import shuffle, sample
import json


def create_password():
    """
    Generate a password based on spinbox selections and insert it in the password entry.
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                       'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '^', '{', '}', '[', ']', '/', '<', '>', '.', ',']

    # define number of items to include based on user choice
    pwd_numbers = sample(numbers, int(number_spinbox.get()))
    pwd_lowcase_letters = sample(letters, int(lowcase_letter_spinbox.get()))
    pwd_capital_letters = sample(capital_letters, int(capital_letters_spinbox.get()))
    pwd_symbols = sample(symbols, int(symbol_spinbox.get()))

    pwd_list = pwd_numbers + pwd_lowcase_letters + pwd_symbols + pwd_capital_letters
    shuffle(pwd_list)

    #insert the password in the password entry widget (clear first so it doesn't append)
    password = "".join(pwd_list)
    pwd_entry.delete(0, END)
    pwd_entry.insert(0, password)

    #after generating, update strength indicator for the user
    update_strength_label()


def save_credentials():
    """Save website/email/password to credentials.json as a nested dict keyed by website."""
    website = website_entry.get()
    email = email_entry.get()
    pwd = pwd_entry.get()

    credentials = {
        website: {
            "email": email,
            "password": pwd,
        }
    }

    if website == "" or pwd == "":
        messagebox.showinfo(title="Warning!", message="Fill in all fields.")
    else:
        try:
            with open("credentials.json", "r") as data_file:
                #reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("credentials.json", "w") as data_file:
                json.dump(credentials, data_file, indent=4)
        else:
            #updating old data with new data
            data.update(credentials)
            with open("credentials.json", "w") as data_file:
                #saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            pwd_entry.delete(0, END)
            email_entry.delete(0, END)
            # Also reset the strength label when fields are cleared
            strength_value_label.config(text="")


def find_password():
    """Lookup credentials by website and display them in a messagebox."""
    website = website_entry.get()
    try:
        with open("credentials.json") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error!", message="Data file not found.")
    else:
        if website in data:
            email = data[website]["email"]
            pwd = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email: {email}\nPassword: {pwd}")
        else:
            messagebox.showinfo(title="Error", message=f"{website} already on file.")


def show_password():
    """
    Show or hide (*) the password characters.
    """
    if show_password_var.get():
        #show password text
        pwd_entry.config(show="")
    else:
        #hide password text
        pwd_entry.config(show="*")


def pswd_strength(password_text):
    """
    Password strength check.
    Returns two things: the text to show (Weak/Medium/Strong)
    and the color to display.
    Score concept:
    +1 if the password is at least 8 characters long
    +1 if it has a lowercase letter
    +1 if it has an uppercase letter
    +1 if it has a number
    +1 if it has a symbol.
    Final score meaning:
    0–1 = Weak
    2–3 = Medium
    4–5 = Strong

    """
    score = 0

    #length check
    if len(password_text) >= 8:
        score += 1

    #lowercase character checks
    has_lower = False
    for char in password_text:
        if char.islower():
            has_lower = True
            break

    #uppercase character checks
    has_upper = False
    for char in password_text:
        if char.isupper():
            has_upper = True
            break

    #digit checks
    has_digit = False
    for char in password_text:
        if char.isdigit():
            has_digit = True
            break

    #symbol check
    has_symbol = False
    for char in password_text:
        if not char.isalnum():
            has_symbol = True
            break

    if has_lower:
        score += 1
    if has_upper:
        score += 1
    if has_digit:
        score += 2
    if has_symbol:
        score += 2

    #map score to label plus color
    if score <= 4:
        return ("Weak", "red")
    elif score <= 6:
        return ("Medium", "orange")
    else:
        return ("Strong", "green")

#optional parameter allows this to be used as a key binding callback
#https://stackoverflow.com/questions/33283903/how-can-i-prevent-tkinter-from-passing-the-event-object-in-a-binding-is-there-a
def update_strength_label(event=None): #optional parameter
    """
    Update the strength label when the password changes.

    """
    pwd = pwd_entry.get()
    if pwd == "":
        strength_value_label.config(text="", fg="black")
        return

    label_text, color = pswd_strength(pwd)
    strength_value_label.config(text=label_text, fg=color)


def copy_password_to_clipboard():
    """
    Copy the current password to the system clipboard using TK built in clipboard.
    Also show confirmation so the user knows it worked.
    """
    pwd = pwd_entry.get()
    if pwd.strip() == "":
        messagebox.showinfo("Copy", "No password to copy.")
        return

    #clear the clipboard and append the new text
    window.clipboard_clear()
    window.clipboard_append(pwd)

    #update the Tk window to ensure clipboard content persistance
    window.update()

    messagebox.showinfo("Copy", "Password copied to clipboard.")


# window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

# canvas
canvas = Canvas(width=200, height=300)
# image = PhotoImage(file="logo.png")
# canvas.create_image(100, 150, image=image)
image = PhotoImage(file="png-clipart.png")
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=0, columnspan=4)

# labels
capital_letter_label = Label(text="Max capital letters? (min 4)")
capital_letter_label.grid(row=1, column=0)

lowcase_letter_label = Label(text="Max low case letters? (min 4)")
lowcase_letter_label.grid(row=2, column=0)

symbol_label = Label(text="Max symbols? (min 2)")
symbol_label.grid(row=3, column=0)

number_label = Label(text="Max numbers? (min 2)")
number_label.grid(row=4, column=0)

website_label = Label(text="Website:")
website_label.grid(row=5, column=0)

email_label = Label(text="Email:")
email_label.grid(row=6, column=0)

pwd_label = Label(text="Pswd:")
pwd_label.grid(row=7, column=0)

# entries
website_entry = Entry(width=45)
website_entry.grid(row=5, column=1, columnspan=2)
website_entry.focus()

email_entry = Entry(width=45)
email_entry.grid(row=6, column=1, columnspan=2)

pwd_entry = Entry(width=35)
pwd_entry.grid(row=7, column=1)

#hide password by default
pwd_entry.config(show="*")

# buttons
search_button = Button(text="Search", width=10, command=find_password)
search_button.grid(row=5, column=3)

create_pswd_button = Button(text="Create pswd", command=create_password)
create_pswd_button.grid(row=7, column=3)

add_button = Button(text="Add", width=36, command=save_credentials, font=("Arial", 12), activebackground="green")
add_button.grid(row=8, column=1, columnspan=2)

copy_button = Button(text="Copy", width=10, command=copy_password_to_clipboard)
copy_button.grid(row=7, column=2)

# spinboxes
capital_letters_spinbox = Spinbox(from_=4, to=10, width=5)
capital_letters_spinbox.grid(row=1, column=1)

lowcase_letter_spinbox = Spinbox(from_=4, to=10, width=5)
lowcase_letter_spinbox.grid(row=2, column=1)

symbol_spinbox = Spinbox(from_=2, to=8, width=5)
symbol_spinbox.grid(row=3, column=1)

number_spinbox = Spinbox(from_=2, to=8, width=5)
number_spinbox.grid(row=4, column=1)

#show/hide checkbox
show_password_var = BooleanVar(value=False)  # False -> hidden by default
show_checkbox = Checkbutton(text="Show", variable=show_password_var, command=show_password)
show_checkbox.grid(row=8, column=0)

strength_title_label = Label(text="Strength:")
strength_title_label.grid(row=9, column=0)

strength_value_label = Label(text="", fg="black")  # will be updated as user types
strength_value_label.grid(row=9, column=1, columnspan=2, sticky="w")

#key release is binded on password entry to update strength while typing
pwd_entry.bind("<KeyRelease>", update_strength_label)

# window showup
window.mainloop()