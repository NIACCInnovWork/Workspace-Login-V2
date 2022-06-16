from tkinter import *
import datetime as dt

# Format the main window
root = Tk()  # Must come first because it defines the window
root.title('Innovation Workspace Login')  # Create title of the window

workspaceLogo = PhotoImage(file='Innovation Workspace Logo-Official-Scaled.png')  # Import Logo
logoLabel = Label(root, image=workspaceLogo)  # Place Logo into a Label

# Implement Datetime
date = dt.datetime.now()


def open_sign_in():  # Function to open sign in window
    sign_in_window = Toplevel(root)
    sign_in_window.geometry("750x250")
    sign_in_window.title("Sign In Window")

    # Crete Objects
    sign_in_window_title_label = Label(sign_in_window, text="Sign In", font=("Arial", 14), pady=10)
    users_list_box = Listbox(sign_in_window)
    user_name_label = Label(sign_in_window, text="User Name", padx=5)
    user_name_entry = Entry(sign_in_window, state='disabled')

    visit_date_label = Label(sign_in_window, text="Visit DateTime", padx=5)
    visit_date_entry = Entry(sign_in_window)
    visit_date_entry.insert(END, date)

    # Place Objects
    sign_in_window_title_label.grid(row=0, column=0, columnspan=2)
    users_list_box.grid(row=1, column=0, rowspan=3)

    user_name_label.grid(row=1, column=1)
    user_name_entry.grid(row=1, column=2)

    visit_date_label.grid(row=2, column=1)
    visit_date_entry.grid(row=2, column=2)


def open_new_user():  # Function to open new user window
    new_user_window = Toplevel(root)
    new_user_window.title("New User Window")

    # Create objects
    new_user_window_title_label = Label(new_user_window, text="Enter the information below to create a new user",
                                        font=("Arial", 14), pady=10)
    name_entry_label = Label(new_user_window, text="Full Name", pady=5)
    name_entry = Entry(new_user_window)

    is_student_checkbox = Checkbutton(new_user_window, text='Student')
    is_entrepreneur_checkbox = Checkbutton(new_user_window, text='Entrepreneur')
    is_community_checkbox = Checkbutton(new_user_window, text='Community Member')

    submit_new_user_button = Button(new_user_window, text='Submit New User')

    # Place objects
    new_user_window_title_label.grid(row=0, column=0, columnspan=3)
    name_entry_label.grid(row=1, column=0)
    name_entry.grid(row=1, column=1)
    is_student_checkbox.grid(row=2, column=0)
    is_entrepreneur_checkbox.grid(row=2, column=1)
    is_community_checkbox.grid(row=2, column=2)
    submit_new_user_button.grid(row=3, column=1)


def open_sign_out():  # Function to open sign out window
    sign_out_window = Toplevel(root)
    sign_out_window.geometry("750x250")
    sign_out_window.title("Sign Out Window")

    logged_in_title = Label(sign_out_window, text="Sign Out Here")
    logged_in_users = Listbox(sign_out_window)

    logged_in_title.grid(row=0, column=0, columnspan=2)
    logged_in_users.grid(row=1, column=0)


# Creating buttons for the main page
signInButton = Button(root, text="Sign In", font=("Arial", 14),
                      height=5, width=20, command=open_sign_in)  # Creating Sign In Button
newUserButton = Button(root, text="New User", font=("Arial", 14),
                       height=5, width=20, command=open_new_user)  # Creating New User Button
signOutButton = Button(root, text="Sign Out", font=("Arial", 14),
                       height=5, width=20, command=open_sign_out)  # Creating Sign Out Button


# Placing Objects on Screen
logoLabel.grid(row=0, column=0, columnspan=3)
signInButton.grid(row=1, column=0)
newUserButton.grid(row=1, column=1)
signOutButton.grid(row=1, column=2)

root.mainloop()  # Creating an event loop
