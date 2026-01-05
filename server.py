from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle, sample


import json

def create_password():
    """Generate a password based on spinbox selections and insert it in the password entry."""
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
               'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    capital_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                       'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+', '^', '{', '}', '[', ']', '/', '<', '>', '.', ',']

    #define number of items to include based on user choice
    pwd_numbers = sample(numbers, int(number_spinbox.get()))
    pwd_lowcase_letters = sample(letters, int(lowcase_letter_spinbox.get()))
    pwd_capital_letters = sample(capital_letters, int(capital_letters_spinbox.get()))
    pwd_symbols = sample(symbols, int(symbol_spinbox.get()))

    pwd_list = pwd_numbers + pwd_lowcase_letters + pwd_symbols + pwd_capital_letters
    shuffle(pwd_list)
    # add the password in the password entry widget
    password = "".join(pwd_list)
    pwd_entry.insert(0, password)


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
                #Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("credentials.json", "w") as data_file:
                json.dump(credentials, data_file, indent=4)
        else:
            #Updating old data with new data
            data.update(credentials)

            with open("credentials.json", "w") as data_file:
                #Saving updated data
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            pwd_entry.delete(0, END)
            email_entry.delete(0, END)




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

#build GUI

#window
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

#canvas
canvas = Canvas(width=200, height=300)
#image = PhotoImage(file="logo.png")
#canvas.create_image(100, 150, image=image)
image = PhotoImage(file="png-clipart.png")
canvas.create_image(100, 100, image=image)
canvas.grid(row=0, column=0, columnspan=4)

#labels
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

#entries
website_entry = Entry(width=45)
website_entry.grid(row=5, column=1, columnspan=2)
website_entry.focus()

email_entry = Entry(width=45)
email_entry.grid(row=6, column=1, columnspan=2)

pwd_entry = Entry(width=35)
pwd_entry.grid(row=7, column=1)

#buttons
search_button = Button(text="Search", width=10, command=find_password)
search_button.grid(row=5, column=3)

create_pswd_button = Button(text="Create pswd", command=create_password)
create_pswd_button.grid(row=7, column=3)

add_button = Button(text="Add", width=36, command=save_credentials, font=("Arial", 12), activebackground="green")
add_button.grid(row=8, column=1, columnspan=2)

#spinbox
capital_letters_spinbox = Spinbox(from_=4, to=10, width=5)
capital_letters_spinbox.grid(row=1, column=1)

lowcase_letter_spinbox = Spinbox(from_=4, to=10, width=5)
lowcase_letter_spinbox.grid(row=2, column=1)

symbol_spinbox = Spinbox(from_=2, to=8, width=5)
symbol_spinbox.grid(row=3, column=1)

number_spinbox = Spinbox(from_=2, to=8, width=5)
number_spinbox.grid(row=4, column=1)

#window showup
window,mainloop()
