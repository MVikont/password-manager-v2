import tkinter
from tkinter import *
from tkinter import messagebox
import random
import pyperclip
import json

FONT = ("Arial", 7)

BG = "white"
#PASSWORD GENERATOR
chars = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U',
'V', 'W', 'X', 'Y', 'Z'
,'0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '!', '#', '$', '%', '&', '(', ')', '*', '+']

def gen_pass():
    pass_field.delete(0, END)
    nr_chars = random.randint(12,18)
    password = [random.choice(chars) for c in range(nr_chars)]
    random.shuffle(password)
    password_h = "".join(password)
    pass_field.insert(0, password_h)
    # messagebox.showinfo(title="Password Generated.", message="Password successfully generated\nand copied to Clipboard.")
    pyperclip.copy(password_h)


#SAVE DATA
def save_data():
    website = website_field.get().title()
    email = email_field.get()
    password = pass_field.get()
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(email) < 1 or len(website) < 1 or len(password) < 1:
        messagebox.showerror(title="Oops!", message="Please fill in required fields.")
    else:
        try:
            with open("data.json", mode="r") as info:
                content = json.load(info)
                content.update(new_data)
        except FileNotFoundError:
            with open("data.json", mode="w") as info:
                json.dump(new_data, info, indent=4)
                messagebox.showinfo(title="Success", message="Data added successfully.")
        else:
            with open("data.json", mode="w") as info:
                json.dump(content, info, indent=4)
                messagebox.showinfo(title="Success", message="Data added successfully.")
        finally:
            website_field.delete(0, END)
            pass_field.delete(0, END)


#SET UP DATABASE WINDOW
def db_window():
    webl = []
    try:
        with open("data.json", mode="r") as sitedb:
            sites = json.load(sitedb)

    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="No database found.")

    else:
        db = Toplevel()
        db.title("Password Database")
        db.config(padx=25, pady=25)

        def show_credentials(event):
            try:
                sel = weblist.get(weblist.curselection())
                cred_label = Label(db, font=FONT, width=30, text=f'''
Login for {sel}:\n
Email/Username: {sites[sel]["email"]}
Password: {sites[sel]["password"]}''')
            except tkinter.TclError:
                pass
            else:
                cred_label.grid(column=5, row=2)

        def remove_entry():
            if weblist.size() == 0:
                pass
            else:
                do_remove = messagebox.askyesno(title="Delete Entry", message="Delete entry?")
                if do_remove == False:
                    pass
                else:
                    new_data = {}
                    current_sel = weblist.get(weblist.curselection())
                    with open("data.json", mode="r") as file:
                        all = json.load(file)
                        for platform in all:
                            if platform != current_sel:
                                new_data[platform] = all[platform]
                    with open("data.json", mode="w") as file:
                        json.dump(new_data, file, indent=4)
                    weblist.delete(weblist.curselection())

        def clear_db():
            if weblist.size() == 0:
                pass
            else:
                do_clear = messagebox.askyesno(title="Clear Database", message='''This will clear the entire Database.
This action cannot be undone.\n
Are you sure you wish to proceed?''')
                if do_clear == False:
                    pass
                else:
                    new_data = {}
                    with open("data.json", mode="w") as file:
                        json.dump(new_data, file, indent=4)
                    weblist.delete(0, END)
                    messagebox.showinfo(title="Success", message="Database cleared.")
                    exit_db()

        def exit_db():
            db.destroy()

        def copy_password():
            try:
                sel = weblist.get(weblist.curselection())
                with open("data.json", mode="r") as file:
                    data = json.load(file)
                    password = data[sel]["password"]
            except tkinter.TclError:
                pass
            else:
                pyperclip.copy(password)
                messagebox.showinfo(title="Copy Successful", message="Password copied to Clipboard.")
                exit_db()
                db_window()

        weblist = Listbox(db)
        weblist.bind("<<ListboxSelect>>", show_credentials)
        weblist.grid(column=0, row=2)

        delete_entry = Button(db, text="Delete Entry", width=10, font=FONT, command=remove_entry)
        delete_entry.grid(column=0, row=4)
        copypass = Button(db, text="Copy Password", width=10, font=FONT, command=copy_password)
        copypass.grid(column=0, row=3)
        clear_database = Button(db, text="Clear Database", width=10, font=FONT, command=clear_db)
        clear_database.grid(column=0, row=5)
        exit_db_button = Button(db, text="Exit", width=5, font=FONT, command=exit_db)
        exit_db_button.grid(column=0, row=6)

        for website in sites:
            webl.append(website)
        for w in webl:
            weblist.insert(webl.index(w), w)


def exit_program():
    win.destroy()

def find_password():
    try:
        with open("data.json", "r") as data_file:
            d = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Oops", message="No data file found.")
    else:
        current_website = website_field.get().title()
        for website_name in d:
            if current_website == website_name:
                messagebox.showinfo(title="Success", message=f'''
The credentials for {website_name}:\n
Email: {d[website_name]["email"]}
Password: {d[website_name]["password"]}''')
                return None

        if len(current_website) == 0:
            messagebox.showinfo(title="Oops", message="Please enter platform name.")
        else:
            messagebox.showinfo(title="Oops", message=f"No details for {current_website}.")

    finally:
        website_field.delete(0, END)

#SET UP MAIN WINDOW
win = Tk()
win.title("MyPass Password Manager")
win.config(padx=20, pady=20, bg="white")

canvas = Canvas(width=200, height=200, bg="white", highlightthickness=0)
lock = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=lock)
canvas.grid(column=1, row=0)

website_label = Label(text="Platform:", font=FONT, bg=BG)
website_label.grid(column=0, row=1)
email_label = Label(text="Email/UN:", font=FONT, bg=BG)
email_label.grid(column=0, row=2)
pass_label = Label(text="Password:", font=FONT, bg=BG)
pass_label.grid(column=0, row=3)

website_field = Entry(width=25)
website_field.focus()
website_field.grid(column=1, row=1)
email_field = Entry(width=25)
email_field.insert(0, "marksh100195@gmail.com")
email_field.grid(column=1, row=2)
pass_field = Entry(width=25)
pass_field.grid(column=1, row=3)

genpass = Button(text="Generate Password", width=14, font=FONT, command=gen_pass)
genpass.grid(column=2, row=3)
add = Button(text="Add",font=FONT, width=30, command=save_data)
add.grid(column=1, row=4, columnspan=2)
off = Button(text="Exit", width=9, font=FONT, command=exit_program)
off.grid(column=0, row=6)
search = Button(text="Search Platform", width=15, font=FONT, command=db_window)
search.grid(column=2, row=1)

win.mainloop()