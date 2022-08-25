"""
NIACC Innovation Workspace Login V2
File that defines the layout and behavior of the popup window where users can search for existing projects to which to
add their current visit.
Author: Anthony Riesen
"""

import tkinter as tk
from tkinter import font as tkfont

from database.class_project import Project, ProjectType
from database.initialize_database import start_workspace_database


class FindProjectWindow(tk.Toplevel):

    def __init__(self, parent, user_id):
        tk.Toplevel.__init__(self, parent)
        self.parent = parent
        self.user_id = user_id

        self.title("Find Existing Project")
        title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")

        # Start Database Connection
        self.database = start_workspace_database()

        label = tk.Label(self, text="Find Your Project", font=title_font)
        project_frame = tk.LabelFrame(self, text="Your Projects")

        # Create listbox & scrollbar
        project_scrollbar = tk.Scrollbar(project_frame, orient="vertical")
        self.project_list_box = tk.Listbox(project_frame, yscrollcommand=project_scrollbar, height=15)

        # Configure and Grid listbox/scrollbar
        project_scrollbar.config(command=self.project_list_box.yview)
        project_scrollbar.pack(side="right", fill=tk.Y)
        self.project_list_box.pack(side="left", fill="both", expand=1)

        # Populate listbox
        self.project_list = []
        self.selected_project = Project.factory("", "", ProjectType["Personal"])
        self.load_my_projects()

        # Create Project Info Frame
        project_info_frame = tk.LabelFrame(self, text="Project Info")

        project_name_label = tk.Label(project_info_frame, text="Project Name:", padx=5)
        project_name_info_label = tk.Label(project_info_frame, width=60, relief="sunken")

        project_description_label = tk.Label(project_info_frame, text="Project Description:", padx=5)
        project_description_info_label = tk.Label(project_info_frame, width=60, relief="sunken")

        project_type_label = tk.Label(project_info_frame, text="Project Type:", padx=5)
        project_type_info_label = tk.Label(project_info_frame, width=60, relief="sunken")

        select_button = tk.Button(project_info_frame, text="Select Project", command=self.return_selected_project)
        cancel_button = tk.Button(project_info_frame, text="Cancel", command=self.close_window)

        project_name_label.grid(row=0, column=0, sticky="E")
        project_name_info_label.grid(row=0, column=1, sticky="W")

        project_description_label.grid(row=1, column=0, sticky="E")
        project_description_info_label.grid(row=1, column=1, sticky="W")

        project_type_label.grid(row=2, column=0, sticky="E")
        project_type_info_label.grid(row=2, column=1, sticky="W")

        cancel_button.grid(row=3, column=0, pady=10, sticky="E")
        select_button.grid(row=3, column=1, pady=10, sticky="W")

        # Create View All Projects Button
        view_all_projects_button = tk.Button(self, text="View All Projects", command=self.load_all_projects)

        project_frame.grid(row=0, column=0, rowspan=3)
        label.grid(row=1, column=1)
        project_info_frame.grid(row=2, column=1)
        view_all_projects_button.grid(row=3, column=0)

        def callback(event):
            selection = event.widget.curselection()
            if selection:
                index = selection[0]
                selected_project_id = self.project_list[index][0]
                self.selected_project = Project.load(self.database, selected_project_id)
                project_name_info_label.configure(text=self.selected_project.project_name, anchor=tk.W)
                project_description_info_label.configure(text=self.selected_project.project_description, anchor=tk.W)
                project_type_info_label.configure(text=self.selected_project.project_type, anchor=tk.W)
            else:
                project_name_info_label.configure(text="")
                project_description_info_label.configure(text="")
                project_type_info_label.configure(text="")

        self.project_list_box.bind("<<ListboxSelect>>", callback)

    def load_my_projects(self):
        self.project_list = Project.load_my_projects(self.database, self.user_id)
        for project in self.project_list:
            self.project_list_box.insert(self.project_list.index(project), project[1])

    def load_all_projects(self):
        self.project_list = Project.load_all_projects(self.database)
        for project in self.project_list:
            self.project_list_box.insert(self.project_list.index(project), project[1])

    def return_selected_project(self):
        print(self.selected_project)
        self.parent.selected_project = self.selected_project
        print(self.parent.selected_project)
        self.parent.set_selected_project_info()
        self.destroy()

    def close_window(self):
        self.destroy()


