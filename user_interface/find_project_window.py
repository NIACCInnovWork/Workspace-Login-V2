"""
NIACC Innovation Workspace Login V2
File that defines the layout and behavior of the popup window where users can search for existing projects to which to
add their current visit.
Author: Anthony Riesen
"""

import tkinter as tk
from tkinter import font as tkfont


class FindProjectWindow(tk.Toplevel):

    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent

        self.title("Find Existing Project")
        title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        label = tk.Label(self, text="Find Your Project", font=title_font)
        project_frame = tk.LabelFrame(self, text="Your Projects")

        # Create listbox & scrollbar
        project_scrollbar = tk.Scrollbar(project_frame, orient="vertical")
        project_list_box = tk.Listbox(project_frame, yscrollcommand=project_scrollbar, height=15)

        # Configure and Grid listbox/scrollbar
        project_scrollbar.config(command=project_list_box.yview)
        project_scrollbar.pack(side="right", fill=tk.Y)
        project_list_box.pack(side="left", fill="both", expand=1)

        # Create Project Info Frame
        project_info_frame = tk.LabelFrame(self, text="Project Info")

        project_name_label = tk.Label(project_info_frame, text="Project Name:", padx=5)
        project_name_info_label = tk.Label(project_info_frame, width=60, relief="sunken")

        project_description_label = tk.Label(project_info_frame, text="Project Description:", padx=5)
        project_description_info_label = tk.Label(project_info_frame, width=60, relief="sunken")

        project_type_label = tk.Label(project_info_frame, text="Project Type:", padx=5)
        project_type_info_label = tk.Label(project_info_frame, width=60, relief="sunken")

        select_button = tk.Button(project_info_frame, text="Select Project")
        cancel_button = tk.Button(project_info_frame, text="Cancel")

        project_name_label.grid(row=0, column=0, sticky="E")
        project_name_info_label.grid(row=0, column=1, sticky="W")

        project_description_label.grid(row=1, column=0, sticky="E")
        project_description_info_label.grid(row=1, column=1, sticky="W")

        project_type_label.grid(row=2, column=0, sticky="E")
        project_type_info_label.grid(row=2, column=1, sticky="W")

        cancel_button.grid(row=3, column=0, pady=10, sticky="E")
        select_button.grid(row=3, column=1, pady=10, sticky="W")

        # Create View All Projects Button
        view_all_projects_button = tk.Button(self, text="View All Projects")

        project_frame.grid(row=0, column=0, rowspan=3)
        label.grid(row=1, column=1)
        project_info_frame.grid(row=2, column=1)
        view_all_projects_button.grid(row=3, column=0)
