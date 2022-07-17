"""
NIACC Innovation Workspace Login V2
File that defines the layout and behavior of the Sign In window.
Author: Anthony Riesen
"""
import tkinter as tk
import datetime as dt
from PIL import Image, ImageTk
from database.class_user import User
from database.initialize_database import start_workspace_database
from controller.sign_in_controller import create_visit_from_ui
import user_interface.launch_gui


class SignInPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller

        # date = dt.datetime.now()

        # Create Users Listbox Frame ##############################################################
        users_frame = tk.LabelFrame(self, text="All Users")

        # Pull Data
        database = start_workspace_database()
        user_list = User.get_all_visitors(database)

        # Create listbox & scrollbar
        user_scrollbar = tk.Scrollbar(users_frame, orient="vertical")
        users_list_box = tk.Listbox(users_frame, yscrollcommand=user_scrollbar.set, height=15)

        # Populate listbox
        for name in user_list:
            users_list_box.insert(user_list.index(name), name[0])

        # Configure & pack listbox/scrollbar
        user_scrollbar.config(command=users_list_box.yview)
        user_scrollbar.pack(side="right", fill=tk.Y)
        users_list_box.pack(side="left", fill="both", expand=1)

        users_frame.grid(row=0, column=0, rowspan=2, padx=10, pady=10)

        # Create Header Frame ##############################################################
        header_frame = tk.LabelFrame(self, text="header")

        page_title = tk.Label(header_frame, text="Sign In", font=controller.title_font)

        # Resize and place logo
        base_width = 300
        photo = (Image.open(r"resources/Innovation Workspace Logo-Official-Scaled.png"))
        width_percent = (base_width/float(photo.size[0]))
        height_size = int((float(photo.size[1])*float(width_percent)))
        resized_photo = photo.resize((base_width, height_size), Image.ANTIALIAS)
        new_photo = ImageTk.PhotoImage(resized_photo)
        header_frame.photo = new_photo
        canvas = tk.Canvas(header_frame, width=base_width, height=height_size)
        canvas.create_image(10, 10, anchor=tk.NW, image=header_frame.photo)
        canvas.pack()
        page_title.pack()

        header_frame.grid(row=0, column=1, columnspan=2)

        # Create User Info Frame ############################################################
        user_info_frame = tk.LabelFrame(self, text="info")

        user_name_label = tk.Label(user_info_frame, text="User Name:", padx=5)
        user_name_entry_label = tk.Label(user_info_frame, width=30, relief="sunken")

        visit_date_label = tk.Label(user_info_frame, text="Visit DateTime:", padx=5)
        visit_date_entry_label = tk.Label(user_info_frame, width=30, relief="sunken")

        user_type_label = tk.Label(user_info_frame, text="Visitor Type:", padx=5)
        user_type_entry_label = tk.Label(user_info_frame, width=30, relief="sunken")

        user_name_label.grid(row=1, column=1, sticky="E")
        user_name_entry_label.grid(row=1, column=2, padx=(5, 20))

        visit_date_label.grid(row=2, column=1, sticky="E")
        visit_date_entry_label.grid(row=2, column=2, padx=(5, 20))

        user_type_label.grid(row=3, column=1, sticky="E")
        user_type_entry_label.grid(row=3, column=2, padx=(5, 20))

        user_info_frame.grid(row=1, column=1)

        # Create Function to update user info based on selection ##########
        def callback(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                selected_name = event.widget.get(index)
                user = User.load(database, selected_name)
                user_name_entry_label.configure(text=user.name)
                user_type_entry_label.configure(text=user.user_type)
                visit_date_entry_label.configure(text=str(dt.datetime.now()))
            else:
                user_name_label.configure(text="")

        users_list_box.bind("<<ListboxSelect>>", callback)

        # Create function for start visit label
        def sign_in_button():
            selected_name = users_list_box.get(users_list_box.curselection())
            user = User.load(database, selected_name)
            print(user.user_id)
            visit = create_visit_from_ui(user.user_id)
            self.return_to_main()

        # Create Button Frame #############################################
        button_frame = tk.LabelFrame(self, text="buttons")

        submit_sign_in_button = tk.Button(button_frame, text="Sign In", width=10,
                                          command=sign_in_button)
        cancel_sign_in_button = tk.Button(button_frame, text="Cancel", width=10,
                                          command=self.return_to_main)

        submit_sign_in_button.grid(row=8, column=3, padx=10)
        cancel_sign_in_button.grid(row=9, column=3, padx=10, pady=(0, 10))

        button_frame.grid(row=1, column=2)

        self.grid(row=1, column=0, rowspan=4, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

    def return_to_main(self):
        self.destroy()
        user_interface.launch_gui.MainPage(self.parent, self.controller)
