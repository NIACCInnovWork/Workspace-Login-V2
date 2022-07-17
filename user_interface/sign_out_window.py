import tkinter as tk
import datetime as dt

import database.initialize_database
import user_interface.launch_gui
from controller.sign_out_controller import load_visit_data, signout_from_ui
from user_interface.ScrollingListFrame import ScrollingListFrame
from user_interface.project_frame import ProjectFrame


class SignOutPage(tk.Frame):

    def __init__(self, parent, controller, selected_user_name):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.controller = controller
        self.user_name = selected_user_name

        # Pull Data from Database
        self.visit_data = load_visit_data(selected_user_name)
        current_time = dt.datetime.now()

        # Create Visit Info Frame ##################################################
        visit_info_frame = tk.LabelFrame(self, text="User Info")

        user_name_label = tk.Label(visit_info_frame, text="Name:", width=10)
        self.user_name = tk.Label(visit_info_frame, text=self.visit_data[0], relief="sunken", width=30)

        user_type_label = tk.Label(visit_info_frame, text="User Type:", width=10)
        self.user_type = tk.Label(visit_info_frame, text=str(self.visit_data[1]), relief="sunken", width=30)

        visit_start_time_label = tk.Label(visit_info_frame, text="Visit Start:", width=10)
        self.visit_start_time = tk.Label(visit_info_frame, text=str(self.visit_data[2]), width=30, relief="sunken")

        visit_end_time_label = tk.Label(visit_info_frame, text="Visit End:", width=10)
        self.visit_end_time = tk.Label(visit_info_frame, text=str(current_time), width=30, relief="sunken")

        user_name_label.grid(row=0, column=0)
        self.user_name.grid(row=0, column=1)

        user_type_label.grid(row=1, column=0)
        self.user_type.grid(row=1, column=1)

        visit_start_time_label.grid(row=0, column=2)
        self.visit_start_time.grid(row=0, column=3)

        visit_end_time_label.grid(row=1, column=2)
        self.visit_end_time.grid(row=1, column=3)

        visit_info_frame.pack()

        # Create Projects List Frame ###############################################
        self.projects_list_frame = ScrollingListFrame(self, height=400)

        self.project_frames_list = []
        self.add_project()
        add_project_button = tk.Button(self.projects_list_frame, text="Add Another Project", command=self.add_project)

        add_project_button.pack()
        self.projects_list_frame.pack()

        # Create Button Menu Frame #################################################
        button_menu_frame = tk.LabelFrame(self, text="Menu")
        cancel_button = tk.Button(button_menu_frame, text="Cancel", command=self.return_to_main)
        submit_button = tk.Button(button_menu_frame, text="Submit", command=self.log_out_user)
        cancel_button.grid(row=0, column=0)
        submit_button.grid(row=0, column=1)

        button_menu_frame.pack()

        self.grid(row=1, column=0, rowspan=4, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

    def add_project(self):
        project = ProjectFrame(self.projects_list_frame.interior)
        project.on_remove(lambda: self.remove_project(project))
        self.project_frames_list.append(project)
        self.project_frames_list[-1].pack(padx=4, pady=4)

    def remove_project(self, project: ProjectFrame):
        self.project_frames_list.remove(project)
        project.destroy()

    def return_to_main(self):
        self.destroy()
        user_interface.launch_gui.MainPage(self.parent, self.controller)

    def log_out_user(self):
        signout_from_ui(self.visit_data[3])
        self.destroy()
        user_interface.launch_gui.MainPage(self.parent, self.controller)
