from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json

# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    password_entry.delete(0, END)
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = [choice(letters) for c in range(randint(8, 10))]
    password_list += [choice(symbols) for c in range(randint(2, 4))]
    password_list += [choice(numbers) for c in range(randint(2, 4))]
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save():
    website = website_entry.get().capitalize()
    email = email_user_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Uh Oh!", message="No empty fields, Please!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)  # Read old data
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)  # Create json file & save new data
        else:
            data.update(new_data)  # Update old data w/ new data
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)  # Save updated data
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)
            website_entry.focus()


# -------- GET PASSWORD FROM JSON FILE ------- #
def find_password():
    search_entry = website_entry.get().capitalize()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="File Not Found")
    else:
        if search_entry in data:
            email = data[search_entry]["email"]
            password = data[search_entry]["password"]
            messagebox.showinfo(title=search_entry,
                                message=f"Email/Username: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"{search_entry} doesn't exist.")
    finally:
        website_entry.delete(0, END)
        website_entry.focus()


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(pady=40, padx=40)

canvas = Canvas(width=200, height=200)
mypass_pic = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=mypass_pic)
canvas.grid(column=1, row=0)

# Labels
website_label = Label(text="Website:", font=("Arial", 10, "normal"))
website_label.grid(column=0, row=1)
website_label.config(pady=5)
email_user_label = Label(text="Email/Username:", font=("Arial", 10, "normal"))
email_user_label.grid(column=0, row=2)
email_user_label.config(pady=5)
password_label = Label(text="Password:", font=("Arial", 10, "normal"))
password_label.grid(column=0, row=3)
password_label.config(pady=10)

# Entry areas
website_entry = Entry(width=30)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_user_entry = Entry(width=50)
email_user_entry.grid(column=1, row=2, columnspan=2)
email_user_entry.insert(0, "djnardone@email.com")
password_entry = Entry(width=30)
password_entry.grid(column=1, row=3)

# Buttons
gen_pass_button = Button(text="Generate Password", width=15, command=generate_password)
gen_pass_button.grid(column=2, row=3)
add_button = Button(text="Add", width=36, command=save)
add_button.grid(column=1, row=4, columnspan=2)
add_button.config(pady=2)
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()


