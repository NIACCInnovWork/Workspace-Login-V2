import tkinter as tk
import datetime as dt

from user_interface.project_frame import ProjectFrame


class SignOutPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        # Create Visit Info Frame ##################################################
        visit_info_frame = tk.LabelFrame(self, text="User Info")

        user_name_label = tk.Label(visit_info_frame, text="Name:", width=10)
        user_name = tk.Label(visit_info_frame, relief="sunken", width=30)

        user_type_label = tk.Label(visit_info_frame, text="User Type:", width=10)
        user_type = tk.Label(visit_info_frame, relief="sunken", width=30)

        visit_start_time_label = tk.Label(visit_info_frame, text="Visit Start:", width=10)
        visit_start_time = tk.Label(visit_info_frame, width=30, relief="sunken")

        visit_end_time_label = tk.Label(visit_info_frame, text="Visit End:", width=10)
        visit_end_time = tk.Label(visit_info_frame, width=30, relief="sunken")

        user_name_label.grid(row=0, column=0)
        user_name.grid(row=0, column=1)

        user_type_label.grid(row=1, column=0)
        user_type.grid(row=1, column=1)

        visit_start_time_label.grid(row=0, column=2)
        visit_start_time.grid(row=0, column=3)

        visit_end_time_label.grid(row=1, column=2)
        visit_end_time.grid(row=1, column=3)

        visit_info_frame.pack()

        # Create Projects List Frame ###############################################
        projects_frame = tk.LabelFrame(self, text="Projects")

        projects = []
        first_project = ProjectFrame(projects_frame)

        first_project.pack()

        projects_frame.pack()

        # Create Button Menu Frame #################################################
        button_menu_frame = tk.LabelFrame(self, text="Menu")
        cancel_button = tk.Button(button_menu_frame, text="Cancel")
        cancel_button.grid(row=0, column=0)

        button_menu_frame.pack()

        self.grid(row=1, column=0, rowspan=4, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

        # date = dt.datetime.now()
        #
        # logged_in_title = tk.Label(self, text="User Sign Out", font=("Arial", 14))
        # logged_in_users = tk.Listbox(self, width=30, height=15)
        #
        # user_name_label = tk.Label(self, text="User Name:", padx=5)
        # user_name_entry = tk.Entry(self, width=30, state="disabled")
        #
        # visit_date_label = tk.Label(self, text="Visit DateTime:", padx=5)
        # visit_date_entry = tk.Entry(self, width=30)
        # visit_date_entry.insert(0, str(date))
        # visit_date_entry.config(state="disabled")
        #
        # visitor_type_label = tk.Label(self, text="Visitor Type:", padx=5)
        # visitor_type_entry = tk.Entry(self, width=30, state="disabled")
        #
        # equipment_used_label = tk.Label(self, text="Equipment Used:", padx=5)
        # fdm_3d_printer_checkbox = tk.Checkbutton(self, text="FDM 3D Printer")
        # sla_3d_printer_checkbox = tk.Checkbutton(self, text="SLA 3D Printer")
        # laser_cutter_checkbox = tk.Checkbutton(self, text="Laser Cutter")
        # vinyl_cutter_checkbox = tk.Checkbutton(self, text="Vinyl Cutter")
        # cnc_mill_checkbox = tk.Checkbutton(self, text="CNC Mill")
        # robotics_checkbox = tk.Checkbutton(self, text="Robotics")
        # electronics_checkbox = tk.Checkbutton(self, text="Electronics Bench")
        #
        # submit_sign_out_button = tk.Button(self, text="Sign Out", width=10)
        # cancel_sign_out_button = tk.Button(self, text="Cancel", width=10,
        #                                    command=lambda: controller.show_frame("MainPage"))
        #
        # # Place Objects
        # logged_in_title.grid(row=0, column=0)
        # logged_in_users.grid(row=1, column=0, rowspan=8, padx=10, pady=10)
        #
        # user_name_label.grid(row=1, column=1, sticky="E")
        # user_name_entry.grid(row=1, column=2, padx=(5, 20))
        #
        # visit_date_label.grid(row=2, column=1, sticky="E")
        # visit_date_entry.grid(row=2, column=2, padx=(5, 20))
        #
        # visitor_type_label.grid(row=3, column=1, sticky="E")
        # visitor_type_entry.grid(row=3, column=2, padx=(5, 20))
        #
        # equipment_used_label.grid(row=4, column=1, sticky="W")
        # fdm_3d_printer_checkbox.grid(row=4, column=2, sticky="W")
        # sla_3d_printer_checkbox.grid(row=5, column=2, sticky="W")
        # laser_cutter_checkbox.grid(row=6, column=2, sticky="W")
        # vinyl_cutter_checkbox.grid(row=7, column=2, sticky="W")
        # cnc_mill_checkbox.grid(row=8, column=2, sticky="W")
        # robotics_checkbox.grid(row=9, column=2, sticky="W")
        # electronics_checkbox.grid(row=10, column=2, sticky="W")
        #
        # submit_sign_out_button.grid(row=9, column=3, padx=10)
        # cancel_sign_out_button.grid(row=10, column=3, padx=10, pady=(0, 10))
        #
        # self.grid(row=1, column=0, rowspan=4, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
