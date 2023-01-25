import tkinter as tk
from tkinter import ttk
from typing import Callable

from database.class_equipment import Equipment
from database.class_material import Material
from database.class_user import User
from database.class_project import Project, ProjectType
from user_interface.ScrollingListFrame import ScrollingListFrame
from user_interface.find_project_window import FindProjectWindow

from client import ApiClient


class ProjectFrame(tk.LabelFrame):
    # @Todo - Need to handle default values in some way

    def __init__(self, parent, user: User, api_client: ApiClient):
        tk.LabelFrame.__init__(self, parent)
        self.parent = parent
        self.user = user
        self.api_client = api_client
        # Create empty Project for selecting

        # TODO get rid of partially initialized object.
        # self.selected_project = Project.factory("", "", ProjectType["Personal"])  
        self.selected_project = Project(None, "", "", ProjectType["Personal"])  

        self.on_remove_callback = None

        project_name_label = tk.Label(self, text="Name: ")
        self.project_name_variable = tk.StringVar(self)
        self.project_name = tk.Entry(self, textvariable=self.project_name_variable)

        project_type_label = tk.Label(self, text="Type: ")
        self.project_type_variable = tk.StringVar(self)
        # project_type_variable.set('Personal')  # Set default value
        self.project_type = ttk.Combobox(self, textvariable=self.project_type_variable)
        self.project_type['values'] = ('Personal', 'Class', 'Entrepreneurial', 'Business', 'Community', 'WorkStudy')
        self.project_type['state'] = 'readonly'

        project_description_label = tk.Label(self, text="Description: ")
        self.project_description_variable = tk.StringVar(self)
        self.project_description = tk.Entry(self, width=60, textvariable=self.project_description_variable)

        self.equipment_list_frame = ScrollingListFrame(self, height=115)
        self.equipment_list_frame.grid(row=2, column=1, columnspan=4, padx=10, pady=10)

        self.equipment_frames_list = []

        self.add_equipment()

        add_equipment_button = tk.Button(self, text="Add Another Equipment", command=self.add_equipment)
        find_project_button = tk.Button(self, text="Find Project", command=self.find_project)
        remove_project_button = tk.Button(self, text="Remove Project", command=lambda: self.on_remove_callback())

        project_name_label.grid(row=0, column=0, sticky=tk.E)
        self.project_name.grid(row=0, column=1, sticky=tk.W)

        project_type_label.grid(row=0, column=2, sticky=tk.E)
        self.project_type.grid(row=0, column=3, sticky=tk.W)

        project_description_label.grid(row=1, column=0, sticky=tk.E)
        self.project_description.grid(row=1, column=1, columnspan=3, sticky=tk.W)

        add_equipment_button.grid(row=3, column=1, padx=10, pady=10)
        find_project_button.grid(row=0, column=4, padx=4, pady=4)
        remove_project_button.grid(row=1, column=4, padx=4, pady=4)

    def add_equipment(self):
        """
        Dynamically adds equipment frames to the UI so projects can have multiple pieces of equipment used.
        :return: none
        """
        equipment = EquipmentFrame(self.equipment_list_frame.interior, self.api_client)
        equipment.on_remove(lambda: self.remove_equipment(equipment))
        self.equipment_frames_list.append(equipment)
        self.equipment_frames_list[-1].pack(padx=4, pady=4)

    def find_project(self):
        # Toplevel object which will be treated as a new window
        find_project_window = FindProjectWindow(self, self.user, self.api_client)

    def set_selected_project_info(self):
        self.project_name_variable.set(self.selected_project.project_name)
        self.project_name.config(state="disabled")
        self.project_description_variable.set(self.selected_project.project_description)
        self.project_description.config(state="disabled")
        self.project_type_variable.set(self.selected_project.project_type.name)
        self.project_type.config(state="disabled")

    def remove_equipment(self, equipment: 'EquipmentFrame'):
        """
        Dynamically removes equipment frames from the UI.
        Will throw a list index out of range error if there are no equipment elements, but this doesn't impact
        the rest of the application at this point.
        :return: none
        """
        self.equipment_frames_list.remove(equipment)
        equipment.destroy()

    def on_remove(self, callback: Callable):
        self.on_remove_callback = callback


class EquipmentFrame(tk.Frame):

    def __init__(self, parent, api_client: ApiClient):
        """
        Frame containing all the fields needed for the Equipment Record Object.
        :param parent: Parent widget in which this frame is placed
        """
        tk.Frame.__init__(self, parent)
        self.api_client = api_client

        self.on_remove_callback = None

        def set_materials(event):
            equipment_name = event.widget.get()
            equipment_index = self.equipment_names.index(equipment_name)
            self.material_names_ids = self.api_client.get_materials_for(self.equipment_names_ids[equipment_index])
            # self.material_names_ids = Material.get_material_names_for_equipment(database,
            #                                                                     self.equipment_names_ids[
            #                                                                         equipment_index][1])
            self.material_list = [mat.material_name for mat in self.material_names_ids]
            # for material in self.material_names_ids:
            #     self.material_list.append(material[0])

            self.material_used['values'] = self.material_list

        def set_unit(event):
            material_name = event.widget.get()
            index = self.material_list.index(material_name)
            material_unit = self.material_names_ids[index].unit
            self.amount_used_unit.config(text=material_unit)

        # Data Validation to ensure time and amount entries are integers only
        def validate_int(P):
            if str.isdigit(P) or P == "":
                return True
            else:
                return False

        validate_command = (self.register(validate_int))

        # database = start_workspace_database()

        equipment_label = tk.Label(self, text="Equipment: ")

        self.equipment_names_ids = self.api_client.get_equipment() # Equipment.get_all_equipment_names(database)
        self.equipment_names = [ eq.equipment_name for eq in self.equipment_names_ids ]

        self.equipment_variable = tk.StringVar(self)
        self.equipment = ttk.Combobox(self, textvariable=self.equipment_variable)
        self.equipment['values'] = self.equipment_names
        self.equipment['state'] = 'readonly'
        self.equipment.bind("<<ComboboxSelected>>", set_materials)

        time_used_label = tk.Label(self, text="Time: ")
        self.time_used_hours = tk.Entry(self, width=5, validate='all', validatecommand=(validate_command, '%P'))
        hours_label = tk.Label(self, text="hr.")
        self.time_used_minutes = tk.Entry(self, width=5, validate='all', validatecommand=(validate_command, '%P'))
        minutes_label = tk.Label(self, text="min.")

        self.material_names_ids = []
        self.material_list = []
        material_used_label = tk.Label(self, text="Material: ")
        self.material_used_variable = tk.StringVar(self)
        self.material_used = ttk.Combobox(self, textvariable=self.material_used_variable)
        self.material_used['state'] = 'readonly'
        self.material_used.bind("<<ComboboxSelected>>", set_unit)

        amount_used_label = tk.Label(self, text="Amount: ")
        self.amount_used = tk.Entry(self, width=10, validate='all', validatecommand=(validate_command, '%P'))
        self.amount_used_unit = tk.Label(self, text="Unit", justify=tk.RIGHT)

        remove_item_button = tk.Button(self, text="Remove", command=lambda: self.on_remove_callback())

        equipment_label.grid(row=0, column=0, sticky=tk.E)
        self.equipment.grid(row=0, column=1, sticky=tk.W)

        time_used_label.grid(row=0, column=2, sticky=tk.E)
        self.time_used_hours.grid(row=0, column=3, sticky=tk.E)
        hours_label.grid(row=0, column=4, sticky=tk.W)
        self.time_used_minutes.grid(row=0, column=5, sticky=tk.E)
        minutes_label.grid(row=0, column=6, sticky=tk.W)

        material_used_label.grid(row=1, column=0, sticky=tk.E)
        self.material_used.grid(row=1, column=1, sticky=tk.W)

        amount_used_label.grid(row=1, column=2, sticky=tk.E)
        self.amount_used.grid(row=1, column=3, columnspan=2, sticky=tk.W)
        self.amount_used_unit.grid(row=1, column=5, sticky=tk.E)

        remove_item_button.grid(row=0, column=7, rowspan=2)

    def on_remove(self, callback: Callable):
        self.on_remove_callback = callback

    def get_equipment(self) -> Equipment:
        equipment_name = self.equipment_variable.get()
        equipment_index = self.equipment_names.index(equipment_name)
        return self.equipment_names_ids[equipment_index]

    def get_material(self) -> Material:
        material_name = self.material_used_variable.get()
        material_index = self.material_list.index(material_name)
        return self.material_names_ids[material_index]
